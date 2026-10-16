# Contrato público (só se pode ADICIONAR; nunca remover, renomear nem mudar semântica ou default)

- **Exports e caminho**: exports nomeados `PaginaPesquisaPaginada` e `usePaginaPesquisa`, e o caminho do arquivo.
- **Props atuais**: nomes, defaults e semântica (ex.: `habilitarBuscaInicial = true`, `filtroInicial = FILTRO_INICIAL`).
- **Handle imperativo** (`paginaPesquisa.referenciaPagina`): `pesquisar`, `dados`, `paginacao`, `filtroAtual`, `ordenacao`,
  `isCarregando`, `pararCarregamento`, `iniciarCarregamento`; e o retorno de `usePaginaPesquisa()`.
  Pode acrescentar chaves. O `useImperativeHandle` NÃO tem array de deps (recria a cada render e evita valor defasado): não adicione.
- **Filtro/API**: `funcaoPesquisa` recebe `prepararFiltros({ ...FILTRO_INICIAL, ...filtroInicial, ...filtro, ...filtroFixo })`
  e a resposta consumida é `{ ok, data.entities, data (paginação), config.url, config.baseURL }`.
  Não altere a ordem desse merge nem `FILTRO_INICIAL`, e NÃO adicione chaves ao objeto de filtro por padrão
  (mudaria a query de todas as telas e o payload da exportação).
- **`filtroAtual`** guarda o filtro ANTES de `prepararFiltros`, que é aplicado em `pesquisar` e em `gerarArquivo`:
  não guarde filtro já preparado nem prepare duas vezes. Também não use `filtroAtual` para estado de UI:
  ele alimenta o `FiltroCollapse` e a exportação.
- **Callbacks**: `aoFinalizarPesquisa(resposta, filtroPreparado)`, `prepararFiltros(filtros)`,
  `tabelaProps.onChange(paginacao, filtros, sorter)` (chamado dentro de `aoOrdenarTabela`); e as funções entregues aos filhos
  (`pesquisar` → `aoPesquisar`, `buscarFiltroInicial` → `aoLimparFiltros`, `pesquisarAoPaginar` → `aoPaginar`): mantenha as assinaturas.
- **Precedência**: `...filtrosProps`, `...restTabelaProps` e `...paginacaoProps` são espalhados DEPOIS das props do componente
  (a tela consegue sobrescrever). Mantenha. O `onChange` da Tabela é sempre `aoOrdenarTabela`.
