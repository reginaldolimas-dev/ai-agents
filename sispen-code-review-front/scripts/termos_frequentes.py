import os
import json
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_BRUTOS_DIR = os.path.join(BASE_DIR, "dados_brutos")

with open(os.path.join(DADOS_BRUTOS_DIR, "amostra_discussoes.json"), "r", encoding="utf-8") as f:
    discussions = json.load(f)

# Coletar todas as palavras e frases mais frequentes dos corpos dos comentários
word_counts = Counter()
for d in discussions:
    words = [w.strip(".,;:?!()[]{}\"'").lower() for w in d["body"].split() if len(w) > 3]
    for w in words:
        if w not in {"para", "como", "mais", "esse", "essa", "esta", "isso", "pelo", "pela", "qual", "onde", "quando", "muito", "mesmo", "aqui", "acho", "pode", "seria", "fazer", "ficou"}:
            word_counts[w] += 1

print("Palavras mais frequentes nos reviews:")
for w, c in word_counts.most_common(40):
    print(f"  {w}: {c}")
