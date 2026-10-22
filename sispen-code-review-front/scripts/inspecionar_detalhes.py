import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_BRUTOS_DIR = os.path.join(BASE_DIR, "dados_brutos")

with open(os.path.join(DADOS_BRUTOS_DIR, "amostra_discussoes.json"), "r", encoding="utf-8") as f:
    discussions = json.load(f)

# Vamos imprimir temas recorrentes específicos para inspeção minuciosa
def inspect_terms(terms, label):
    print(f"\n==================== {label} ====================")
    found = 0
    for d in discussions:
        full_text = (d["body"] + " " + " ".join(d["replies"]) + " " + (d["file"] or "")).lower()
        if any(term in full_text for term in terms):
            found += 1
            print(f"MR !{d['mr']} [{d['author']}] {d['file']}:{d['line']} (Resolvido: {d['resolved']})")
            print(f"  Texto: {d['body']}")
            for r in d['replies']:
                print(f"    ↳ Resposta: {r}")
            print("-" * 50)
    print(f"Total encontrados para {label}: {found}")

inspect_terms(["paginapesquisa", "paginacao", "paginado"], "PAGINAÇÃO / PAGINAPESQUISAPAGINADA")
inspect_terms(["back", "backend", "formata", "dto"], "FORMATACAO NO BACKEND / DTO")
inspect_terms(["useeffect", "usecallback", "usememo", "usestate"], "HOOKS REACT")
inspect_terms(["console.log", "debugger", "comentado", "código morto"], "LIMPEZA / CODIGO MORTO")
inspect_terms(["valid", "obrigat", "obrigatorio"], "VALIDACOES E REGRAS")
inspect_terms(["toast", "sweetalert", "alerta", "erro"], "ERROS E FEEDBACK")
