---
name: mapear-usos-pagina-pesquisa
description: Mapeia, somente leitura, todos os usos de PaginaPesquisaPaginada e usePaginaPesquisa no SISPEN Client, agrupando telas por padrão de uso. Use antes de qualquer mudança no componente, ao avaliar impacto de uma nova prop, ao procurar colisão de nomes de props, ou quando o usuário perguntar "quais telas usam a listagem paginada".
---

# Mapear usos (somente leitura)

Não edite nada. Use grep/SearchText e leia só os trechos necessários.

1. Liste todos os usos de `PaginaPesquisaPaginada` e `usePaginaPesquisa`:
   - function components via hook;
   - class components via `createRef` + `paginaPesquisa={{ referenciaPagina }}`.
2. Agrupe telas com o mesmo padrão de uso.
3. Para cada grupo registre:
   - props usadas;
   - membros do handle consumidos (`pesquisar`, `dados`, `paginacao`, `filtroAtual`, `ordenacao`, `isCarregando`, `pararCarregamento`, `iniciarCarregamento`);
   - particularidades: override via `tabelaProps/filtrosProps/paginacaoProps`, `exibicaoAlternativa`, `exportarArquivo` parcial, remount por `key`.
4. Se existir `convencoes.md`, leia e siga (estilo: ele vale; retrocompatibilidade: vale o plugin).
5. Verifique se há testes/stories do componente e das telas.
6. Se for investigar nome de prop nova: faça grep do nome em todas as telas (inclusive dentro de `tabelaProps/filtrosProps/paginacaoProps`)
   e confirme que não é prop nativa do antd (Table/Pagination) já passada por alguma tela.

## Saída
Tabela: grupo | telas | props | membros do handle | particularidades. Depois, lista de testes/stories encontrados.
Responda em português do Brasil.
