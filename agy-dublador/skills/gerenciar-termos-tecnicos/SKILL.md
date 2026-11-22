---
name: gerenciar-termos-tecnicos
description: >-
  Consulta, adiciona ou atualiza termos no glossário técnico de dublagem.
  Use quando o usuário quiser adicionar novos termos de programação ou ajustar termos existentes.
---

# Skill: Gerenciar Termos Técnicos de Dublagem

Permite inspecionar e atualizar o vocabulário técnico para evitar que o tradutor automático cometa erros conceituais (como traduzir *hooks* para *ganchos* ou *props* para *adereços*).

## Onde os Termos Ficam Armazenados
1. **Glossário Base Global do Plugin:**
   `C:\Users\reginaldo\.gemini\config\plugins\agy-dublador\scripts\termos_tecnicos.json`
2. **Glossário Específico do Projeto / Workspace (opcional):**
   `C:\dublar\termos_tecnicos.json` (ou no diretório passado em `--workdir`)

> [!NOTE]
> O tradutor carrega o glossário base global e, caso exista um `termos_tecnicos.json` na pasta de trabalho, mescla as regras de ambos automaticamente!

## Formato do Dicionário
O arquivo é um objeto JSON mapeando `"expressao_errada": "termo_correto"`:
```json
{
  "reagir": "React",
  "gancho": "hook",
  "ganchos": "hooks",
  "adereços": "props",
  "árvore de agitação": "tree shaking",
  "elevação de estado": "state lifting"
}
```

## Como Adicionar Novos Termos
Para adicionar um novo jargão (ex: *bundler*, *tailwind*, *sharding*):
1. Leia o arquivo `termos_tecnicos.json`.
2. Adicione a chave com a tradução indesejada e o valor desejado (ou o próprio termo em inglês mantido).
3. Salve o arquivo mantendo a codificação UTF-8.
