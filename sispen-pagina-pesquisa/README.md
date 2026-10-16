# sispen-pagina-pesquisa

Plugin global para o Antigravity CLI (`agy`): instruções, agentes auxiliares e skills reutilizáveis
para adicionar funcionalidades ao `PaginaPesquisaPaginada` (SISPEN Client) com risco zero de regressão.

## Instalação

```bash
agy plugin install /caminho/para/sispen-pagina-pesquisa
agy plugin list
```

Reinicie o `agy` (ou abra uma nova sessão) para carregar skills e agentes.

## Uso

No `agy`, descreva a funcionalidade e invoque a skill principal:

```
/adicionar-funcionalidade-pagina-pesquisa
Quero uma prop habilitaX que ... (o que faz, quando aparece, exemplo de JSX, critérios de aceite)
```

O fluxo para no plano (etapa B) e só implementa após o seu "ok".

## Conteúdo

| Componente | Nome | Função |
|---|---|---|
| rule | `pagina-pesquisa-paginada` | Regra de ouro e limites, carregada quando a tarefa envolve o componente |
| skill | `adicionar-funcionalidade-pagina-pesquisa` | Workflow A–F + contrato público + 12 armadilhas + modelo de relatório |
| skill | `mapear-usos-pagina-pesquisa` | Etapa A: mapeamento somente leitura |
| skill | `testes-caracterizacao-pagina-pesquisa` | Etapa C: testes de caracterização ou roteiro manual |
| skill | `verificar-desligado-igual` | Etapa E: lint/testes/build e prova de retrocompatibilidade |
| agente | `mapeador-usos` | Delegado para a etapa A |
| agente | `revisor-retrocompatibilidade` | Revisão do diff contra contrato e armadilhas |
| agente | `escritor-testes-caracterizacao` | Delegado para a etapa C |
