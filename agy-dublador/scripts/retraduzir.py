#!/usr/bin/env python
"""
retraduzir.py
Varre o arquivo json_traduzido.json em busca de segmentos que
tenham permanecido em inglês e aplica retentativas automáticas.
"""
import json
import time
import sys
import os
import argparse
from deep_translator import GoogleTranslator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WORK_DIR = os.environ.get("AGY_DUBLAR_DIR", r"C:\dublar")

def is_english(text):
    """Detecta se o segmento ainda contém palavras estruturais em inglês."""
    en_words = ['the ', 'we ', 'so ', 'and ', 'this ', 'that ', 'you ', 'right', 'here', 'save',
                'click', 'let\'s', 'okay', 'want to', 'going to', 'can ', 'will ', 'have ',
                'from ', 'with ', 'for ', 'first ', 'next ', 'then ']
    text_lower = text.lower()
    en_count = sum(1 for w in en_words if w in text_lower)
    return en_count >= 3

def retraduzir(workdir=DEFAULT_WORK_DIR, retries=5):
    json_path = os.path.join(workdir, "tmp", "json_traduzido.json")
    if not os.path.exists(json_path):
        print(f"[ERRO] Arquivo não encontrado: {json_path}", file=sys.stderr)
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    indices_para_retraduzir = [i for i, seg in enumerate(data) if is_english(seg['text'])]
    total = len(indices_para_retraduzir)

    if total == 0:
        print("[RETRADUTOR] Nenhum segmento pendente em inglês encontrado. Tudo pronto!", file=sys.stderr)
        print(f"SUCESSO_RETRADUCAO: {json_path}")
        return

    print(f"[RETRADUTOR] {total} segmentos ainda parecem estar em inglês. Iniciando recuperação...", file=sys.stderr)

    translator = GoogleTranslator(source='en', target='pt')

    for count, idx in enumerate(indices_para_retraduzir):
        text = data[idx]['text']
        print(f"[{count + 1}/{total}] Re-traduzindo segmento {idx}...", end=" ", flush=True, file=sys.stderr)
        sucesso = False
        for attempt in range(retries):
            try:
                translated = translator.translate(text)
                data[idx]['text'] = translated
                print("OK", file=sys.stderr)
                sucesso = True
                break
            except Exception as e:
                wait = 2 * (attempt + 1)
                print(f"Tentativa {attempt + 1}/{retries} falhou. Aguardando {wait}s...", end=" ", flush=True, file=sys.stderr)
                time.sleep(wait)

        if not sucesso:
            print("FALHOU (mantendo texto original)", file=sys.stderr)

        time.sleep(1.0)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    restantes = sum(1 for seg in data if is_english(seg['text']))
    print(f"\n[RETRADUTOR] Concluído! Segmentos ainda em inglês: {restantes}", file=sys.stderr)
    print(f"SUCESSO_RETRADUCAO: {json_path}")

def main():
    parser = argparse.ArgumentParser(description="Re-traduz segmentos pendentes em inglês.")
    parser.add_argument("--workdir", default=DEFAULT_WORK_DIR, help="Diretório de trabalho (padrão: C:\\dublar)")
    parser.add_argument("--retries", type=int, default=5, help="Número de tentativas por segmento")

    args = parser.parse_args()
    retraduzir(workdir=args.workdir, retries=args.retries)

if __name__ == "__main__":
    main()
