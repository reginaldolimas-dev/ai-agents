#!/usr/bin/env python
"""
verificar_ambiente.py
Valida se as ferramentas do sistema (FFmpeg, FFprobe, yt-dlp)
e as bibliotecas Python (edge-tts, pydub, deep-translator) estão operacionais.
"""
import sys
import subprocess
import shutil

def check_command(cmd, name):
    path = shutil.which(cmd)
    if path:
        print(f"[OK] {name} encontrado em: {path}")
        return True
    else:
        print(f"[ERRO] {name} ({cmd}) não encontrado no PATH do sistema.", file=sys.stderr)
        return False

def check_python_modules():
    modules = ["deep_translator", "edge_tts", "pydub"]
    all_ok = True
    for mod in modules:
        try:
            __import__(mod)
            print(f"[OK] Pacote Python '{mod}' instalado.")
        except ImportError:
            print(f"[ERRO] Pacote Python '{mod}' NÃO encontrado.", file=sys.stderr)
            all_ok = False
    return all_ok

def main():
    print("Verificando ambiente de dublagem AGY...")
    ok_ffmpeg = check_command("ffmpeg", "FFmpeg")
    ok_ffprobe = check_command("ffprobe", "FFprobe")
    ok_ytdlp = check_command("yt-dlp", "yt-dlp")
    ok_python = check_python_modules()

    if ok_ffmpeg and ok_ffprobe and ok_ytdlp and ok_python:
        print("\nAmbiente 100% configurado e pronto para dublagem!")
        sys.exit(0)
    else:
        print("\nFalha na validação do ambiente. Verifique os erros acima.", file=sys.stderr)
        print("Para instalar pacotes Python: pip install yt-dlp deep-translator edge-tts pydub", file=sys.stderr)
        print("Para instalar FFmpeg no Windows: winget install Gyan.FFmpeg ou baixe em ffmpeg.org", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
