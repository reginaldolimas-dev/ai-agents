#!/usr/bin/env python
"""
tradutor.py
Traduz os segmentos estruturados em tmp/raw_transcript.json para pt-BR.
Aplica correções automatizadas com base no glossário de termos técnicos.
Garante a integridade temporal (sem sobreposição) em tmp/json_traduzido.json.
"""
import json
import time
import sys
import os
import re
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WORK_DIR = os.environ.get("AGY_DUBLAR_DIR", r"C:\dublar")

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Erro: deep-translator não instalado. Execute: pip install deep-translator", file=sys.stderr)
    sys.exit(1)

def carregar_termos_tecnicos(workdir, glossario_custom=None):
    """Carrega o dicionário do plugin e mescla com glossário do workspace se existir."""
    termos = {}

    # 1. Carrega o dicionário base do plugin
    base_termos_path = os.path.join(SCRIPT_DIR, "termos_tecnicos.json")
    if os.path.exists(base_termos_path):
        try:
            with open(base_termos_path, "r", encoding="utf-8") as f:
                termos.update(json.load(f))
        except Exception as e:
            print(f"[AVISO] Não foi possível ler termos base: {e}", file=sys.stderr)

    # 2. Carrega termos específicos do workspace se existir
    workspace_termos = os.path.join(workdir, "termos_tecnicos.json")
    if os.path.exists(workspace_termos) and os.path.abspath(workspace_termos) != os.path.abspath(base_termos_path):
        try:
            with open(workspace_termos, "r", encoding="utf-8") as f:
                termos.update(json.load(f))
            print(f"[TRADUTOR] Termos do workspace mesclados de: {workspace_termos}", file=sys.stderr)
        except Exception as e:
            print(f"[AVISO] Erro ao carregar termos do workspace: {e}", file=sys.stderr)

    # 3. Carrega arquivo adicional especificado via linha de comando
    if glossario_custom and os.path.exists(glossario_custom):
        try:
            with open(glossario_custom, "r", encoding="utf-8") as f:
                termos.update(json.load(f))
            print(f"[TRADUTOR] Glossário customizado carregado de: {glossario_custom}", file=sys.stderr)
        except Exception as e:
            print(f"[AVISO] Erro ao carregar glossário customizado: {e}", file=sys.stderr)

    return termos

def corrigir_termos(texto, termos):
    """Substitui termos mal traduzidos preservando limites de palavras."""
    for termo_errado, termo_correto in termos.items():
        texto = re.sub(
            r'\b' + re.escape(termo_errado) + r'\b',
            termo_correto,
            texto,
            flags=re.IGNORECASE
        )
    return texto

def traduzir(workdir=DEFAULT_WORK_DIR, batch_size=20, glossario=None):
    tmp_dir = os.path.join(workdir, "tmp")
    input_path = os.path.join(tmp_dir, "raw_transcript.json")
    output_path = os.path.join(tmp_dir, "json_traduzido.json")

    if not os.path.exists(input_path):
        print(f"[ERRO] Arquivo de transcrição não encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"[TRADUTOR] Traduzindo {len(data)} segmentos com Google Translator...", file=sys.stderr)

    translator = GoogleTranslator(source='en', target='pt')
    termos = carregar_termos_tecnicos(workdir, glossario)

    texts = [item['text'] for item in data]
    translated_texts = []

    total_batches = (len(texts) - 1) // batch_size + 1
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_num = i // batch_size + 1
        print(f"[TRADUTOR] Traduzindo lote {batch_num}/{total_batches}...", file=sys.stderr)
        try:
            trans_batch = translator.translate_batch(batch)
            translated_texts.extend(trans_batch)
        except Exception as e:
            print(f"[AVISO] Erro no lote {batch_num}: {e}. Tentando segmento por segmento...", file=sys.stderr)
            for text in batch:
                try:
                    translated_texts.append(translator.translate(text))
                except Exception as e2:
                    print(f"[FALHA] Não foi possível traduzir: '{text}' - mantendo original.", file=sys.stderr)
                    translated_texts.append(text)
        time.sleep(0.4)

    for i, t_text in enumerate(translated_texts):
        # 1. Aplica o dicionário técnico
        t_text = corrigir_termos(t_text, termos)
        data[i]['text'] = t_text

        # 2. Garante não-sobreposição temporal
        if i > 0:
            if data[i]['start_time'] < data[i - 1]['end_time']:
                data[i]['start_time'] = data[i - 1]['end_time']

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[TRADUTOR] Concluído com sucesso! Salvo em: {output_path}", file=sys.stderr)
    print(f"SUCESSO_TRADUCAO: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Traduz segmentos de transcrição do inglês para português.")
    parser.add_argument("--workdir", default=DEFAULT_WORK_DIR, help="Diretório de trabalho (padrão: C:\\dublar)")
    parser.add_argument("--batch-size", type=int, default=20, help="Tamanho do lote para tradução em lote")
    parser.add_argument("--glossario", help="Caminho para arquivo JSON adicional de termos técnicos")

    args = parser.parse_args()
    traduzir(workdir=args.workdir, batch_size=args.batch_size, glossario=args.glossario)

if __name__ == "__main__":
    main()
