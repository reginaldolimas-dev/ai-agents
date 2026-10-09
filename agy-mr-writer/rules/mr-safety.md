# Regras de segurança para Merge Requests

- Leitura do Git é permitida: `status`, `log`, `diff`, `fetch`, `branch --show-current`.
- Operações que alteram histórico ou remoto exigem pedido explícito: `commit`, `push`, `merge`, `rebase`, `reset`, `checkout` de outra branch.
- Nunca incluir segredos, dados reais de custodiados ou trechos de dumps na mensagem do MR.
- Não inventar o que o código não faz. Em caso de dúvida, perguntar.
