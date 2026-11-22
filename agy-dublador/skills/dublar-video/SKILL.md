---
name: dublar-video
description: >-
  Executa o pipeline completo de dublagem de um vídeo do YouTube para Português (pt-BR).
  Use quando o usuário solicitar dublar um vídeo técnico, passando uma URL do YouTube.
---

# Skill: Dublar Vídeo Técnico (Pipeline Completo)

Executa de ponta a ponta a dublagem de vídeos técnicos do YouTube para Português do Brasil com sincronização temporal e vozes neurais.

## Procedimento Passo a Passo

### 1. Pré-Validação de Ambiente
Execute a verificação de ferramentas do sistema e bibliotecas Python:
```powershell
python "C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\verificar_ambiente.py"
```
Se algum item falhar, informe o usuário e interrompa o processo.

### 2. Extração de Vídeo e Transcrição
Baixe o vídeo e gere os segmentos temporais em `C:\dublar\tmp\raw_transcript.json`:
```powershell
python "C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\extrator.py" "<URL_DO_YOUTUBE>"
```
*Dica:* Caso o usuário deseje usar outro diretório, passe `--workdir "<CAMINHO>"`.

### 3. Tradução e Ajuste de Termos Técnicos
Traduza os segmentos para pt-BR aplicando o dicionário de jargões técnicos:
```powershell
python "C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\tradutor.py"
```

### 4. Refinamento Contextual com Gemini (LLM)
Após a tradução preliminar:
1. Leia o arquivo `C:\dublar\tmp\json_traduzido.json`.
2. Analise os segmentos em busca de:
   - Termos técnicos que tenham sido traduzidos literalmente e devam permanecer em inglês (ex: nomes de funções, métodos de API, flags de terminal, jargões como *state lifting*, *spread operator*).
   - Pontuação truncada ou pausas artificiais que prejudicariam a síntese vocal.
   - Segmentos que permaneceram em inglês.
3. Se necessário, execute a contingência de retradução:
   ```powershell
   python "C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\retraduzir.py"
   ```
4. Salve as melhorias de texto refinadas no próprio `C:\dublar\tmp\json_traduzido.json` mantendo intocados os timestamps (`start_time` e `end_time`).

### 5. Síntese Vocal e Renderização de Vídeo
Gere a fala com Edge-TTS neural e realize o multiplexing com FFmpeg:
```powershell
python "C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\renderizador.py" json_traduzido.json --voice pt-BR-AntonioNeural
```
*Vozes disponíveis:*
- `pt-BR-AntonioNeural` (Masculino padrão)
- `pt-BR-FranciscaNeural` (Feminino)
- `pt-BR-NicolauNeural` (Masculino alternativo)
- `pt-BR-ThalitaNeural` (Feminino alternativo)

### 6. Conclusão e Entrega
Informe ao usuário que o vídeo final foi renderizado com sucesso em:
`C:\dublar\output\video_tecnico_ptbr.mp4`
