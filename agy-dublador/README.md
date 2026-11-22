# Plugin Global AGY: `agy-dublador`

Plugin oficial e global para o **Antigravity CLI (AGY)** que capacita o Gemini a orquestrar e executar a **dublagem automatizada de vídeos técnicos do YouTube para Português do Brasil (pt-BR)**.

---

## 🚀 Recursos Principais

- **Extração Inteligente**: Baixa o vídeo original em alta qualidade e legendas JSON3 com `yt-dlp`. Agrupa sentenças respeitando pausas naturais de fala e limites de tempo.
- **Tradução com Preservação de Vocabulário Técnico**: Dicionário nativo com dezenas de jargões de desenvolvimento de software (React, Hooks, Props, State Lifting, Endpoints, Bundlers, etc.).
- **Refinamento Contextual com Gemini (LLM)**: O agente analisa as frases traduzidas e aprimora a fluidez, ritmo de fala e vocabulário antes da sintetização.
- **Síntese Vocal Neural**: Vozes ultra-realistas com Microsoft Edge-TTS (`pt-BR-AntonioNeural`, `pt-BR-FranciscaNeural`, etc.).
- **Sincronização Labial/Temporal com Pydub**: Aceleração dinâmica proporcional (speedup até 1.4x) para falas que excedem a janela original, evitando encavalamento de voz.
- **Mux Direto com FFmpeg**: Renderização do arquivo final em MP4 com vídeo original intacto e áudio em português.

---

## 📁 Estrutura do Plugin

```
C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\
├── plugin.json                     # Manifesto oficial AGY
├── README.md                       # Documentação e instruções de uso
├── rules/
│   └── dublagem-regras.md          # Diretrizes de qualidade e segurança
├── agents/
│   └── dublador.md                 # Subagente dublador registrado no AGY
├── skills/
│   ├── dublar-video/               # Fluxo completo ponta a ponta
│   ├── extrair-video-legenda/      # Download e segmentação
│   ├── traduzir-transcricao/       # Tradução e refinamento LLM
│   ├── renderizar-dublagem/        # Síntese TTS e montagem FFmpeg
│   └── gerenciar-termos-tecnicos/  # Vocabulário e jargões
└── scripts/
    ├── verificar_ambiente.py       # Diagnóstico do sistema
    ├── extrator.py                 # Extrator parametrizável
    ├── tradutor.py                 # Tradutor em lote com glossário
    ├── retraduzir.py               # Retradutor resiliente de fallback
    ├── renderizador.py             # Renderizador neural com seleção de voz
    └── termos_tecnicos.json        # Dicionário técnico padrão
```

---

## 🛠️ Como Usar no Antigravity CLI

### 1. Invocando o Subagente
Você pode pedir diretamente ao Gemini no chat:
> *"Duble o vídeo do YouTube: https://www.youtube.com/watch?v=EXEMPLO"*
ou
> *"Use o subagente dublador para traduzir e dublar este vídeo com voz feminina"*

### 2. Executando Etapas Isoladas
Você pode acionar qualquer uma das skills registradas:
- **`extrair-video-legenda`**: Baixa o vídeo e extrai `raw_transcript.json`.
- **`traduzir-transcricao`**: Traduz e permite refinar o JSON com o Gemini.
- **`renderizar-dublagem`**: Gera o áudio neural e renderiza o vídeo final.
- **`gerenciar-termos-tecnicos`**: Adiciona ou consulta termos no glossário.

---

## 🎙️ Vozes Disponíveis (Edge-TTS)

| Voz | Gênero | Característica |
| :--- | :--- | :--- |
| `pt-BR-AntonioNeural` | Masculino | Padrão, neutro, ideal para tutoriais técnicos |
| `pt-BR-FranciscaNeural` | Feminino | Claro, didático e natural |
| `pt-BR-NicolauNeural` | Masculino | Expressivo |
| `pt-BR-ThalitaNeural` | Feminino | Jovem e dinâmico |
| `pt-BR-ValerioNeural` | Masculino | Grave e encorpado |

---

## 📂 Diretórios Padrão

Por padrão, o plugin utiliza:
- **`C:\dublar\tmp\`**: Armazena arquivos temporários (`video_base.mp4`, `legenda.*.json3`, `raw_transcript.json`, `json_traduzido.json`, `audio_ptbr.mp3`).
- **`C:\dublar\output\`**: Armazena o vídeo renderizado final (`video_tecnico_ptbr.mp4`).
