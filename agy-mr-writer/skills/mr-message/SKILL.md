---
name: mr-message
description: Gera a mensagem de Merge Request no padrão Objetivo / Alterações Realizadas / Como Testar a partir do diff entre a branch atual e a branch de destino do git flow.
---

# Skill: mensagem de Merge Request

## Quando usar
Quando o usuário pedir mensagem, descrição ou texto de MR/PR para a branch atual.

## Entrada
- Branch atual e branch de destino (ver agente `mr-writer`).
- Diff e commits entre as duas branches.
- Opcional: link ou número da tarefa informado pelo usuário.

## Formato de saída (obrigatório)

### Objetivo
- Descreva brevemente o que este MR pretende alcançar.

### Alterações Realizadas
- Liste as principais mudanças feitas no código de forma clara e concisa.

### Como Testar
1. Passo 1 para testar a alteração.
2. Passo 2 para testar a alteração.
3. Passo 3 para testar a alteração.

(Os textos acima são orientações: substitua pelo conteúdo real.)

## Diretrizes por seção

**Objetivo**
- Uma a três linhas sobre o problema resolvido ou a funcionalidade entregue. Foque no "porquê".

**Alterações Realizadas**
- Agrupe por área (backend, frontend, banco/migração, testes, configuração) quando houver mais de um grupo.
- Cite classes, componentes, endpoints ou migrações relevantes pelo nome real.
- Destaque o que exige atenção do revisor: mudança de contrato de API, migração, novas dependências, variáveis de ambiente, permissões.
- Ignore ruído (formatação, imports reordenados, arquivos gerados), salvo se for o foco.

**Como Testar**
- Passos numerados, executáveis e na ordem real de uso, com pré-condições e resultado esperado.
- Se o diff incluir testes automatizados, informe o comando real do projeto (verifique `pom.xml`/`package.json`).
- Se o passo a passo não puder ser deduzido do diff, escreva o roteiro mais provável e marque com "(confirmar)".

## Cuidados
- Nunca inclua dados reais de custodiados, credenciais, tokens ou conteúdo de `.env`.
- Não afirme que testes foram executados ou passaram sem verificação nesta sessão.
- Entregue o resultado em um único bloco de código markdown para facilitar a cópia.
- Sinalize commits aparentemente não relacionados ao objetivo principal.
