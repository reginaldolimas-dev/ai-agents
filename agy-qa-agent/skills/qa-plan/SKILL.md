---
name: qa-plan
description: Use quando o usuário fornecer uma feature, história, regra de negócio ou critérios de aceitação e quiser planejar testes antes de codificar.
---

# Planejar testes de QA

1. Leia a especificação fornecida e inspecione apenas os arquivos relevantes do projeto.
2. Extraia regras de negócio, atores, permissões, estados e dependências.
3. Crie cenários positivos, negativos, limites e de regressão quando aplicáveis.
4. Associe cada cenário ao identificador do requisito original.
5. Priorize P0 (integridade/segurança), P1 (fluxos principais) e P2 (complementares).
6. Registre pré-condições, dados sintéticos, passos e resultado esperado.
7. Marque ambiguidades sem inventar regras.
8. Identifique quais cenários são adequados para UI com Playwright e quais podem precisar de API ou testes de backend.
9. Apresente o plano e aguarde aprovação antes de implementar.

Formato recomendado da matriz:
| ID | Requisito | Cenário | Pré-condições/dados | Resultado esperado | Prioridade | Tipo |
