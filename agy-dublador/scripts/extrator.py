#!/usr/bin/env python
"""
extrator.py
Baixa o vídeo original e as legendas automáticas em inglês via yt-dlp.
Agrupa sentenças de acordo com pausas e limites temporais sem sobreposição.
Gera tmp/raw_transcript.json pronto para tradução.
"""
import sys
import json
import subprocess
import os
import glob
import argparse

DEFAULT_WORK_DIR = os.environ.get("AGY_DUBLAR_DIR", r"C:\dublar")

def get_video_duration(video_path):
    """Obtém a duração do vídeo em segundos via ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", video_path],
            capture_output=True, text=True, check=True
        )
        return float(result.stdout.strip())
    except Exception:
        return None

def find_subtitle_file(tmp_dir, base_prefix="legenda"):
    """Busca dinamicamente qualquer arquivo de legenda JSON3 baixado."""
    patterns = [
        os.path.join(tmp_dir, f"{base_prefix}.en.json3"),
        os.path.join(tmp_dir, f"{base_prefix}.en-US.json3"),
        os.path.join(tmp_dir, f"{base_prefix}.en-orig.json3"),
        os.path.join(tmp_dir, f"{base_prefix}*.json3")
    ]
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            return matches[0]
    return None

def extrair(url, workdir=DEFAULT_WORK_DIR, sub_lang="en"):
    tmp_dir = os.path.join(workdir, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)

    video_path = os.path.join(tmp_dir, "video_base.mp4")
    legenda_prefix = os.path.join(tmp_dir, "legenda")
    raw_json_path = os.path.join(tmp_dir, "raw_transcript.json")

    # Limpa arquivos de legendas anteriores para evitar misturar vídeos
    for old_sub in glob.glob(os.path.join(tmp_dir, "legenda*.json3")):
        try:
            os.remove(old_sub)
        except OSError:
            pass

    print(f"[EXTRATOR] Baixando vídeo e legendas de: {url}", file=sys.stderr)
    print(f"[EXTRATOR] Diretório de trabalho: {workdir}", file=sys.stderr)

    # 1. Baixa o vídeo
    subprocess.run([
        "yt-dlp", "--quiet", "-f", "bestvideo+bestaudio/best",
        "-o", video_path, url
    ], check=True)

    # 2. Baixa legenda automática / manual em formato JSON3
    subprocess.run([
        "yt-dlp", "--quiet", "--write-auto-sub", "--write-sub",
        "--sub-lang", sub_lang, "--sub-format", "json3",
        "--skip-download", "-o", legenda_prefix, url
    ], check=True)

    legenda_path = find_subtitle_file(tmp_dir)
    if not legenda_path or not os.path.exists(legenda_path):
        print(f"[ERRO] Nenhuma legenda em formato JSON3 encontrada para este vídeo.", file=sys.stderr)
        sys.exit(1)

    print(f"[EXTRATOR] Legenda identificada: {legenda_path}", file=sys.stderr)

    with open(legenda_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    raw = []
    for evento in dados.get("events", []):
        if "segs" in evento and "tStartMs" in evento:
            texto = "".join([seg.get("utf8", "") for seg in evento["segs"]]).strip()
            if texto and texto != "\n":
                raw.append({"start": evento["tStartMs"] / 1000.0, "text": texto})

    video_duration = get_video_duration(video_path)

    segmentos = []
    if raw:
        curr_start = raw[0]["start"]
        curr_texts = [raw[0]["text"]]

        for i in range(1, len(raw)):
            prev = raw[i - 1]
            curr = raw[i]
            pause = curr["start"] - prev["start"]
            curr_span = curr["start"] - curr_start

            # Agrupa fragmentos contíguos em sentenças completas sem sobreposição
            if (pause > 2.2 and curr_span >= 6.0) or pause > 3.2 or curr_span >= 14.0:
                segmentos.append({
                    "start_time": round(curr_start, 2),
                    "end_time": round(curr["start"], 2),
                    "text": " ".join(curr_texts)
                })
                curr_start = curr["start"]
                curr_texts = [curr["text"]]
            else:
                curr_texts.append(curr["text"])

        if curr_texts:
            if video_duration and video_duration > curr_start:
                last_end = min(video_duration, curr_start + 8.0)
            else:
                last_end = curr_start + 4.0
            segmentos.append({
                "start_time": round(curr_start, 2),
                "end_time": round(last_end, 2),
                "text": " ".join(curr_texts)
            })

    with open(raw_json_path, "w", encoding="utf-8") as f:
        json.dump(segmentos, f, ensure_ascii=False, indent=2)

    print(f"[EXTRATOR] Total de segmentos estruturados: {len(segmentos)}", file=sys.stderr)
    print(f"[EXTRATOR] Transcrição salva em: {raw_json_path}", file=sys.stderr)
    print(f"SUCESSO_EXTRACAO: {raw_json_path}")

def main():
    parser = argparse.ArgumentParser(description="Extrai vídeo base e transcrições estruturadas do YouTube.")
    parser.add_argument("url", nargs="?", help="URL do vídeo do YouTube")
    parser.add_argument("--url", dest="url_opt", help="URL do vídeo (opcional se fornecido como argumento posicional)")
    parser.add_argument("--workdir", default=DEFAULT_WORK_DIR, help="Diretório base para pastas tmp/ e output/")
    parser.add_argument("--sub-lang", default="en", help="Código de idioma das legendas (padrão: en)")

    args = parser.parse_args()
    target_url = args.url or args.url_opt
    if not target_url:
        print("Erro: A URL do vídeo do YouTube é obrigatória.", file=sys.stderr)
        print("Uso: python extrator.py <URL> [--workdir CAMINHO]", file=sys.stderr)
        sys.exit(1)

    extrair(target_url, workdir=args.workdir, sub_lang=args.sub_lang)

if __name__ == "__main__":
    main()
