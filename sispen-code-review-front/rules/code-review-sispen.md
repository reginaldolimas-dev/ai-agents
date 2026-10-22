---
trigger: model_decision
description: Aplicar sempre que a tarefa envolver revisão de código (code review), análise de diff ou validação de Merge Requests no SISPEN Client ou SISPEN API.
---

# Regras de Code Review — SISPEN

Ao revisar código ou preparar um Merge Request no projeto SISPEN Client:

1. **Catálogo de Regras**: Consulte sempre o catálogo consolidado em `~/.gemini/config/plugins/sispen-code-review/regras/regras.yaml`.
2. **Severidades Estritas**:
   - `PaginaPesquisaPaginada` e ausência de Redux são **bloqueadores inegociáveis**.
   - Uso de predicados centrais (`@/utils/helpers`), proteção de `Promise.all` com `.ok` e eliminação de `try/catch` redundantes de API são **requisitos de alta prioridade**.
3. **Formatos**:
   - Siga a estrutura definida em `CODE_REVIEW_AGENT.md`.
   - Referencie os IDs das regras (`SISPEN-XXX-YY`) e justifique tecnicamente com soluções prontas.
4. **Imparcialidade**:
   - Nunca emita julgamento sobre o autor do código.
   - Avalie somente os aspectos técnicos do diff e sua compatibilidade com as convenções da equipe.
