# SISPEN Code Review — Governança e Manutenção da Base Histórica

Este arquivo contém as instruções permanentes para operadores e agentes de IA sobre como manter, atualizar e expandir a base de conhecimento de Code Review do SISPEN Client no Antigravity CLI (AGY).

---

## 1. Visão Geral da Arquitetura do Plugin

O plugin `sispen-code-review` está estruturado da seguinte forma:

```
~/.gemini/config/plugins/sispen-code-review/
├── plugin.json                 ← Metadados e manifesto do plugin AGY
├── README.md                   ← Documentação geral e guia rápido
├── AGENTS.md                   ← Instruções permanentes de manutenção da base
├── CODE_REVIEW_AGENT.md        ← Playbook operacional para revisão de novos MRs
├── agents/
│   └── code-review-client.md   ← Definição do subagente executável
├── rules/
│   └── code-review-sispen.md   ← Regras de contexto injetadas automaticamente
├── skills/
│   ├── revisar-mr-client/      ← Skill para executar a revisão de código
│   └── consultar-regras-review/← Skill para pesquisar catálogo de regras
├── config/
│   └── analysis.yaml           ← Parâmetros não-secretos da análise histórica
├── historico/
│   ├── RESUMO_EXECUTIVO.md     ← Estatísticas, cobertura e participantes
│   ├── PADROES_ENCONTRADOS.md  ← Análise detalhada dos padrões e discussões
│   └── INDICE_EVIDENCIAS.md    ← Mapeamento de rastreabilidade com links dos MRs
├── regras/
│   ├── REGRAS_CODE_REVIEW.md   ← Catálogo legível das regras aprovadas
│   └── regras.yaml             ← Catálogo estruturado consumível por IA
├── scripts/
│   ├── coletar_historico.py    ← Script Python de extração via GitLab REST API
│   └── analisar_discussoes.py  ← Script de normalização e auditoria
└── dados/
    ├── resumo_coleta.json      ← Snapshot consolidado da coleta
    └── discussoes_normalizadas.json ← Dataset normalizado e sanitizado
```

---

## 2. Como Re-executar a Coleta Periódica

A coleta histórica deve ser executada semestralmente ou trimestralmente para incorporar novas diretrizes estabelecidas pelo time.

### Pré-requisitos
1. Python 3.10+ instalado no ambiente local.
2. Variável de ambiente `$env:GITLAB_TOKEN` definida com um Personal Access Token (escopo `read_api`) OU credencial do GitLab configurada no Git Credential Manager do Windows.

### Procedimento
1. Abra o terminal e navegue até a pasta de scripts do plugin:
   ```powershell
   Set-Location -Path "$HOME\.gemini\config\plugins\sispen-code-review"
   ```
2. Atualize a data de referência no arquivo `config/analysis.yaml` se necessário.
3. Execute o script de coleta:
   ```powershell
   python scripts/coletar_historico.py
   ```
4. Em seguida, normalize os dados:
   ```powershell
   python scripts/analisar_discussoes.py
   ```
5. Atualize o `historico/RESUMO_EXECUTIVO.md` e o `historico/INDICE_EVIDENCIAS.md` com as novas ocorrências.

---

## 3. Critérios de Auditoria e Qualidade de Novas Regras

Ao analisar novas discussões para promover uma sugestão a regra:

1. **Evidência Comprovada**: Exigir pelo menos 3 MRs distintos onde a equipe convergiu para o mesmo apontamento.
2. **Resolução Efetiva**: Verificar se o autor de fato alterou o código conforme solicitado (status `resolved: true` e commit posterior com a mudança).
3. **Ausência de Conflito**: Checar se a regra não contraria o `ACORDO_DEV.md` nem regras superiores do projeto.
4. **Graduação de Severidade**:
   - `Bloqueadora`: Violações de paginação (`PaginaPesquisaPaginada`) e uso de Redux.
   - `Crítica`: Riscos de corrupção ou sobrescrita silenciosa de dados.
   - `Alta`: Helpers obrigatórios (`isFalsy`), `try/catch` redundante e `<ComPermissao>`.
   - `Média/Baixa`: Organização interna, nomes de funções e estilo declarativo.
