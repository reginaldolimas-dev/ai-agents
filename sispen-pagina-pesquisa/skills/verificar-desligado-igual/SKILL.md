---
name: verificar-desligado-igual
description: Prova que, sem nenhuma prop nova, o PaginaPesquisaPaginada se comporta exatamente como antes (mount, paginar, ordenar, limpar filtros, exportar) e testa a funcionalidade nova ligada, incluindo caso de borda e remount por key. Use após implementar qualquer mudança no componente, antes do relatório final, ou quando o usuário pedir "prova de retrocompatibilidade".
---

# Verificar

1. Rode lint, testes e build do projeto. Registre resultados (não altere configuração para "passar").
2. **Prova de "desligado = igual"**, SEM nenhuma prop nova, em: mount, paginar, ordenar, limpar filtros e exportar.
   Compare com o baseline (testes de caracterização escritos antes):
   - mesmos argumentos e mesmo número de chamadas de `funcaoPesquisa`;
   - mesmas chaves do handle;
   - mesmas colunas enviadas à exportação;
   - mesma renderização (snapshot/DOM).
3. Combinações de props usadas hoje (no mínimo): básica; com filtros; com `habilitaSelecaoColunas`;
   com `visualizacoesColunas`; com `exportarArquivo`; com `exibicaoAlternativa`.
4. **Funcionalidade nova LIGADA**: caminho feliz, caso de borda, remount por `key` (estado zerado, 1 pesquisa no mount),
   e os estados de render da armadilha 12 (busca inicial desabilitada, sem `camposFiltro`, lista vazia, resposta `ok` falso).
5. Confira o diff: nenhuma linha existente reformatada/movida, nenhuma tela alterada, nenhuma dependência nova, nenhuma chave nova no filtro por padrão.

Se qualquer prova falhar: pare, explique e proponha correção. Não mascare o teste.
Responda em português do Brasil.
