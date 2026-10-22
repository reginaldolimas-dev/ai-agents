---
name: revisar-mr-client
description: >-
  Executa uma revisão de código completa em uma branch ou Merge Request do SISPEN Client,
  confrontando as mudanças com o catálogo histórico de regras de Code Review da equipe.
---

# Skill: Revisar Merge Request (SISPEN Client)

Esta skill executa uma análise estática e arquitetural do diff da branch atual contra o branch de integração (`dev` ou `main`), gerando um relatório no formato oficial de Code Review do time.

## Quando Usar
- Antes de abrir um Merge Request para o branch `dev`.
- Ao receber solicitação de review de um colega.
- Para verificar se uma refatoração violou regras do time.

## Procedimento

### 1. Inspecionar o Diff
Execute no terminal do repositório:
```powershell
git fetch origin dev
git diff origin/dev...HEAD
```

### 2. Checagem Automática de Regras
Para cada arquivo alterado, avalie:

1. **`SISPEN-PAG-01`**: A tela nova cria listagem sem `PaginaPesquisaPaginada`? A prop `habilitarBuscaInicial` foi setada para `true` indevidamente?
2. **`SISPEN-HLP-01`**: Há ocorrências de `!var` para checar nulos ou vazios? Substitua por `isFalsy`, `isNonEmpty` ou `isNil`.
3. **`SISPEN-ERR-01`**: Há `try/catch` que apenas faz `alerta(e)` ao chamar serviço de API? Remova o bloco.
4. **`SISPEN-VAL-01`**: Há `Promise.all` ou múltiplos cadastros sem checar se `.ok` é verdadeiro? Adicione os guards.
5. **`SISPEN-SEC-01`**: Os botões de inserção/edição/exclusão estão envolvidos por `<ComPermissao>`?
6. **`SISPEN-RED-01`**: Houve adição de Redux? Se sim, barre imediatamente.
7. **`SISPEN-CLN-01`**: Há imports órfãos ou blocos de código comentados?

### 3. Emissão do Parecer
Utilize o formato padronizado detalhado em `CODE_REVIEW_AGENT.md`.
