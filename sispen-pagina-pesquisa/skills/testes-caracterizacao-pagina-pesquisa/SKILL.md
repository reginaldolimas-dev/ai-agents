---
name: testes-caracterizacao-pagina-pesquisa
description: Escreve testes de caracterização mínimos para PaginaPesquisaPaginada, verdes contra o código ATUAL, antes de qualquer alteração; ou, sem infraestrutura de testes, entrega roteiro de teste manual por grupo de telas. Use quando o componente não tiver testes, antes de implementar funcionalidade nova, ou quando o usuário pedir rede de segurança/testes de regressão para a listagem paginada.
---

# Rede de segurança

Use a stack de testes que o projeto JÁ tem. **Não instale nada.**

## Com infraestrutura de testes
Escreva testes verdes contra o código atual, sem alterar o componente. Cobertura mínima:
1. mount dispara exatamente 1 pesquisa;
2. paginar (argumentos de `funcaoPesquisa`, incluindo `page`/`size` e filtros);
3. ordenar (registrar o comportamento atual de `pesquisar({ sort, page: 0 })`, mesmo estranho: apenas caracterize);
4. limpar filtros (`buscarFiltroInicial` → `aoLimparFiltros`);
5. formato do handle (chaves exatas e tipos);
6. colunas enviadas à exportação;
7. `habilitarBuscaInicial={false}` (nenhuma chamada no mount; `ResultCore` "Nenhuma busca realizada ainda").

Boas práticas: mock de `funcaoPesquisa` com resposta `{ ok, data: { entities, ...paginacao }, config: { url, baseURL } }`;
registre argumentos E número de chamadas; cubra remount por `key`.
Não corrija nada que o teste revele: apenas reporte.

## Sem infraestrutura de testes
Entregue um **roteiro de teste manual por grupo de telas** (passo a passo, resultado esperado, o que observar na aba Network:
URL, query params, quantidade e momento das chamadas; e o arquivo exportado).

Responda em português do Brasil.
