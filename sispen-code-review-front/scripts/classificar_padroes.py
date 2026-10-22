import os
import json
import re
from collections import defaultdict, Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_BRUTOS_DIR = os.path.join(BASE_DIR, "dados_brutos")
INPUT_FILE = os.path.join(DADOS_BRUTOS_DIR, "discussoes_normalizadas.json")

def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def run():
    mrs = load_data()
    all_threads = []
    for mr in mrs:
        for t in mr["threads"]:
            all_threads.append(t)

    print(f"Analisando {len(all_threads)} threads em {len(mrs)} MRs...")

    # Imprimir todas as discussões com resumo para categorização apurada
    summary_list = []
    for idx, t in enumerate(all_threads):
        summary_list.append({
            "idx": idx,
            "mr": t["mr_iid"],
            "author": t["author"],
            "file": t["file"],
            "line": t["line"],
            "resolved": t["resolved"],
            "body": t["body"].replace("\n", " ").strip(),
            "replies": [r["body"].replace("\n", " ").strip() for r in t.get("replies", [])]
        })

    with open(os.path.join(DADOS_BRUTOS_DIR, "amostra_discussoes.json"), "w", encoding="utf-8") as f:
        json.dump(summary_list, f, ensure_ascii=False, indent=2)

    print("Salvo amostra_discussoes.json")

if __name__ == "__main__":
    run()
