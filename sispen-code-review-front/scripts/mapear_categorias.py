import os
import json
import re
from collections import defaultdict, Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_BRUTOS_DIR = os.path.join(BASE_DIR, "dados_brutos")

with open(os.path.join(DADOS_BRUTOS_DIR, "amostra_discussoes.json"), "r", encoding="utf-8") as f:
    discussions = json.load(f)

print(f"Total threads: {len(discussions)}")

# Definir regras de busca por categorias
categories_patterns = {
    "1. Arquitetura e organização": [
        r"arquitetura", r"camada", r"service", r"hook", r"componente", r"pasta", r"modular", r"responsabilidade", r"reutiliz", r"scaffold"
    ],
    "2. Integração Backend / API": [
        r"back", r"backend", r"endpoint", r"dto", r"api\.", r"swagger", r"status\s*===\s*200", r"contrato", r"requisi[çc]", r"payload"
    ],
    "3. React e JavaScript": [
        r"useeffect", r"usecallback", r"usememo", r"usestate", r"render", r"ciclo de vida", r"depend[eê]ncia", r"hook", r"async", r"promise", r"await", r"arrow function", r"desestrutura", r"props"
    ],
    "4. Banco de Dados / DTOs": [
        r"banco", r"sql", r"migration", r"consulta", r"relat[oó]rio", r"coluna", r"tabela", r"filtro"
    ],
    "5. Segurança e Permissões": [
        r"seguran[çc]a", r"permiss", r"perfil", r"autoriza", r"token", r"senha", r"privil[eé]gio", r"acesso", r"vulnerab"
    ],
    "6. Validações e Regras de Negócio": [
        r"valida", r"regra", r"obrigat[oó]rio", r"campo", r"data", r"cpf", r"dataFim", r"dataInicio", r"status", r"condi[çc][aã]o", r"neg[oó]cio"
    ],
    "7. Persistência e Transações": [
        r"salvar", r"cadastr", r"atualiz", r"delet", r"excluir", r"put", r"post", r"delete", r"patch", r"persist"
    ],
    "8. Tratamento de Erros": [
        r"try", r"catch", r"erro", r"exception", r"tratamento", r"toast", r"mensagem", r"falha", r"alerta"
    ],
    "9. Desempenho": [
        r"desempenho", r"performance", r"pagin", r"tamanho", r"lento", r"otimiz", r"loop", r"re-render", r"mem[oó]ria"
    ],
    "10. Legibilidade e Nomenclatura": [
        r"nome", r"nomenclatura", r"leg[ií]vel", r"refatora", r"c[oó]digo morto", r"coment[aá]rio", r"console\.log", r"prettier", r"formata", r"limp", r"sonar"
    ],
    "11. Testes e Regressão": [
        r"teste", r"unit[aá]rio", r"e2e", r"regress", r"cen[aá]rio", r"mock", r"jest", r"playwright"
    ],
    "12. Convenções do Projeto / ACORDO_DEV": [
        r"paginapesquisapaginada", r"acordo", r"padrao", r"padrão", r"redux", r"sweetalert", r"toast", r"ant\b", r"material", r"conven[çc]"
    ]
}

matches_by_cat = defaultdict(list)
for d in discussions:
    text = (d["body"] + " " + " ".join(d["replies"]) + " " + (d["file"] or "")).lower()
    matched = False
    for cat, pats in categories_patterns.items():
        for p in pats:
            if re.search(p, text, re.IGNORECASE):
                matches_by_cat[cat].append(d)
                matched = True
                break

for cat, items in matches_by_cat.items():
    print(f"{cat}: {len(items)} discussões")

