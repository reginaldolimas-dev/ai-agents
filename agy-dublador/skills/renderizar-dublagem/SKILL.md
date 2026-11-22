---
name: renderizar-dublagem
description: >-
  Sintetiza as falas em português com Edge-TTS neural, sincroniza a linha do tempo
  de áudio ajustando a velocidade e mixa com o vídeo base via FFmpeg.
  Use quando o json_traduzido.json estiver pronto e revisado para gerar o vídeo final.
---

# Skill: Renderizar Áudio Neural e Vídeo Dublado

Esta skill processa o arquivo JSON com a tradução e os timestamps, gerando áudio neural sincronizado e mixando-o diretamente sobre o vídeo original com FFmpeg.

## Pré-requisitos
- `C:\dublar\tmp\video_base.mp4` presente.
- `C:\dublar\tmp\json_traduzido.json` presente e validado.

## Como Executar

### 1. Renderização Padrão (Voz Masculina - Antonio)
```powershell
python "C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\renderizador.py" json_traduzido.json
```

### 2. Renderização com Voz Feminina (Francisca)
```powershell
python "C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\renderizador.py" json_traduzido.json --voice pt-BR-FranciscaNeural
```

### 3. Argumentos Disponíveis
| Argumento | Padrão | Descrição |
| :--- | :--- | :--- |
| `json_file` | `json_traduzido.json` | Nome ou caminho do arquivo JSON de tradução |
| `--voice` | `pt-BR-AntonioNeural` | Voz neural Microsoft Edge-TTS |
| `--rate` | `+10%` | Taxa base de velocidade da fala sintetizada |
| `--output` | `video_tecnico_ptbr.mp4` | Nome do arquivo de vídeo gerado na pasta `output/` |
| `--workdir` | `C:\dublar` | Diretório de trabalho |
| `--limpar` | `false` | Remove a pasta `tmp/` após finalizar com sucesso |

### Vozes Suportadas
- `pt-BR-AntonioNeural` (Masculino, neutro e profissional - Padrão)
- `pt-BR-FranciscaNeural` (Feminino, natural e claro)
- `pt-BR-NicolauNeural` (Masculino dinâmico)
- `pt-BR-ThalitaNeural` (Feminino expressivo)
- `pt-BR-ValerioNeural` (Masculino grave)

## Resultado Final
O vídeo dublado em alta resolução será salvo em:
`C:\dublar\output\video_tecnico_ptbr.mp4`
