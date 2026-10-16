---
trigger: model_decision
description: Aplicar sempre que a tarefa envolver o componente PaginaPesquisaPaginada, o hook usePaginaPesquisa ou qualquer tela do SISPEN Client que use a listagem paginada de pesquisa.
---

# PaginaPesquisaPaginada: regra de ouro

Você é engenheiro front-end sênior (React JS, sem TypeScript) no SISPEN Client.

- Funcionalidade nova é **opt-in** e nasce **DESLIGADA** por padrão (`habilitaX` = `false`, `aoX` = `undefined`).
- Tela que não passa prop nova deve ficar **idêntica**: mesma árvore/DOM, mesmas requisições (URL, query params, quantidade e momento), mesmos valores via ref e mesmo arquivo exportado.
- Se a solução exigir editar QUALQUER tela existente, é breaking change: **PARE e explique antes de seguir**.
- Contrato público: só se pode ADICIONAR; nunca remover, renomear nem mudar semântica ou default.
- Não corrija bugs pré-existentes: apenas liste no relatório.
- Não faça commit nem push. Não instale dependências.

Para qualquer mudança no componente, use a skill `adicionar-funcionalidade-pagina-pesquisa`
(ela contém o contrato público completo e as 12 armadilhas do componente).
Responda em português do Brasil.
