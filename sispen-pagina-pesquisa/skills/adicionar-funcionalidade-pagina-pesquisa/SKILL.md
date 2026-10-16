---
name: adicionar-funcionalidade-pagina-pesquisa
description: Workflow completo e seguro para ADICIONAR funcionalidade ao componente compartilhado PaginaPesquisaPaginada (ou usePaginaPesquisa) do SISPEN Client sem regressão nas telas existentes. Use SEMPRE que o usuário pedir nova prop, recurso, botão, coluna, filtro, exportação, seleção, persistência ou qualquer mudança em PaginaPesquisaPaginada, mesmo que ele não mencione "retrocompatibilidade". Cobre mapeamento, plano com aprovação, testes de caracterização, implementação aditiva, verificação "desligado = igual" e relatório final.
---

# Adicionar funcionalidade ao PaginaPesquisaPaginada

## Entrada
A funcionalidade desejada vem do pedido do usuário. Extraia dela:
o que faz • quando aparece • como a tela ativa (prop desejada, se houver ideia) • comportamento esperado •
exemplo de uso em JSX • critérios de aceite.
Se algo essencial faltar, faça no máximo 3 perguntas objetivas antes do plano.

## Antes de começar
Leia, nesta ordem:
1. `references/contrato-publico.md`: o que NUNCA pode mudar.
2. `references/armadilhas.md`: as 12 armadilhas do componente (cada uma já causou ou pode causar regressão).
3. `convencoes.md` do projeto, se existir. Conflito de estilo/nomenclatura: vale o `convencoes.md`. Conflito sobre retrocompatibilidade: vale este plugin.

## Regra de ouro
Funcionalidade nova é opt-in e nasce DESLIGADA. Tela sem prop nova fica idêntica à de hoje
(DOM, requisições, valores via ref, arquivo exportado). Se exigir editar QUALQUER tela existente,
é breaking change: PARE e explique antes de seguir.

## Processo (siga na ordem)

### A) MAPEAR (somente leitura)
Use a skill `mapear-usos-pagina-pesquisa` (ou delegue ao agente `mapeador-usos`).
Entregável: usos agrupados por padrão, props usadas, membros do handle consumidos, particularidades,
existência de testes/stories.

### B) PLANO (NÃO edite código ainda)
Apresente:
- nome, tipo e default de cada prop nova;
- em que pontos do arquivo entra cada mudança;
- quais linhas EXISTENTES serão tocadas (ideal: nenhuma além de pontos de extensão);
- matriz "grupo de telas × impacto", justificando por que o impacto é nenhum;
- comportamento em cada estado de render (armadilha 12).

Se não houver forma segura dentro do componente, proponha alternativa (componente/hook novo que reutiliza o existente).
Dúvidas: no máximo 3, objetivas.
**Aguarde o "ok" do usuário antes de implementar.**

### C) REDE DE SEGURANÇA
Use a skill `testes-caracterizacao-pagina-pesquisa` (ou o agente `escritor-testes-caracterizacao`).
Sem testes do componente: escreva ANTES testes de caracterização verdes contra o código atual.
Sem infraestrutura de testes: NÃO instale nada; entregue roteiro de teste manual por grupo de telas.

### D) IMPLEMENTAR (diff mínimo)
- Só mudanças aditivas e localizadas. Não reformatar, reordenar, renomear, extrair ou mover código existente.
- Padrões: nomes em português do Brasil; flags `habilitaX` (boolean, default `false`); eventos `aoX` (default `undefined`/no-op);
  lodash (`isNil`, `isEmpty`, `map`, `filter`...); `RenderizaCaso` para render condicional;
  wrappers `*Core` (nunca importar antd direto; se faltar wrapper, pare e pergunte); ESLint/Prettier do projeto; sem dependências novas.
- Documente cada prop nova no JSDoc acima do componente (descrição, default, exemplo).
- Filhos compartilhados (`Tabela`, `FiltroCollapse`, `Paginacao`, `AcoesDropdownSimples`, `SeletorColunasTabela`,
  `VisualizacoesColunasTabela`) e `ordenacaoTabelaUtils`: prefira não mexer; se inevitável, só aditivo e repetindo a análise de impacto para os usos DELES.
- NÃO corrija estranhezas pré-existentes; apenas liste. Já conhecidas:
  - `extensao.extesao` parece typo, mas deve ser o nome real em `EXTENSOES` (confirme e não altere);
  - `aoOrdenarTabela` e `aoAlterarVisualizacaoColunas` chamam `pesquisar({ sort, page: 0 })` sem espalhar `filtroAtual`
    (diferente de `pesquisarAoPaginar`), aparentemente descartando filtros e `size` (confirme e apenas reporte).
- Sem commit, sem push.
- Ao terminar, peça revisão ao agente `revisor-retrocompatibilidade`.

### E) VERIFICAR
Use a skill `verificar-desligado-igual`. Rode lint, testes e build. Prove "desligado = igual" sem nenhuma prop nova
e teste a funcionalidade LIGADA, incluindo caso de borda e remount por `key`.

### F) RELATÓRIO FINAL
Siga o modelo em `references/relatorio-final.md`.

Responda em português do Brasil.
