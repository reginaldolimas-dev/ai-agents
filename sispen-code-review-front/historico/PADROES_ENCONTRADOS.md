# Padrões Encontrados: Análise Detalhada de Code Review (SISPEN Client)

Esta análise decompõe os comportamentos, decisões arquiteturais e problemas recorrentes identificados nos **245 Merge Requests** analisados no período de 22/04/2026 a 22/10/2026.

---

## Estrutura de Classificação por Nível de Confiança

1. **Regra Confirmada (DOC)**: Documentada expressamente no `ACORDO_DEV.md` ou na arquitetura de playbooks `AGENTS.md`.
2. **Padrão Recorrente (EVID)**: Observado repetidamente em 3+ MRs de múltiplos autores/revisores, demonstrando consenso tácito da equipe.
3. **Preferência Individual (PREF)**: Opinião ou estilo sugerido por revisor específico sem evidência de consenso pleno.
4. **Sugestão Contestada (CONT)**: Sugestão que gerou debate e foi fundamentadamente refutada pelo autor do código.
5. **Hipótese Não Validada (HIPO)**: Comportamento incipiente ou pontual que requer maturação antes de virar regra.

---

## 1. Padrões por Categoria Técnica

### A. Convenções e Helpers Específicos do SISPEN (`@/utils/helpers`)

#### `SISPEN-HLP-01`: Uso Mandatório de Predicados Centrais (`isFalsy`, `isTruthy`, `isNonEmpty`, `isEqual`)
- **Status / Nível**: `Padrão Recorrente (EVID)` | **Severidade**: `Média`
- **Frequência**: 41 ocorrências em 18 MRs distintos.
- **Descrição**: Em vez de utilizar checagens booleanas nativas do JavaScript como `!variavel`, `variavel === null || variavel === undefined`, ou `variavel.length > 0`, os desenvolvedores devem importar e usar as funções de predicado de `@/utils/helpers`: `isFalsy`, `isTruthy`, `isNonEmpty`, `isEqual`, `isNotEqual` e `isNil`.
- **Justificativa Técnica**: Previne armadilhas com valores falsy do JS (`0`, `""`, `false`, `NaN`, `[]`), garante comparação profunda consistente (em objetos/arrays) e padroniza a legibilidade semântica do código em todo o monorepo.
- **Contexto de Aplicação**: Condicionais de formulários, renderização condicional, validações de props e checagem de parâmetros de pesquisa.
- **Exceções**: Expressões booleanas puras de flags já tipadas booleanamente ou operadores de curto-circuito simples.
- **Exemplo Negativo (Reprovado em Review)**:
  ```javascript
  // ❌ Reprovado nos MRs !882, !1007, !1031, !1032
  if (!agendamentoId) { ... }
  if (dados.length > 0) { ... }
  if (tipoAtividade !== 'EXTERNO') { ... }
  ```
- **Exemplo Positivo (Aprovado em Review)**:
  ```javascript
  // ✅ Padrão adotado
  import { isFalsy, isNonEmpty, isNotEqual, isEqual } from "@/utils/helpers";

  if (isFalsy(agendamentoId)) { ... }
  if (isNonEmpty(dados)) { ... }
  if (isNotEqual(tipoAtividade, CONSTANTES.EXTERNO)) { ... }
  ```
- **Evidências**:
  - MR `!882` (Pedro Venicius: *"isNonEmpty?"*)
  - MR `!1007` (Pedro Venicius: *"agendamentoId isFalsy?"*)
  - MR `!1031` (Reginaldo Silva: *"isEmpty"*)
  - MR `!1032` (Pedro Venicius: *"isNotEqual"*, Reginaldo Silva: *"isEqual"*)
  - MR `!1070` (Janiel Araujo: *"isEqual"*)

---

### B. Tratamento de Erros e Camada de Rede

