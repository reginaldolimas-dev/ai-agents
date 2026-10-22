# Catálogo de Regras de Code Review — SISPEN Client

Este catálogo reúne as diretrizes técnicas consolidadas a partir do histórico real de revisões de código e dos acordos do time no SISPEN Client. As regras são classificadas por status de maturidade e severidade.

---

## Índice Rápido de Regras

| ID | Regra | Categoria | Severidade | Status |
|---|---|---|:---:|:---:|
| `SISPEN-PAG-01` | [Obrigatoriedade de PaginaPesquisaPaginada](#sispen-pag-01) | Paginação | **Bloqueadora** | Aprovada (DOC) |
| `SISPEN-PAG-02` | [Uso de Select Paginado](#sispen-pag-02) | Paginação | **Média** | Aprovada (EVID) |
| `SISPEN-HLP-01` | [Uso de Predicados Centrais (`@/utils/helpers`)](#sispen-hlp-01) | Helpers / JS | **Alta** | Aprovada (EVID) |
| `SISPEN-ERR-01` | [Proibição de `try/catch` Redundante](#sispen-err-01) | Tratamento de Erros | **Alta** | Aprovada (EVID) |
| `SISPEN-VAL-01` | [Validação de `.ok` em `Promise.all` e Modais](#sispen-val-01) | Validação / Dados | **Crítica** | Aprovada (EVID) |
| `SISPEN-INT-01` | [Formatação e Tratamento no Backend (DTO Pronto)](#sispen-int-01) | Integração / DTO | **Média** | Aprovada (EVID) |
| `SISPEN-INT-02` | [Respeito a Parâmetros Padrão de API](#sispen-int-02) | Integração / DTO | **Baixa** | Aprovada (EVID) |
| `SISPEN-SEC-01` | [Envelopamento com `<ComPermissao>`](#sispen-sec-01) | Segurança | **Alta** | Aprovada (DOC/EVID) |
| `SISPEN-RCT-01` | [Prevenção de Reset com `useMemo` em Inicializadores](#sispen-rct-01) | React / Performance | **Alta** | Aprovada (EVID) |
| `SISPEN-RCT-02` | [Renderização Declarativa com `<RenderizaCaso>`](#sispen-rct-02) | React / UI | **Baixa** | Aprovada (EVID) |
| `SISPEN-RCT-03` | [Adoção de Hooks Oficiais do Sistema (`useModal`, `useCarregando`)](#sispen-rct-03) | React / Arquitetura | **Média** | Aprovada (EVID) |
| `SISPEN-RCT-04` | [Evitar `key={index}` em Mapeamentos](#sispen-rct-04) | React / Performance | **Média** | Aprovada (EVID) |
| `SISPEN-CLN-01` | [Remoção de Código Morto e Imports Órfãos](#sispen-cln-01) | Limpeza | **Média** | Aprovada (EVID) |
| `SISPEN-NOM-01` | [Nomenclatura Semântica e Assertiva de Funções](#sispen-nom-01) | Legibilidade | **Baixa** | Aprovada (EVID) |
| `SISPEN-RED-01` | [Proibição Total de Redux em Código Novo](#sispen-red-01) | Arquitetura | **Bloqueadora** | Aprovada (DOC) |
| `SISPEN-DEB-01` | [Granularidade de Custom Hooks em Telas](#sispen-deb-01) | Arquitetura | **Informativa** | Em Debate |
| `SISPEN-DEB-02` | [Nomenclatura PT-BR de Handlers (`altera` vs `set`)](#sispen-deb-02) | Convenções | **Informativa** | Em Debate |
| `SISPEN-HIP-01` | [Enums Obrigatórios para Passos de Wizards](#sispen-hip-01) | Arquitetura | **Baixa** | Hipótese |

---

## 1. Regras Aprovadas

### `SISPEN-PAG-01`
#### Obrigatoriedade de `PaginaPesquisaPaginada` e Sem Busca Inicial
- **Status**: `Aprovada (DOC)` — Baseada no `ACORDO_DEV.md` (Regras #1 e #2).
- **Severidade**: `Bloqueadora`
- **Descrição**: Toda listagem de entidades deve obrigatoriamente utilizar o componente `PaginaPesquisaPaginada`, passando `funcaoPesquisa={(filtros) => API.Entidade.pesquisarPaginado(filtros)}`. A prop `habilitarBuscaInicial` deve ser mantida `false` por padrão.
- **Evidências**: MRs [!931](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/931), [!948](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/948).

### `SISPEN-HLP-01`
#### Uso Obrigatório de Predicados Centrais (`@/utils/helpers`)
- **Status**: `Aprovada (EVID)`
- **Severidade**: `Alta`
- **Descrição**: Sempre utilizar as funções utilitárias `isFalsy`, `isTruthy`, `isNonEmpty`, `isEqual`, `isNotEqual` e `isNil` de `@/utils/helpers` em vez de operadores booleanos ou comparações frouxas.
- **Exemplo Correto**:
  ```javascript
  import { isFalsy, isNonEmpty, isEqual } from "@/utils/helpers";
  if (isFalsy(unidadeId)) return;
  if (isNonEmpty(listaCustodiados)) { ... }
  ```
- **Evidências**: MRs [!882](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/882), [!1007](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/1007), [!1031](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/1031), [!1032](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/1032), [!1070](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/1070).

### `SISPEN-ERR-01`
#### Proibição de `try/catch` Redundante em Requisições Simples
- **Status**: `Aprovada (EVID)`
- **Severidade**: `Alta`
- **Descrição**: Não envolver chamadas de API em blocos `try/catch` se o bloco apenas repetir alertas ou omitir o erro. O Interceptor Axios global do SISPEN Client captura os erros `4xx/5xx` e emite o toast de erro da API.
- **Exceção**: Quando o erro requer reversão de estado local específico da tela.
- **Evidências**: MRs [!828](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/828), [!935](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/935), [!954](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/954), [!1032](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/1032).

### `SISPEN-VAL-01`
#### Validação Estrita de `.ok` em `Promise.all` e Fluxos Compostos
- **Status**: `Aprovada (EVID)`
- **Severidade**: `Crítica`
- **Descrição**: Em chamadas assíncronas paralelas ou sequenciais antes de abrir modais ou salvar dados, é obrigatório checar `resposta?.ok` (ou `status === 200`). Interromper a execução caso alguma resposta falhe, evitando corromper dados com listas `undefined`.
- **Evidências**: MR [!944](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/944).

### `SISPEN-INT-01`
#### Princípio do DTO Pronto (Formatação Primária no Backend)
- **Status**: `Aprovada (EVID)`
- **Severidade**: `Média`
- **Descrição**: Conversões de exibição (ex.: booleanos para "Sim/Não", status textuais para relatórios e exportações) devem ser implementadas no backend Java/DTO, e não reformatadas manualmente com funções auxiliares no React.
- **Evidências**: MRs [!834](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/834), [!928](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/928), [!972](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/972), [!985](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/985), [!1043](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/1043), [!1070](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/1070).

### `SISPEN-SEC-01`
#### Envelopamento Mandatório com `<ComPermissao>`
- **Status**: `Aprovada (DOC/EVID)`
- **Severidade**: `Alta`
- **Descrição**: Ações restritas (inserir, editar, excluir, homologar) devem estar encapsuladas pelo componente `<ComPermissao permissao={...}>`.
- **Evidências**: MR [!1048](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/1048).

### `SISPEN-RCT-01`
#### Prevenção de Resets de Formulário com `useMemo`
- **Status**: `Aprovada (EVID)`
- **Severidade**: `Alta`
- **Descrição**: Objetos de valores iniciais de formulário (`VALORES_INICIAIS`) não devem ser declarados inline no corpo do componente. Devem ser memorizados com `useMemo` ou mantidos fora do componente.
- **Evidências**: MR [!944](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/944).

### `SISPEN-CLN-01`
#### Purga de Código Morto e Imports Não Utilizados
- **Status**: `Aprovada (EVID)`
- **Severidade**: `Média`
- **Descrição**: Proibido manter linhas ou blocos de código comentados. Comentários JSDoc explicativos de parâmetros de utilitários são permitidos e incentivados.
- **Evidências**: MRs [!829](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/829), [!882](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/882), [!946](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/946).

### `SISPEN-RED-01`
#### Proibição Absoluta de Redux em Código Novo
- **Status**: `Aprovada (DOC)` — `ACORDO_DEV.md` e `AGENTS.md`.
- **Severidade**: `Bloqueadora`
- **Descrição**: Redux é proibido em qualquer desenvolvimento novo. Todo novo gerenciamento de estado deve utilizar exclusivamente React Hooks e Context API.

---

## 2. Itens em Debate e Orientações

### `SISPEN-DEB-01`
#### Granularidade de Hooks Simples de Consulta
- **Status**: `Em Debate`
- **Orientação**: Se a consulta à API for simples (apenas buscar uma lista de opções para preencher um select e não houver reuso em outro módulo), é aceitável mantê-la com `useCallback` + `useFetch` no próprio componente da tela, evitando criar arquivos de hook de menos de 10 linhas. Se houver reuso ou paginação, criar o hook.
- **Evidências**: MRs [!881](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/881), [!973](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/973), [!1013](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/1013).

### `SISPEN-DEB-02`
#### Nomenclatura PT-BR vs Padrão React
- **Status**: `Em Debate`
- **Orientação**: Respeitar a convenção do módulo em que está trabalhando. Se o arquivo já adota handlers em português (`tratarClique`, `alteraEstado`), manter o padrão. Não abrir discussões no review apenas para forçar `setX` ou `alteraX`.
- **Evidências**: MRs [!809](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/809), [!1048](http://gitlab.sap.ce.gov.br/desenvolvimento/sispen_client/-/merge_requests/1048).
