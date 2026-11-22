# Regras de Dublagem Técnica - AGY Dublador

Estas diretrizes devem ser seguidas sempre que o agente ou subagente executar processos de extração, tradução e dublagem de vídeos.

## 1. Diretórios e Armazenamento
- O diretório centralizado padrão para operações de dublagem é `C:\dublar`.
- Arquivos temporários (vídeo original, arquivos `.json3`, transcrições brutas e áudios intermediários) ficam em `C:\dublar\tmp\`.
- O vídeo final gerado é salvo em `C:\dublar\output\`.
- Se o usuário especificar explicitamente um caminho diferente, use o diretório solicitado através do argumento `--workdir`.

## 2. Pré-Validação de Ambiente
- Antes de iniciar downloads ou tarefas demoradas, valide se `ffmpeg`, `yt-dlp` e os pacotes Python necessários estão acessíveis (via script `verificar_ambiente.py`).
- Em ambientes Windows, execute comandos Python utilizando `python` em vez de `python3`.

## 3. Preservação de Vocabulário Técnico
- **NUNCA** traduza nomes próprios de tecnologias, bibliotecas, ferramentas ou frameworks (ex: *React, Vite, Next.js, Docker, Kubernetes, Tailwind*).
- **NUNCA** traduza conceitos fundamentais de desenvolvimento de software de maneira literal que prejudique o entendimento do desenvolvedor:
  - *props* $\rightarrow$ manter **props** (nunca "adereços")
  - *hooks* $\rightarrow$ manter **hooks** (nunca "ganchos")
  - *placeholder* $\rightarrow$ manter **placeholder** (nunca "espaço reservado")
  - *callback* $\rightarrow$ manter **callback** (nunca "retorno de chamada")
  - *deploy / deployment* $\rightarrow$ manter **deploy / deployment** (nunca "implantação")
  - *debug / debugging* $\rightarrow$ manter **debug / depuração**
  - *state lifting* $\rightarrow$ **elevação de estado** ou **lifting state**
  - *spread operator* $\rightarrow$ **operador spread**
  - *middleware* $\rightarrow$ manter **middleware**
- Consulte e respeite sempre o dicionário `termos_tecnicos.json`.

## 4. Refinamento Contextual (Gemini)
- O Google Translate fornece uma base rápida, mas pode gerar frases truncadas ou robóticas.
- Sempre que a skill `traduzir-transcricao` for acionada, inspecione os segmentos traduzidos para garantir fluidez da língua portuguesa falada, pontuação adequada (que orienta as pausas do TTS neural) e precisão técnica.
- Ao refinar as sentenças, **NUNCA** altere a estrutura dos campos `start_time` e `end_time` no JSON. Apenas o campo `text` deve ser aprimorado.

## 5. Integridade Temporal e Renderização
- Garanta que nenhum segmento de fala inicie antes do término do segmento anterior (`start_time >= end_time_anterior`).
- O sintetizador de áudio deve respeitar a janela de tempo original do interlocutor. Quando a fala em português for mais longa que o original em inglês, aplique o ajuste dinâmico de velocidade (speedup) via `renderizador.py`.
- Não limpe a pasta `tmp/` por padrão sem confirmação do usuário, preservando o vídeo base para possíveis regravações com outra voz.
