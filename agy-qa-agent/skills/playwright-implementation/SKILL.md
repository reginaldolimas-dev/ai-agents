---
name: playwright-implementation
description: Use quando o usuário aprovar a implementação de testes E2E ou solicitar automação de fluxos web usando Playwright.
---

# Implementar testes Playwright

## Reconhecimento
- Inspecione package scripts, dependências, configuração Playwright, autenticação e testes existentes.
- Confirme a URL e o ambiente autorizado.
- Descubra como preparar dados de teste com segurança.
- Não adicione arquivos de agente ao projeto: os testes da aplicação devem ficar no local de testes já adotado pelo projeto.

## Implementação
- Reutilize a configuração atual.
- Prefira TypeScript se o projeto já o utiliza ou se for a convenção da suíte.
- Use locators acessíveis e estáveis.
- Use `test`, `expect`, fixtures e `APIRequestContext` quando apropriado.
- Evite dependência da ordem de execução.
- Não use dados pessoais reais.
- Não execute operações destrutivas em produção.
- Não altere o código de produção apenas para facilitar o teste sem explicar o motivo e pedir autorização.

## Validação
- Execute um conjunto pequeno primeiro.
- Investigue a causa de cada falha antes de modificar o teste.
- Valide persistência após recarregar a tela quando aplicável.
- Informe os comandos e os resultados reais.
- Se não puder executar, diga exatamente o que impediu a execução e como o usuário pode executá-la.