#### `SISPEN-ERR-01`: Proibição de `try/catch` Redundante em Chamadas de API
- **Status / Nível**: `Padrão Recorrente (EVID)` | **Severidade**: `Alta`
- **Frequência**: 16 ocorrências em 9 MRs.
- **Descrição**: É terminantemente desaconselhado envolver chamadas de serviço de API em blocos `try/catch` vazios ou que apenas re-disparam toast genérico, a menos que haja uma ação de fallback específica na tela (ex.: resetar um estado particular).
- **Justificativa Técnica**: O cliente SISPEN possui um **Interceptor Global no Axios** configurado na camada de infraestrutura. Esse interceptor já captura qualquer status `4xx` ou `5xx`, extrai a mensagem retornada pelo backend Java e exibe o toast de notificação para o usuário. Adicionar `try/catch` local causa duplicação de alertas visuais ou captura silenciosa de erros que mascara falhas.
- **Contexto de Aplicação**: Funções assíncronas em páginas de pesquisa, modais e hooks que consomem `API.*`.
- **Exceções**: Fluxos onde o erro exige ação de rollback local (ex.: reabrir modal, restaurar backup de formulário).
- **Exemplo Negativo**:
  ```javascript
  // ❌ Reprovado nos MRs !828, !935, !954, !1032
  const carregarDados = async () => {
    try {
      const resp = await API.UnidadeSaude.listar();
      setDados(resp);
    } catch (e) {
      alertaErro("Falha ao listar unidades"); // ⚠️ Redundante! Interceptor já emite notificação
    }
  };
  ```
- **Exemplo Positivo**:
  ```javascript
  // ✅ Padrão aprovado
  const carregarDados = async () => {
    const resp = await API.UnidadeSaude.listar();
    setDados(resp);
  };
  ```
- **Evidências**:
  - MR `!828` (Pedro Venicius: *"pq o try?"*)
  - MR `!935` (Pedro Venicius: *"pode remover o try"*)
  - MR `!954` (Pedro Venicius: *"observar os interceptors, visto que se houver erro na listagem, a mensagem vinda do backend já iria ser apresentada"*)
  - MR `!1032` (Pedro Venicius: *"melhor remover esse try e deixar o interceptor apresentar o erro?"*)

---

### C. Persistência, Transações e Concorrência

#### `SISPEN-VAL-01`: Validação Estrita de Resposta (`.ok` / `status === 200`) em Operações Múltiplas
- **Status / Nível**: `Padrão Recorrente (EVID)` | **Severidade**: `Crítica`
- **Frequência**: 8 ocorrências em 4 MRs.
- **Descrição**: Em operações que envolvem `Promise.all` ou encadeamento de múltiplos cadastros/associações, nunca assumir sucesso sem checar a flag `.ok` ou o status da resposta de cada requisição antes de abrir modais ou salvar dados compostos.
- **Justificativa Técnica**: Falhas parciais em requisições paralelas podem deixar variáveis com valor `undefined`. Se o fluxo prosseguir e o usuário clicar em "Salvar", os vínculos ou permissões anteriores serão sobrescritos com vazio/nulo no banco de dados.
- **Exemplo Negativo**:
  ```javascript
  // ❌ Reprovado no MR !944
  const [respTipos, respPermissoes] = await Promise.all([
    API.Condicao.buscarTipos(),
    API.Condicao.buscarPermissoes()
  ]);
  // Abre modal ou salva diretamente sem verificar se alguma falhou!
  setDados({ tipos: respTipos.dados, permissoes: respPermissoes.dados });
  abrirModal();
  ```
- **Exemplo Positivo**:
  ```javascript
  // ✅ Padrão exigido
  const [respTipos, respPermissoes] = await Promise.all([
    API.Condicao.buscarTipos(),
    API.Condicao.buscarPermissoes()
  ]);
  if (!respTipos?.ok || !respPermissoes?.ok) {
    notificacaoAlerta("Não foi possível carregar os vínculos necessários.");
    return;
  }
  setDados({ tipos: respTipos.dados, permissoes: respPermissoes.dados });
  abrirModal();
  ```
