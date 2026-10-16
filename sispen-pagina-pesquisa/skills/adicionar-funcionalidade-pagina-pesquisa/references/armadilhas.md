# Armadilhas deste componente

1. **Remount = refresh.** Telas atualizam a listagem remontando o componente via `key` (ex.: `chaveListagem` após exclusão).
   O efeito de mount (`[]`) deve seguir disparando exatamente 1 pesquisa (se `habilitarBuscaInicial`), e todo estado novo
   deve viver DENTRO do componente (nada em variável de módulo/singleton), para o remount continuar "zerando" tudo.
2. **Props inline.** Objetos, arrays e funções vindos das telas chegam com identidade nova a cada render. Nunca os use em deps
   de `useEffect/useMemo/useCallback` para disparar efeito; derive um valor estável (como o `join` de `chavesColunasDisponiveis`).
   Os `useEffect` atuais têm deps enxutas por design (só mount; só `chavesColunasDisponiveis`): não "corrija" deps/lint nem adicione dependências neles.
3. **Colunas alimentam tabela E exportação.** `obterColunasTabela()` também é usado em `tratarColunas` → `removerColunasParaExportacao`.
   Coluna sintética nova precisa de `exportavel: false`; qualquer mudança no conjunto de colunas altera o PDF/XLSX gerado.
   Sem `habilitaSelecaoColunas` e sem `visualizacoesColunas`, as colunas devem passar intactas.
4. **Config em objeto.** Quando a tela passa `exportarArquivo` (ou qualquer objeto de config), o default é substituído por inteiro, sem merge:
   chaves novas chegam `undefined` nas telas antigas. Trate `undefined` como "desligado" no ponto de uso (`obj?.chave ?? padrão`).
5. **Colisão de nomes e repasse a filhos.** `tabelaProps`, `filtrosProps` e `paginacaoProps` já são repassados a componentes filhos (antd),
   e `tabelaProps.titulo/acoes/renderizarCabecalhoExtra` são consumidos no cabeçalho E continuam em `restTabelaProps`.
   Prefira props novas no nível do componente (`habilitaX`, `aoX`) e não altere o destructuring de `tabelaProps`.
   Antes de criar qualquer prop/chave, faça grep e confirme que o nome não é usado por nenhuma tela (nem dentro desses objetos)
   nem é prop nativa do antd (Table/Pagination) que as telas já passem. Props novas repassadas a filhos: só com a flag ligada
   (spread condicional) e ANTES do spread `...xProps`, para que, desligada, o filho receba exatamente as mesmas props de hoje.
6. **Dois flags de loading.** `isCarregando` é controlado pelas telas via handle (`iniciarCarregamento/pararCarregamento`);
   `isCarregandoDados` é interno. Não use o primeiro para estados internos de features novas e não os unifique.
7. **Render e hooks.** Hook nunca é chamado condicionalmente por causa de prop (desligada, ele continua sendo chamado e fica inerte).
   `RenderizaCaso` não adia a avaliação das expressões JSX dos filhos: monte props de elementos novos com `?.`/defaults, senão telas antigas quebram.
   Com a flag desligada: sem `setState` extra no mount, sem wrappers/Fragments/divs novos, sem mexer em `RowCore/ColCore`, spans ou ordem dos elementos;
   o botão "Exportar" (`AcoesDropdownSimples`) continua sempre renderizado.
8. **Imutabilidade.** Não mute `resposta`, `dados`, filtros nem `colunas` recebidos: as telas compartilham essas referências
   (`aoFinalizarPesquisa` recebe a própria `resposta`). Trabalhe com cópias.
9. **Persistência.** `chaveLocalStorage` pertence ao `FiltroCollapse`. Persistência nova usa chave própria com namespace,
   é opt-in e nunca lê/escreve as chaves existentes.
10. **Imports.** `isFalsy` e `isNonEmpty` vêm de `@/utils/helpers` (não existem no lodash; importar de lá gera `isFalsy is not a function`).
    Os demais utilitários vêm do lodash, como hoje.
11. **Consumidores variados.** Telas podem ser class components (Redux/reduxsauce) ou function components (Context API).
    Toda ativação deve ser só por props, sem exigir hook, Context ou Provider na tela.
12. **Estados de render.** Declare o comportamento de cada funcionalidade em: busca inicial desabilitada
    (`ResultCore` "Nenhuma busca realizada ainda"), `exibicaoAlternativa`, sem `camposFiltro`, lista vazia e resposta com `ok` falso.
