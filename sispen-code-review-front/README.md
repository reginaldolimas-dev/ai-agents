# Plugin: SISPEN Code Review (GitLab Knowledge Base)

Plugin global para o **Antigravity CLI (AGY)** que fornece uma base de conhecimento histórica e agentes automatizados para Code Review no ecossistema do **SISPEN Client**.

Construído a partir da mineração direta de **245 Merge Requests** e **385 comentários técnicos de revisão** dos últimos seis meses na API REST do GitLab (`http://gitlab.sap.ce.gov.br`).

---

## 📁 Estrutura do Plugin

```
~/.gemini/config/plugins/sispen-code-review/
├── plugin.json                 # Manifesto do plugin Antigravity
├── README.md                   # Este guia de uso
├── AGENTS.md                   # Instruções de governança e re-coleta periódica
├── CODE_REVIEW_AGENT.md        # Playbook de revisão para agentes de IA
├── agents/
│   └── code-review-client.md   # Subagente executável de Code Review
├── rules/
│   └── code-review-sispen.md   # Regras ativadas por contexto de revisão
├── skills/
│   ├── revisar-mr-client/      # Skill para analisar diffs locais ou de MRs
│   └── consultar-regras-review/# Skill para pesquisar catálogo de regras
├── config/
│   └── analysis.yaml           # Configurações não-secretas da análise
├── historico/
│   ├── RESUMO_EXECUTIVO.md     # Resumo estatístico do período e participantes
│   ├── PADROES_ENCONTRADOS.md  # Análise profunda dos padrões e debates
│   └── INDICE_EVIDENCIAS.md    # Tabela de evidências com links para os MRs
├── regras/
│   ├── REGRAS_CODE_REVIEW.md   # Catálogo legível com status e exemplos
│   └── regras.yaml             # Catálogo YAML estruturado para IA
├── scripts/
│   ├── coletar_historico.py    # Extrator automatizado da API REST do GitLab
│   └── analisar_discussoes.py  # Normalizador de threads e sanitizador
└── dados/
    ├── resumo_coleta.json      # Snapshot das métricas de coleta
    └── discussoes_normalizadas.json # Dataset normalizado e sanitizado
```

---

## 🚀 Como Usar no Antigravity CLI (AGY)

Como este plugin está localizado na pasta global de plugins do usuário (`~/.gemini/config/plugins/sispen-code-review`), ele é carregado automaticamente pelo Antigravity em qualquer sessão de trabalho.

### 1. Invocando o Subagente de Revisão
Você pode delegar a revisão completa de uma branch para o subagente especializado:
```markdown
"Use o subagente code-review-client para revisar as alterações da branch atual contra dev."
```

### 2. Usando a Skill de Revisão de MR
Peça diretamente ao agente para revisar seu código:
```markdown
"Execute a skill revisar-mr-client no diff atual antes de eu abrir o MR."
```

### 3. Consultando Regras e Evidências
Consulte o histórico técnico para embasar decisões arquiteturais:
```markdown
"Consulte as regras de Code Review sobre tratamento de erros em requisições de API."
"Mostre as evidências históricas sobre o uso de predicados de @/utils/helpers."
```

---

## 🔒 Segurança, Credenciais e LGPD

- **Zero Segredos Versionados**: Nenhum token ou senha é persistido em disco. O extrator utiliza a variável `$env:GITLAB_TOKEN` em memória ou o fluxo OAuth ROPC com o Git Credential Manager local.
- **Sanitização de Dados**: Nomes de custodiados, números de prontuário, CPFs e processos foram omitidos nos arquivos de histórico.
- **Isolamento Total**: O repositório do projeto (`sispen_client`) não é modificado. Todos os artefatos de IA, regras e dados residem exclusivamente neste plugin.
