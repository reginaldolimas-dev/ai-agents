import os
import sys
import json
import time
import urllib.request
import urllib.parse
import urllib.error
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_BRUTOS_DIR = os.path.join(BASE_DIR, "dados_brutos")
MRS_DIR = os.path.join(DADOS_BRUTOS_DIR, "mrs")

GITLAB_BASE_URL = "http://gitlab.sap.ce.gov.br"
PROJECT_ID = "110"  # desenvolvimento/sispen_client
DATE_FROM = "2026-04-22T00:00:00Z"
PER_PAGE = 100

def get_auth_token():
    token = os.environ.get("GITLAB_TOKEN") or os.environ.get("GITLAB_PRIVATE_TOKEN")
    if token:
        return token, "PRIVATE-TOKEN"
    
    # Exchanging local git credentials for OAuth token
    try:
        proc = subprocess.Popen(
            ["git", "credential", "fill"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        out, _ = proc.communicate("protocol=http\nhost=gitlab.sap.ce.gov.br\n")
        creds = dict(line.split("=", 1) for line in out.strip().split("\n") if "=" in line)
        username = creds.get("username")
        password = creds.get("password")
        
        if username and password:
            data = urllib.parse.urlencode({
                "grant_type": "password",
                "username": username,
                "password": password
            }).encode("utf-8")
            req = urllib.request.Request(f"{GITLAB_BASE_URL}/oauth/token", data=data, method="POST")
            with urllib.request.urlopen(req, timeout=15) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res["access_token"], "Bearer"
    except Exception as e:
        print(f"[ERRO] Falha ao obter credenciais: {e}", file=sys.stderr)
    
    return None, None

def make_request(url, token, auth_type, max_retries=3):
    headers = {
        "User-Agent": "Antigravity-GitLab-Collector/1.0"
    }
    if auth_type == "Bearer":
        headers["Authorization"] = f"Bearer {token}"
    else:
        headers["PRIVATE-TOKEN"] = token

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read().decode("utf-8")
                return json.loads(data), dict(resp.headers)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                wait = (attempt + 1) * 2
                print(f"[WARN] HTTP {e.code} em {url}. Tentando novamente em {wait}s...")
                time.sleep(wait)
            else:
                print(f"[ERRO] HTTP {e.code} em {url}: {e.read().decode('utf-8', errors='ignore')}")
                raise
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise

def collect_all_mrs(token, auth_type):
    print("=== Fase 2: Coletando lista de Merge Requests (ultimos 6 meses) ===")
    mrs_list_file = os.path.join(DADOS_BRUTOS_DIR, "mrs_list.json")
    
    if os.path.exists(mrs_list_file):
        with open(mrs_list_file, "r", encoding="utf-8") as f:
            all_mrs = json.load(f)
        print(f"[CACHE] Carregados {len(all_mrs)} MRs de {mrs_list_file}")
        return all_mrs

    all_mrs = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        url = (
            f"{GITLAB_BASE_URL}/api/v4/projects/{PROJECT_ID}/merge_requests"
            f"?updated_after={DATE_FROM}&scope=all&state=all&per_page={PER_PAGE}&page={page}"
        )
        data, headers = make_request(url, token, auth_type)
        if not data:
            break
        all_mrs.extend(data)
        total_pages = int(headers.get("x-total-pages") or headers.get("X-Total-Pages") or 1)
        total_items = headers.get("x-total") or headers.get("X-Total") or len(all_mrs)
        print(f"  Página {page}/{total_pages} coletada ({len(all_mrs)}/{total_items} MRs)")
        page += 1
        time.sleep(0.1)

    with open(mrs_list_file, "w", encoding="utf-8") as f:
        json.dump(all_mrs, f, ensure_ascii=False, indent=2)
    print(f"[OK] Total de {len(all_mrs)} MRs salvos em {mrs_list_file}\n")
    return all_mrs

def collect_mr_details(token, auth_type, mr):
    iid = mr["iid"]
    mr_file = os.path.join(MRS_DIR, f"mr_{iid}.json")
    
    if os.path.exists(mr_file):
        with open(mr_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # 1. Coleta todas as páginas de discussões
    discussions = []
    d_page = 1
    d_total_pages = 1
    while d_page <= d_total_pages:
        d_url = f"{GITLAB_BASE_URL}/api/v4/projects/{PROJECT_ID}/merge_requests/{iid}/discussions?per_page=100&page={d_page}"
        d_data, d_headers = make_request(d_url, token, auth_type)
        if not d_data:
            break
        discussions.extend(d_data)
        d_total_pages = int(d_headers.get("x-total-pages") or d_headers.get("X-Total-Pages") or 1)
        d_page += 1
        time.sleep(0.05)

    # 2. Coleta changes/diffs para contexto dos comentários inline
    changes_url = f"{GITLAB_BASE_URL}/api/v4/projects/{PROJECT_ID}/merge_requests/{iid}/changes"
    changes_data = {}
    try:
        changes_data, _ = make_request(changes_url, token, auth_type)
    except Exception as e:
        print(f"[WARN] Falha ao coletar changes para MR !{iid}: {e}")

    full_mr_record = {
        "id": mr["id"],
        "iid": mr["iid"],
        "title": mr.get("title"),
        "description": mr.get("description"),
        "state": mr.get("state"),
        "created_at": mr.get("created_at"),
        "updated_at": mr.get("updated_at"),
        "merged_at": mr.get("merged_at"),
        "closed_at": mr.get("closed_at"),
        "source_branch": mr.get("source_branch"),
        "target_branch": mr.get("target_branch"),
        "web_url": mr.get("web_url"),
        "author": {
            "username": mr.get("author", {}).get("username"),
            "name": mr.get("author", {}).get("name")
        },
        "discussions": discussions,
        "changes_count": len(changes_data.get("changes", [])),
        "changes": [
            {
                "old_path": c.get("old_path"),
                "new_path": c.get("new_path"),
                "new_file": c.get("new_file"),
                "renamed_file": c.get("renamed_file"),
                "deleted_file": c.get("deleted_file"),
                "diff": c.get("diff")
            }
            for c in changes_data.get("changes", [])
        ]
    }

    with open(mr_file, "w", encoding="utf-8") as f:
        json.dump(full_mr_record, f, ensure_ascii=False, indent=2)

    return full_mr_record

def main():
    os.makedirs(MRS_DIR, exist_ok=True)
    
    token, auth_type = get_auth_token()
    if not token:
        print("[ERRO CRITICO] Nao foi possivel obter token de autenticacao.", file=sys.stderr)
        sys.exit(1)

    print("[INFO] Autenticacao estabelecida com sucesso.")
    all_mrs = collect_all_mrs(token, auth_type)

    total_mrs = len(all_mrs)
    total_discussions = 0
    total_user_notes = 0
    total_diff_notes = 0
    mrs_with_review = 0

    print("=== Fase 2: Coletando discussoes e diffs detalhados de cada MR ===")
    for idx, mr in enumerate(all_mrs, start=1):
        iid = mr["iid"]
        full_mr = collect_mr_details(token, auth_type, mr)
        
        # Estatísticas do MR
        mr_user_notes = 0
        mr_diff_notes = 0
        for d in full_mr.get("discussions", []):
            for n in d.get("notes", []):
                if not n.get("system"):
                    mr_user_notes += 1
                    if n.get("type") == "DiffNote" or "position" in n:
                        mr_diff_notes += 1

        total_discussions += len(full_mr.get("discussions", []))
        total_user_notes += mr_user_notes
        total_diff_notes += mr_diff_notes
        if mr_user_notes > 0:
            mrs_with_review += 1

        if idx % 10 == 0 or idx == total_mrs:
            print(f"  Progresso: {idx}/{total_mrs} MRs processados... (MRs com review: {mrs_with_review}, notas de revisão: {total_user_notes})")

    resumo = {
        "projeto": "desenvolvimento/sispen_client",
        "projeto_id": 110,
        "periodo_inicio": DATE_FROM,
        "periodo_fim": datetime.now().isoformat(),
        "total_mrs": total_mrs,
        "mrs_por_estado": {
            "merged": sum(1 for m in all_mrs if m.get("state") == "merged"),
            "closed": sum(1 for m in all_mrs if m.get("state") == "closed"),
            "opened": sum(1 for m in all_mrs if m.get("state") == "opened")
        },
        "total_discussoes": total_discussions,
        "total_notas_usuario": total_user_notes,
        "total_notas_diff": total_diff_notes,
        "mrs_com_review_humano": mrs_with_review
    }

    resumo_file = os.path.join(DADOS_BRUTOS_DIR, "resumo_coleta.json")
    with open(resumo_file, "w", encoding="utf-8") as f:
        json.dump(resumo, f, ensure_ascii=False, indent=2)

    print("\n=== Coleta da Fase 2 Concluída com Sucesso! ===")
    print(f"  Total de MRs no período: {total_mrs}")
    print(f"    - Merged: {resumo['mrs_por_estado']['merged']}")
    print(f"    - Closed: {resumo['mrs_por_estado']['closed']}")
    print(f"    - Opened: {resumo['mrs_por_estado']['opened']}")
    print(f"  MRs com comentários de revisão: {mrs_with_review}")
    print(f"  Total de notas de usuários: {total_user_notes}")
    print(f"  Total de notas em linhas de diff: {total_diff_notes}")
    print(f"  Resumo gravado em: {resumo_file}")

if __name__ == "__main__":
    main()
