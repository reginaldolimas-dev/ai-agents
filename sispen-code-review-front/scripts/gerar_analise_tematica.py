import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_BRUTOS_DIR = os.path.join(BASE_DIR, "dados_brutos")

with open(os.path.join(DADOS_BRUTOS_DIR, "amostra_discussoes.json"), "r", encoding="utf-8") as f:
    discussions = json.load(f)

output_lines = []

def log(text=""):
    output_lines.append(text)

def inspect_terms(terms, label):
    log(f"\n==================== {label} ====================")
    found = 0
    for d in discussions:
        full_text = (d["body"] + " " + " ".join(d["replies"]) + " " + (d["file"] or "")).lower()
        if any(term in full_text for term in terms):
            found += 1
            log(f"MR !{d['mr']} [{d['author']}] {d['file']}:{d['line']} (Resolvido: {d['resolved']})")
            log(f"  Texto: {d['body']}")
            for r in d['replies']:
                log(f"    -> Resposta: {r}")
            log("-" * 50)
    log(f"Total encontrados para {label}: {found}")

inspect_terms(["paginapesquisa", "paginacao", "paginado", "select paginado"], "1. PAGINACAO E PESQUISA")
inspect_terms(["back", "backend", "formata", "formatar", "dto", "endpoint"], "2. INTEGRACAO BACKEND E FORMATACAO")
inspect_terms(["useeffect", "usecallback", "usememo", "usestate", "hook"], "3. HOOKS E REACT")
inspect_terms(["console.log", "debugger", "comentado", "código morto", "apaga", "remover", "sobrando"], "4. LIMPEZA E CODIGO MORTO")
inspect_terms(["valid", "obrigat", "obrigatorio", "regra", "condicao", "condição"], "5. VALIDACOES E REGRAS")
inspect_terms(["toast", "sweetalert", "alerta", "erro", "catch", "try"], "6. TRATAMENTO DE ERROS E FEEDBACK")
inspect_terms(["nome", "nomenclatura", "legivel", "padrao", "padrão"], "7. NOMENCLATURA E CONVENCOES")
inspect_terms(["permissao", "permissão", "autorizacao", "seguranca", "segurança", "token"], "8. SEGURANCA E PERMISSOES")
inspect_terms(["performance", "lento", "render", "re-render", "pesado"], "9. DESEMPENHO")
inspect_terms(["redux", "store", "dispatch"], "10. REDUX LEGADO")

with open(os.path.join(DADOS_BRUTOS_DIR, "analise_tematica.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"Relatório temático gravado com sucesso! Total linhas: {len(output_lines)}")
