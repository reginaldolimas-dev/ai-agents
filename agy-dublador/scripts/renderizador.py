#!/usr/bin/env python
"""
renderizador.py
Sintetiza o áudio em português via Microsoft Edge TTS neural.
Ajusta dinamicamente a taxa de reprodução com Pydub para evitar sobreposição de fala.
Mixa áudio dublado com o vídeo original usando FFmpeg.
Salva o resultado em output/video_tecnico_ptbr.mp4.
"""
import sys
import json
import asyncio
import tempfile
import subprocess
import os
import shutil
import argparse

try:
    from pydub import AudioSegment
    from pydub.effects import speedup
    import edge_tts
except ImportError:
    print("[ERRO] Dependências ausentes. Execute: pip install edge-tts pydub", file=sys.stderr)
    sys.exit(1)

DEFAULT_WORK_DIR = os.environ.get("AGY_DUBLAR_DIR", r"C:\dublar")
DEFAULT_VOICE = "pt-BR-AntonioNeural"

async def montar_e_renderizar(workdir=DEFAULT_WORK_DIR,
                              arquivo_json="json_traduzido.json",
                              voice=DEFAULT_VOICE,
                              rate="+10%",
                              output_name="video_tecnico_ptbr.mp4",
                              limpar=False):
    tmp_dir = os.path.join(workdir, "tmp")
    output_dir = os.path.join(workdir, "output")
    os.makedirs(output_dir, exist_ok=True)

    json_path = arquivo_json if os.path.isabs(arquivo_json) else os.path.join(tmp_dir, arquivo_json)
    video_path = os.path.join(tmp_dir, "video_base.mp4")
    audio_path = os.path.join(tmp_dir, "audio_ptbr.mp3")
    output_path = os.path.join(output_dir, output_name)

    if not os.path.exists(json_path):
        print(f"[ERRO] Arquivo JSON de tradução não encontrado: {json_path}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(video_path):
        print(f"[ERRO] Vídeo base não encontrado em: {video_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[RENDERIZADOR] Lendo traduções de: {json_path}", file=sys.stderr)
    with open(json_path, 'r', encoding='utf-8') as f:
        segments = json.load(f)

    if not segments:
        print("[ERRO] Lista de segmentos vazia.", file=sys.stderr)
        sys.exit(1)

    last_end = segments[-1].get("end_time", 1.0) * 1000
    final_audio = AudioSegment.silent(duration=int(last_end) + 3000)

    print(f"[RENDERIZADOR] Sintetizando {len(segments)} falas com Edge-TTS ({voice}, rate={rate})...", file=sys.stderr)

    with tempfile.TemporaryDirectory() as tmpdir:
        sem = asyncio.Semaphore(10)

        async def sintetizar(idx, txt):
            temp_file = os.path.join(tmpdir, f"seg_{idx}.mp3")
            for attempt in range(3):
                try:
                    communicate = edge_tts.Communicate(txt, voice, rate=rate)
                    await communicate.save(temp_file)
                    return
                except Exception as err:
                    if attempt == 2:
                        print(f"[AVISO] Falha ao sintetizar segmento {idx}: {err}", file=sys.stderr)
                        # Gera silêncio mínimo como fallback para não travar
                        silencio = AudioSegment.silent(duration=1000)
                        silencio.export(temp_file, format="mp3")
                        return
                    await asyncio.sleep(0.5)

        async def tarefa(idx, txt):
            async with sem:
                await sintetizar(idx, txt)

        await asyncio.gather(*(tarefa(i, seg["text"]) for i, seg in enumerate(segments)))

        print("[RENDERIZADOR] Ajustando tempos e mixando timeline de áudio...", file=sys.stderr)
        cursor_ms = 0
        for i, seg in enumerate(segments):
            start_ms = int(seg["start_time"] * 1000)
            target_end_ms = int(seg["end_time"] * 1000) if "end_time" in seg else start_ms + 3000

            # Garante que uma nova fala JAMAIS comece antes da anterior terminar
            if start_ms < cursor_ms:
                start_ms = cursor_ms

            temp_mp3 = os.path.join(tmpdir, f"seg_{i}.mp3")
            if not os.path.exists(temp_mp3):
                continue

            seg_audio = AudioSegment.from_mp3(temp_mp3)

            # Se a fala sintetizada exceder a janela até o próximo segmento, aceleramos para caber
            available_ms = target_end_ms - start_ms
            if available_ms > 400 and len(seg_audio) > available_ms:
                ratio = len(seg_audio) / available_ms
                if ratio <= 1.4:
                    seg_audio = speedup(seg_audio, playback_speed=ratio)
                else:
                    seg_audio = speedup(seg_audio, playback_speed=1.35)

            if len(final_audio) < start_ms + len(seg_audio):
                final_audio += AudioSegment.silent(duration=(start_ms + len(seg_audio) - len(final_audio) + 1000))

            final_audio = final_audio.overlay(seg_audio, position=start_ms)
            cursor_ms = start_ms + len(seg_audio) + 60

        print(f"[RENDERIZADOR] Exportando áudio completo em: {audio_path}", file=sys.stderr)
        final_audio.export(audio_path, format="mp3")

    print(f"[RENDERIZADOR] Realizando mixagem de vídeo via FFmpeg...", file=sys.stderr)
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path, "-i", audio_path,
        "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_path
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"[RENDERIZADOR] Vídeo dublado renderizado com sucesso em: {output_path}", file=sys.stderr)
    print(f"SUCESSO_RENDERIZACAO: {output_path}")

    if limpar:
        print("[RENDERIZADOR] Limpando pasta temporária tmp/...", file=sys.stderr)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        print("[RENDERIZADOR] Arquivos temporários removidos.", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Sintetiza áudio neural e renderiza vídeo dublado via FFmpeg.")
    parser.add_argument("json_file", nargs="?", default="json_traduzido.json", help="Arquivo JSON de tradução")
    parser.add_argument("--json", dest="json_opt", help="Caminho do arquivo JSON de tradução")
    parser.add_argument("--workdir", default=DEFAULT_WORK_DIR, help="Diretório de trabalho (padrão: C:\\dublar)")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Voz Edge-TTS (padrão: pt-BR-AntonioNeural)")
    parser.add_argument("--rate", default="+10%", help="Ajuste de velocidade base da voz (padrão: +10%%)")
    parser.add_argument("--output", default="video_tecnico_ptbr.mp4", help="Nome do arquivo de vídeo final")
    parser.add_argument("--limpar", action="store_true", help="Remove os arquivos temporários após renderizar")

    args = parser.parse_args()
    target_json = args.json_opt or args.json_file

    asyncio.run(montar_e_renderizar(
        workdir=args.workdir,
        arquivo_json=target_json,
        voice=args.voice,
        rate=args.rate,
        output_name=args.output,
        limpar=args.limpar
    ))

if __name__ == "__main__":
    main()