- **Evidências**:
  - MR `!944` (Ronier Lima: *"Promise.all sem validar respostaTiposPessoas.ok... em falha, alterarEntidade grava listas undefined e o usuário pode salvar sobrescrevendo vínculos"*)
  - MR `!944` (Ronier Lima: *"formRef?.validarCampos deixa a Promise pendente se o ref não existir — Salvar pode travar"*)

---

### D. Listagens e Paginação

#### `SISPEN-PAG-01`: Obrigatoriedade Absoluta de `PaginaPesquisaPaginada` e Sem Busca Inicial
- **Status / Nível**: `Regra Confirmada (DOC - ACORDO_DEV #1 e #2)` | **Severidade**: `Bloqueadora`
- **Frequência**: 23 ocorrências diretas e indiretas.
- **Descrição**: Todas as telas de listagem de pesquisa do SISPEN Client devem utilizar o componente central `PaginaPesquisaPaginada`. É proibido carregar todos os registros de uma vez e proibido habilitar busca inicial automática sem filtros restritivos (`habilitarBuscaInicial={false}`).
- **Justificativa Técnica**: Bases prisionais possuem centenas de milhares de registros de custodiados e movimentações. Requisições sem paginação causam lentidão extrema, sobrecarga de memória no frontend e esgotamento de conexões no backend/PostgreSQL.
- **Evidências**:
  - `ACORDO_DEV.md` (Regras Obrigatórias #1 e #2)
  - MR `!931` (Pedro Venicius: *"manter o pesquisaPaginado e tratar a renderização na coluna"*)
  - MR `!948` (Davi Melo: *"coloca API.ContratoEmpresa.pesquisarPaginado direto no componente paginado"*)
  - MR `!954` (Pedro Venicius: *"se tiver usando isso para usar em um select, há um select paginado"*)

---

### E. Integração com Backend e DTOs

#### `SISPEN-INT-01`: Formatação e Tratamento Primário no Backend (Princípio DTO Pronto)
- **Status / Nível**: `Padrão Recorrente (EVID)` | **Severidade**: `Média`
- **Frequência**: 14 ocorrências em 8 MRs.
- **Descrição**: Sempre que uma informação precisar de conversão semântica (ex.: converter booleano em "Sim/Não", formatar datas compostas, cruzar status), a prioridade arquitetural é que o DTO do backend Java já entregue a informação formatada, em vez de implementar conversores complexos no JavaScript.
- **Justificativa Técnica**: Facilita a exportação direta de planilhas/PDFs, evita duplicar lógicas de exibição entre diferentes telas e simplifica o componente visual.
- **Evidências**:
  - MR `!972` (Davi Melo: *"se tratar isso no back nao precisa dessa conversão"*)
  - MR `!985` (Pedro Venicius: *"o campo é realmente ativoDescricao? -> Sim, adicionei no back para poder formatar na exportação"*)
  - MR `!1043` (Janiel Araujo: *"Não seria melhor deixar tudo no Back?"*)
  - MR `!1070` (Janiel Araujo: *"não da pra formatar direto no back?"*)

---

### F. React, Hooks e Ciclo de Vida

#### `SISPEN-RCT-01`: Prevenção de Instabilidade de Referência em Formulários (`useMemo` em Inicializadores)
- **Status / Nível**: `Padrão Recorrente (EVID)` | **Severidade**: `Alta`
- **Frequência**: 9 ocorrências.
- **Descrição**: Constantes e objetos de valores iniciais de formulário (`VALORES_INICIAIS`) que dependem de entidades carregadas assincronamente devem ser declarados com `useMemo` ou colocados fora do escopo do componente caso sejam estáticos.
- **Justificativa Técnica**: A recriação do objeto de valores iniciais em cada render dispara o ciclo de reset do formulário do Ant Design / Formik, apagando edições do usuário.
- **Evidências**:
  - MR `!944` (Ronier Lima: *"VALORES_INICIAIS recriado a cada render pode resetar o formulário... Usar useMemo dependente de entidade"*)

#### `SISPEN-RCT-02`: Preferência por Declaratividade com `<RenderizaCaso>` e `<BlocoCondicional>`
- **Status / Nível**: `Padrão Recorrente (EVID)` | **Severidade**: `Baixa / Nit`
- **Frequência**: 8 ocorrências em 5 MRs.
- **Descrição**: Em vez de cadeias complexas de `condicao ? <A /> : condicao2 ? <B /> : null`, utilizar os componentes utilitários de exibição condicional do design system interno (`<RenderizaCaso>` e `<BlocoCondicional>`).
- **Evidências**:
  - MR `!836` (Davi Melo: *"Não rolava usar o <BlocoCondicional> com o <RenderizaCaso>?"*)
  - MR `!859` (Davi Melo: *"renderizacaso"*)
  - MR `!1031` (Pedro Venicius: *"componente de blocoCondicional para esse caso"*)

---

### G. Segurança e Controle de Acesso

#### `SISPEN-SEC-01`: Envelopamento Obrigatório de Ações com `<ComPermissao>`
- **Status / Nível**: `Regra Confirmada (DOC/EVID)` | **Severidade**: `Alta`
- **Frequência**: 5 ocorrências.
- **Descrição**: Botões de ação restrita (ex.: Inserir, Excluir, Homologar, Reativar) não devem ser renderizados livremente no DOM, devendo estar envolvidos pelo componente `<ComPermissao permissao={...}>`.
- **Justificativa Técnica**: Impede que usuários sem privilégio visualizem ou interajam com rotas e botões sensíveis do sistema penitenciário.
- **Evidências**:
  - MR `!1048` (Reginaldo Silva: *"usaria o <ComPermissao... <ComPermissao..."*)
  - MR `!1051` (Ronier Lima: discussão sobre centralização de permissões)

---

### H. Higiene do Código e Nomenclatura

#### `SISPEN-CLN-01`: Proibição de Código Comentado e Imports Não Utilizados
- **Status / Nível**: `Padrão Recorrente (EVID)` | **Severidade**: `Média`
- **Frequência**: 16 ocorrências em 11 MRs.
- **Descrição**: Blocos de código descontinuados ou comentados devem ser deletados, confiando no histórico do Git. Imports não utilizados devem ser purgados.
- **Exceção Aceita**: Comentários no padrão **JSDoc** com documentação de parâmetros e tipos de retorno são permitidos e incentivados.
- **Evidências**:
  - MR `!829` (Pedro Venicius: *"não seria melhor remover? no lugar de comentar -> Justo"*)
  - MR `!882` (Pedro Venicius / Autor: debate sobre JSDoc aceito)
  - MR `!946` (Ronier Lima: *"Import DashboardMetabase adicionado sem uso. -> Remover para evitar lint"*)

---

## 2. Diferenciação das Preferências e Debates da Equipe

| ID | Tópico | Posição A | Posição B | Status |
|---|---|---|---|---|
| `SISPEN-DEB-01` | **Granularidade de Custom Hooks** | Criar hook próprio mesmo para queries pequenas de 5 linhas | Usar `useCallback` + `useFetch` na própria página para queries simples (MRs `!881`, `!973`, `!1013`) | **Preferência Individual**: Válido tolerar ambas, recomendando inline se não houver reuso |
| `SISPEN-DEB-02` | **Nomenclatura PT-BR vs Padrão React** | Usar `alteraX` em vez de `setX` no `useState` (MR `!809`) | Usar o padrão universal `setX` | **Preferência Individual**: Seguir convenção do arquivo onde está editando |
| `SISPEN-DEB-03` | **JSDoc em Utilitários** | Remover comentários para manter arquivo limpo | Manter JSDoc para providenciar autocomplete e inteligência na IDE (MR `!882`) | **Contestado e Resolvido**: JSDoc é permitido e bem-vindo |
| `SISPEN-DEB-04` | **Constantes / Enums de Passos** | Criar enum/constantes para cada passo de wizard | Manter strings literais nos componentes filhos | **Hipótese Não Validada**: Recomendado quando houver repetição de 3+ ocorrências |
