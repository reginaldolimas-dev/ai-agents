---
name: traduzir-transcricao
description: >-
  Traduz os segmentos de transcrição do inglês para português (pt-BR) com deep-translator,
  substitui termos técnicos via glossário e aplica refinamento contextual do Gemini.
  Use quando o raw_transcript.json já existir e precisar ser traduzido ou reprocessado.
---

# Skill: Traduzir e Refinar Transcrição

Converte a transcrição em inglês para Português do Brasil, aplicando dicionário especializado de termos técnicos de desenvolvimento de software e permitindo refinamento contextual pelo Gemini.

## Etapa A: Tradução Preliminar com Glossário

Execute o script de tradução em lote:
```powershell
python "C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\tradutor.py"
```

O script realizará:
1. Tradução em blocos de 20 segmentos via Google Translator.
2. Substituição de termos mal traduzidos utilizando `termos_tecnicos.json`.
3. Ajuste de timestamps para impedir que um segmento comece antes do anterior terminar.
4. Gravação do arquivo intermediário em `C:\dublar\tmp\json_traduzido.json`.

## Etapa B: Verificação e Retradução (Fallback)

Caso haja segmentos que falharam na primeira passagem:
```powershell
python "C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\retraduzir.py"
```

## Etapa C: Refinamento Contextual (Gemini)

1. Leia o arquivo `C:\dublar\tmp\json_traduzido.json`.
2. Como modelo de linguagem de alta capacidade, analise o texto em português para identificar:
   - Construções frasais truncadas que soem artificiais na fala falada.
   - Jargões técnicos que precisem de ajuste contextual (ex: *"elevação de estado"*, *"desestruturação"*, *"gerenciamento de estado"*).
   - Manutenção de nomes de métodos, APIs e variáveis idênticos ao código exibido em tela.
3. Atualize o arquivo `C:\dublar\tmp\json_traduzido.json` com os textos refinados.
   > [!IMPORTANT]
   > Nunca altere os números de `start_time` e `end_time` nesta etapa para preservar a sincronia temporal original.
