# AGY QA Playwright

Plugin global para Antigravity CLI com instruções, agentes auxiliares e skills reutilizáveis para QA e Playwright.

## Princípios

- Este repositório é independente dos projetos de aplicação, como o SIGEPEN.
- As instruções do plugin definem metodologia; os testes gerados pertencem ao projeto-alvo.
- O plugin deve começar em modo conservador: analisar e propor um plano antes de alterar arquivos.
- Nunca executar testes destrutivos contra produção nem utilizar dados pessoais reais.
- Não presumir comandos, seletores, permissões, rotas ou endpoints: inspecionar o projeto.

## Estrutura

- `plugin.json`: manifesto do plugin.
- `rules/qa-safety.md`: regras gerais de segurança e qualidade.
- `agents/qa-planner.md`: subagente para planejamento e rastreabilidade.
- `agents/playwright-engineer.md`: subagente para implementação e execução.
- `agents/qa-reviewer.md`: subagente para revisão independente.
- `skills/qa-plan/SKILL.md`: transforma requisitos em plano de testes.
- `skills/playwright-implementation/SKILL.md`: implementa testes Playwright.
- `skills/qa-review/SKILL.md`: revisa cobertura e qualidade dos testes.

## 1. Criar o repositório privado

Crie no GitHub um repositório privado chamado `agy-qa-agent`. Depois, no PowerShell:

```powershell
New-Item -ItemType Directory -Force C:\dev\ai-agents | Out-Null
Set-Location C:\dev\ai-agents
git clone https://github.com/SEU-USUARIO/agy-qa-agent.git
Set-Location .\agy-qa-agent
```

Copie os arquivos deste pacote para o repositório clonado, faça commit e push.

```powershell
git add .
git commit -m "feat: cria plugin global de QA Playwright"
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu usuário ou organização do GitHub. Para repositórios privados, configure o acesso ao GitHub no computador (por exemplo, via Git Credential Manager ou SSH).

## 2. Validar o CLI

Antes de instalar, confirme a versão e os comandos disponíveis:

```powershell
agy --version
agy plugin --help
agy plugin list
```

Os comandos podem variar conforme a versão instalada. Se `agy plugin install` não estiver disponível, consulte `agy --help` e a documentação da versão em uso.

## 3. Instalar globalmente a partir do GitHub

Execute fora do SIGEPEN:

```powershell
agy plugin install https://github.com/SEU-USUARIO/agy-qa-agent
agy plugin list
```

O plugin deve aparecer como `qa-playwright`. A instalação por GitHub precisa conseguir acessar o repositório privado com suas credenciais Git.

## 4. Desenvolvimento seguro (recomendado)

Desenvolva sempre no clone independente:

```powershell
Set-Location C:\dev\ai-agents\agy-qa-agent
git switch -c feat/novo-workflow
```

Para testar mudanças locais, verifique se a sua versão do AGY oferece instalação/link local:

```powershell
agy plugin install C:\dev\ai-agents\agy-qa-agent
```

Se já houver uma instalação com o mesmo nome e a versão do CLI não atualizar o plugin local automaticamente, não apague diretórios manualmente às cegas. Consulte `agy plugin --help` e use o procedimento de reinstalação suportado pela versão instalada.

Depois de validar:
1. Faça commit na branch de desenvolvimento.
2. Abra um Pull Request para `main`.
3. Revise o diff e faça merge.
4. Atualize a instalação global usando o procedimento de atualização/reinstalação suportado pela sua versão do AGY.
5. Reinicie a sessão do AGY e confira a lista de plugins/skills.

## 5. Usar no SIGEPEN sem adicionar arquivos de agente ao projeto

Abra o terminal na pasta do SIGEPEN e execute `agy`. O plugin global deve estar disponível sem criar `agents/`, `skills/` ou arquivos experimentais no repositório do SIGEPEN.

Ao iniciar uma tarefa, peça ao agente para:
1. inspecionar a configuração e os testes existentes;
2. apresentar o plano de testes;
3. esperar aprovação antes de modificar arquivos;
4. criar os testes no local apropriado do projeto somente após aprovação.

O plugin não substitui as regras específicas do projeto. Ele deve ler os padrões existentes do SIGEPEN e respeitá-los.

## 6. Fluxo de branches sugerido

- `main`: versão estável do plugin.
- `feat/*`: novas skills, regras ou agentes em desenvolvimento.
- `fix/*`: correções.
- Pull Request obrigatório antes de incorporar mudanças à `main`.

Não mantenha credenciais, dados reais, arquivos `.env`, screenshots com dados pessoais ou dumps do banco neste repositório.

## 7. Checklist inicial

- [ ] O repositório é privado.
- [ ] `plugin.json` está na raiz.
- [ ] O CLI reconhece o plugin.
- [ ] As skills aparecem na interface/comandos disponíveis do AGY.
- [ ] Uma sessão no SIGEPEN consegue consultar o agente sem criar arquivos de configuração no projeto.
- [ ] O agente propõe plano antes de editar arquivos.
- [ ] Nenhum dado real ou segredo foi versionado.

## Nota sobre atualização

O plugin instalado é uma cópia staged no perfil local do AGY; fazer `git pull` no clone não garante que a cópia instalada seja atualizada. Confirme os comandos de atualização suportados pela versão do AGY com `agy plugin --help`. Se não houver atualização direta, use o fluxo de desinstalar e reinstalar documentado pela versão, ou instale novamente a partir do repositório local. Faça isso apenas depois de validar as alterações e sem editar a cópia instalada manualmente.
