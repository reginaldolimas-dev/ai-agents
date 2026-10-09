# agy-mr-writer

Plugin global para o Antigravity CLI (AGY) que gera mensagens de Merge Request em português, seguindo git flow.

## Estrutura

```
plugin.json
agents/mr-writer.md
rules/mr-safety.md
skills/mr-message/SKILL.md
```

## Instalação

```powershell
agy plugin --help
agy plugin install https://github.com/SEU-USUARIO/agy-mr-writer
agy plugin list
```

Ou, a partir de um clone local, se a sua versão do CLI permitir: `agy plugin install C:\dev\ai-agents\agy-mr-writer`.
O `plugin.json` é um ponto de partida: se o CLI rejeitar, ajuste conforme a documentação da sua versão.

## Uso

Na branch da feature:

> Use o agente mr-writer. Analise o diff da minha branch atual, compare com a dev e gere a mensagem de MR.

Destino por tipo de branch: `feature/*` e `bugfix/*` → `dev`; `release/*` e `hotfix/*` → `main`/`master`. O agente só lê o Git (`fetch`, `log`, `diff`); não faz commit, push nem merge.
