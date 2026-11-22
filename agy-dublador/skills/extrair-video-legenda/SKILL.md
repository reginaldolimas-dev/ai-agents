---
name: extrair-video-legenda
description: >-
  Baixa o vídeo base do YouTube e extrai as legendas automáticas em inglês,
  estruturando as falas em segmentos temporais sem sobreposição em raw_transcript.json.
  Use quando precisar apenas obter o vídeo original e a transcrição temporalizada.
---

# Skill: Extrair Vídeo e Legendas

Faz o download do vídeo original em alta qualidade e extrai a transcrição automática ou manual em inglês no formato JSON3, gerando a estrutura inicial de segmentos de fala.

## Quando Usar
- Para inspecionar a transcrição original antes de traduzir.
- Quando o usuário quiser apenas baixar e segmentar o conteúdo para análise.

## Como Executar

Execute o script de extração passando a URL desejada:
```powershell
python "C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\extrator.py" "<URL_DO_YOUTUBE>"
```

### Argumentos Opcionais
- `--workdir <CAMINHO>`: Define diretório de trabalho alternativo (padrão: `C:\dublar`).
- `--sub-lang <IDIOMA>`: Define idioma da legenda a buscar (padrão: `en`).

## Saídas Geradas
- `C:\dublar\tmp\video_base.mp4`: Vídeo original baixado.
- `C:\dublar\tmp\legenda.*.json3`: Legenda bruta em formato JSON3.
- `C:\dublar\tmp\raw_transcript.json`: Lista de segmentos estruturados com `start_time`, `end_time` e `text`.
