---
name: consultar-regras-review
description: >-
  Pesquisa regras, padrões históricos e evidências de Code Review do SISPEN Client
  por categoria, palavra-chave ou identificador de regra.
---

# Skill: Consultar Regras de Review

Permite que agentes ou desenvolvedores consultem rapidamente os padrões e decisões já tomadas pelo time do SISPEN Client sobre um determinado tópico.

## Arquivos Consultados
- **Catálogo estruturado**: `~/.gemini/config/plugins/sispen-code-review/regras/regras.yaml`
- **Catálogo em prosa**: `~/.gemini/config/plugins/sispen-code-review/regras/REGRAS_CODE_REVIEW.md`
- **Índice de evidências**: `~/.gemini/config/plugins/sispen-code-review/historico/INDICE_EVIDENCIAS.md`
- **Padrões e debates**: `~/.gemini/config/plugins/sispen-code-review/historico/PADROES_ENCONTRADOS.md`

## Exemplos de Uso
- *"Quais são as regras para tratamento de erros em requisições?"* -> Exibe `SISPEN-ERR-01` e orientações sobre interceptors.
- *"Como o time trata condicionais e checagens de valores?"* -> Exibe `SISPEN-HLP-01` e a tabela de predicados de `@/utils/helpers`.
- *"É permitido usar Redux?"* -> Exibe `SISPEN-RED-01` e a proibição documentada.
