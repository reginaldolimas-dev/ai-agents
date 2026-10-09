# Regras globais de QA

- Antes de alterar código, inspecione o projeto e apresente um plano.
- Não crie nem altere arquivos no projeto-alvo sem autorização explícita após o plano.
- Nunca execute testes destrutivos em produção.
- Nunca use dados pessoais reais; prefira fixtures e dados sintéticos.
- Não presuma arquitetura, rotas, seletores, permissões, comandos ou endpoints.
- Reutilize a configuração e os padrões de testes já existentes.
- Não masque falhas com `test.skip`, `force: true`, timeouts arbitrários ou asserts fracos.
- Diferencie defeito de produto, defeito do teste, falha de ambiente e dados inválidos.
- Relate somente testes realmente executados como aprovados/reprovados.
- Mantenha o plugin e suas experiências fora do repositório do projeto-alvo.
- Quando houver ambiguidade de regra de negócio, registre a dúvida em vez de inventar comportamento.
