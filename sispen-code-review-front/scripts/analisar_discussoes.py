import os
import json
import re
from collections import defaultdict, Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_BRUTOS_DIR = os.path.join(BASE_DIR, "dados_brutos")
MRS_DIR = os.path.join(DADOS_BRUTOS_DIR, "mrs")

def sanitize_text(text):
    if not text:
        return ""
    # Mascarar CPF
    text = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF_OMITIDO]', text)
    # Mascarar e-mails específicos que não sejam @sap.ce.gov.br
    # Mascarar tokens ou senhas se houver
    text = re.sub(r'(bearer\s+)[A-Za-z0-9_\-\.]{20,}', r'\1[TOKEN_OMITIDO]', text, flags=re.IGNORECASE)
    text = re.sub(r'(password|senha)\s*[:=]\s*["\']?[^\s"\']+["\']?', r'\1: [REDACTED]', text, flags=re.IGNORECASE)
    return text

def run():
    discussions_by_mr = []
    all_threads = []
    
    files = sorted(os.listdir(MRS_DIR), key=lambda x: int(x.replace('mr_', '').replace('.json', '')) if x.startswith('mr_') and x.endswith('.json') else 0)

    for f in files:
        if not f.endswith('.json') or f == 'mrs_list.json' or f == 'resumo_coleta.json':
            continue
        with open(os.path.join(MRS_DIR, f), 'r', encoding='utf-8') as fp:
            mr = json.load(fp)
            
        changes_by_path = {c.get('new_path') or c.get('old_path'): c.get('diff') for c in mr.get('changes', [])}
        
        mr_threads = []
        for d in mr.get('discussions', []):
            notes = [n for n in d.get('notes', []) if not n.get('system')]
            if not notes:
                continue
            first_note = notes[0]
            pos = first_note.get('position', {}) or {}
            file_path = pos.get('new_path') or pos.get('old_path')
            line_no = pos.get('new_line') or pos.get('old_line')
            
            # Obter trecho de diff se existir
            diff_snippet = None
            if file_path and file_path in changes_by_path:
                diff_snippet = changes_by_path[file_path]
                if diff_snippet and len(diff_snippet) > 1000:
                    diff_snippet = diff_snippet[:1000] + "... [diff truncado]"
                    
            thread_data = {
                "discussion_id": d.get("id"),
                "mr_iid": mr["iid"],
                "mr_title": mr.get("title"),
                "mr_url": mr.get("web_url"),
                "mr_state": mr.get("state"),
                "mr_author": mr.get("author", {}).get("username"),
                "author": first_note.get("author", {}).get("name") or first_note.get("author", {}).get("username"),
                "author_username": first_note.get("author", {}).get("username"),
                "created_at": first_note.get("created_at"),
                "body": sanitize_text(first_note.get("body", "")),
                "file": file_path,
                "line": line_no,
                "resolved": first_note.get("resolved", False),
                "reply_count": len(notes) - 1,
                "replies": [
                    {
                        "author": n.get("author", {}).get("name") or n.get("author", {}).get("username"),
                        "author_username": n.get("author", {}).get("username"),
                        "created_at": n.get("created_at"),
                        "body": sanitize_text(n.get("body", ""))
                    }
                    for n in notes[1:]
                ],
                "diff_snippet": diff_snippet
            }
            mr_threads.append(thread_data)
            all_threads.append(thread_data)
            
        if mr_threads:
            discussions_by_mr.append({
                "mr_iid": mr["iid"],
                "mr_title": mr.get("title"),
                "mr_url": mr.get("web_url"),
                "mr_state": mr.get("state"),
                "threads_count": len(mr_threads),
                "threads": mr_threads
            })

    output_path = os.path.join(DADOS_BRUTOS_DIR, "discussoes_normalizadas.json")
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(discussions_by_mr, fp, ensure_ascii=False, indent=2)

    print(f"Normalizacao concluida!")
    print(f"MRs com discussoes: {len(discussions_by_mr)}")
    print(f"Total threads de discussao estruturadas: {len(all_threads)}")
    print(f"Arquivo salvo em: {output_path}")

if __name__ == "__main__":
    run()
