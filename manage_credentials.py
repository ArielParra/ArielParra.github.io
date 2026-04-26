#!/usr/bin/env python3
"""
Credentials Management CLI
Usage: python manage_credentials.py <command> [options]

Commands:
    add         Add a new credential (interactive)
    list        List credentials (optionally filtered/sorted)
    get <id>   Get a credential by ID
    delete <id> Delete a credential by ID
    sort        Sort credentials by year (default: newest first)
"""
import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path

CREDENTIALS_FILE = Path(__file__).resolve().parent / "data" / "credentials.json"
# Alternative: use when running from repo root
if not CREDENTIALS_FILE.exists():
    CREDENTIALS_FILE = Path(__file__).resolve().parent / "credentials" / "data" / "credentials.json"

CARD_TYPES = ["certification", "certificate", "badge", "award", "education", "degree"]
TYPE_PRIORITY = {"education": 4, "certification": 3, "certificate": 2, "badge": 1, "award": 0}
TOPIC_OPTIONS = ["cybersecurity", "devops", "networks", "cloud", "blockchain", "programming", "datascience", "ai", "language", "finance"]

def load_credentials():
    if not CREDENTIALS_FILE.exists():
        return {"credentials": []}
    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_credentials(data):
    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved to {CREDENTIALS_FILE}")

def generate_id(title, issued_on):
    clean = re.sub(r'[^a-zA-Z0-9]', '', title.lower().replace(' ', '-'))
    date_part = issued_on.replace('-', '')[:4] if issued_on else "unknown"
    return f"{clean}-{date_part}"

def prompt_credit_type():
    print("\nCredential type (choose from):")
    for i, t in enumerate(CARD_TYPES, 1):
        print(f"  {i}) {t}")
    while True:
        choice = input("Type [1]: ").strip()
        if not choice:
            return CARD_TYPES[0]
        if choice.isdigit() and 1 <= int(choice) <= len(CARD_TYPES):
            return CARD_TYPES[int(choice) - 1]
        if choice in CARD_TYPES:
            return choice
        print("Invalid. Choose a number or type name.")

def prompt_topics():
    print("\nTopics (comma-separated, choose from):")
    for i, t in enumerate(TOPIC_OPTIONS, 1):
        print(f"  {i}) {t}")
    while True:
        inp = input("Topics []: ").strip()
        if not inp:
            return []
        topics = []
        for part in inp.split(','):
            part = part.strip()
            if part.isdigit() and 1 <= int(part) <= len(TOPIC_OPTIONS):
                topics.append(TOPIC_OPTIONS[int(part) - 1])
            elif part.lower() in TOPIC_OPTIONS:
                topics.append(part.lower())
            else:
                topics.append(part)
        return list(set(topics))

def prompt_skills():
    print("\nSkills (comma-separated, free text):")
    while True:
        inp = input("Skills []: ").strip()
        if not inp:
            return []
        return [s.strip() for s in inp.split(',') if s.strip()]

def prompt_yesno(question):
    while True:
        ans = input(f"{question} [y/n]: ").strip().lower()
        if ans in ('y', 'yes'):
            return True
        if ans in ('n', 'no'):
            return False

def cmd_add(args):
    data = load_credentials()
    print("\n=== Add New Credential ===")
    
    title = input("Title: ").strip()
    if not title:
        print("Title required.")
        return 1
    
    ctype = prompt_credit_type()
    issuer = input("Issuer: ").strip()
    level = input("Level/Rank: ").strip()
    score = input("Score (optional): ").strip()
    issued_on = input("Issued on (YYYY-MM): ").strip()
    if issued_on:
        if not re.match(r'^\d{4}-\d{2}$', issued_on):
            print("Format: YYYY-MM (e.g., 2025-01)")
            return 1
    
    topics = prompt_topics()
    skills = prompt_skills()
    
    image = input("Image path (e.g., ./credentials/img/...): ").strip()
    if not image:
        if ctype in ("certification", "certificate"):
            safe_title = re.sub(r'[^a-zA-Z0-9]', '_', title)
            image = f"./credentials/img/{safe_title}.png"
        else:
            image = ""
    
    link = input("Verify URL (or local PDF path): ").strip()
    
    print("\n--- Description ---")
    desc_en = input("English description: ").strip()
    desc_es = input("Spanish description: ").strip()
    
    cred_id = args.get('--id') or input("ID [auto-generated]: ").strip()
    if not cred_id:
        cred_id = generate_id(title, issued_on)
    
    new_cred = {
        "id": cred_id,
        "type": ctype,
        "issuer": issuer,
        "title": title,
        "level": level,
        "score": score,
        "issuedOn": issued_on,
        "topics": topics,
        "skills": skills,
        "image": image,
        "link": link,
        "description": {
            "en": desc_en,
            "es": desc_es
        }
    }
    
    existing = data.get('credentials', [])
    for i, c in enumerate(existing):
        if c.get('id') == cred_id:
            if prompt_yesno(f"Credential '{cred_id}' exists. Overwrite?"):
                existing[i] = new_cred
                print(f"Updated '{cred_id}'.")
            else:
                print("Aborted.")
                return 0
            break
    else:
        existing.append(new_cred)
        print(f"Added '{cred_id}'.")
    
    data['credentials'] = existing
    save_credentials(data)
    return 0

def cmd_list(args):
    data = load_credentials()
    creds = data.get('credentials', [])
    
    if not creds:
        print("No credentials found.")
        return 0
    
    sort_by = args.get('--sort', 'type')
    reverse = not args.get('--asc')
    
    if sort_by == 'year' or sort_by == 'date':
        creds = sorted(creds, key=lambda c: c.get('issuedOn', ''), reverse=reverse)
        desc_str = "newest first" if reverse else "oldest first"
    elif sort_by == 'title':
        creds = sorted(creds, key=lambda c: c.get('title', '').lower(), reverse=reverse)
        desc_str = "title Z-A" if reverse else "title A-Z"
    elif sort_by == 'type':
        def sort_key(c):
            ctype = c.get('type', 'certificate')
            type_order = TYPE_PRIORITY.get(ctype, 99)
            issued = c.get('issuedOn', '')
            return (type_order, issued if reverse else '')
        creds = sorted(creds, key=sort_key, reverse=reverse)
        desc_str = "type priority, newest date per type" if reverse else "type priority, oldest date per type"
    elif sort_by == 'issuer':
        creds = sorted(creds, key=lambda c: c.get('issuer', '').lower(), reverse=reverse)
        desc_str = "issuer Z-A" if reverse else "issuer A-Z"
    else:
        desc_str = "default (type + date)"
    
    filter_type = args.get('--type')
    if filter_type:
        creds = [c for c in creds if c.get('type') == filter_type]
    
    filter_topic = args.get('--topic')
    if filter_topic:
        creds = [c for c in creds if filter_topic in c.get('topics', [])]
    
    limit = args.get('--limit')
    if limit and limit.isdigit():
        creds = creds[:int(limit)]
    
    print(f"\n{'='*60}")
    print(f"{'ID':<30} {'TYPE':<14} {'ISSUED':<10}")
    print(f"{'='*60}")
    
    for c in creds:
        cid = c.get('id', '')
        ctype = c.get('type','')
        issued = c.get('issuedOn', '')
        title = c.get('title', '')
        print(f"{cid:<30} {ctype:<14} {issued:<10}")
        print(f"  {title}")
    
    print(f"\nTotal: {len(creds)} credential(s)")
    return 0

def cmd_get(args):
    data = load_credentials()
    creds = data.get('credentials', [])
    
    cred_id = args.get('<id>')
    if not cred_id:
        print("Usage: get <credential-id>")
        return 1
    
    for c in creds:
        if c.get('id') == cred_id:
            print(json.dumps(c, indent=2, ensure_ascii=False))
            return 0
    
    print(f"Credential '{cred_id}' not found.")
    return 1

def cmd_delete(args):
    data = load_credentials()
    creds = data.get('credentials', [])
    
    cred_id = args.get('<id>')
    if not cred_id:
        print("Usage: delete <credential-id>")
        return 1
    
    new_creds = [c for c in creds if c.get('id') != cred_id]
    
    if len(new_creds) == len(creds):
        print(f"Credential '{cred_id}' not found.")
        return 1
    
    if prompt_yesno(f"Delete '{cred_id}'?"):
        data['credentials'] = new_creds
        save_credentials(data)
        print(f"Deleted '{cred_id}'.")
    else:
        print("Aborted.")
    return 0

def cmd_sort(args):
    data = load_credentials()
    creds = data.get('credentials', [])
    
    if not creds:
        print("No credentials to sort.")
        return 0
    
    order = args.get('--order', 'desc')
    reverse = (order == 'desc')
    
    def sort_key(c):
        ctype = c.get('type', 'certificate')
        type_order = TYPE_PRIORITY.get(ctype, 99)
        issued = c.get('issuedOn', '')
        return (type_order, issued if reverse else '')
    
    sorted_creds = sorted(creds, key=sort_key, reverse=reverse)
    data['credentials'] = sorted_creds
    save_credentials(data)
    
    order_text = "newest first" if reverse else "oldest first"
    print(f"Sorted by type then date ({order_text}): {len(sorted_creds)} credentials.")
    return 0

def cmd_generate(args):
    """Generate credentials/index.md from JSON"""
    data = load_credentials()
    creds = data.get('credentials', [])
    
    if not creds:
        print("No credentials to generate.")
        return 0
    
    output_file = Path(__file__).resolve().parent / "credentials" / "index.md"
    
    TYPE_ORDER = ["education", "certification", "certificate", "badge", "award"]
    TYPE_LABELS = {
        "education": "((en))Education((/en))((es))Educación((/es))",
        "certification": "((en))Certifications((/en))((es))Certificaciones((/es))",
        "certificate": "((en))Certificates((/en))((es))Certificados((/es))",
        "badge": "((en))Badges((/en))((es))Insignias((/es))",
        "award": "((en))Awards and Honors((/en))((es))Premios y Reconocimientos((/es))",
    }
    
    lines = []
    
    lines.append("---")
    lines.append("lang: en")
    lines.append("base_href: ../")
    lines.append("keywords: [Ariel Parra, certifications, certificates, badges, achievements, degree, diploma]")
    lines.append("description: Ariel Parra multiple achievements")
    lines.append("title: ((en))achievements((/en))((es))acreditaciones((/es))")
    lines.append("js: [cookies, language, theme, menu, favicon, tags, credentials]")
    lines.append("css: [theme, common, credentials]")
    lines.append("nav_current: 3")
    lines.append("---")
    lines.append("")
    
    prev_type = None
    
    for cred in creds:
        ctype = cred.get('type', 'certificate')
        
        if ctype != prev_type:
            if prev_type is not None:
                lines.append("  </div><!--container Elements-->")
                lines.append("")
            
            type_label = TYPE_LABELS.get(ctype, ctype.capitalize())
            
            lines.append('  <div class="container">')
            lines.append('    <div class="card" data-tags="' + ctype.capitalize() + '">')
            lines.append("      <hr>")
            lines.append('      <div class="center">')
            lines.append("        ### " + type_label)
            lines.append("      </div>")
            lines.append("      <hr>")
            lines.append("    </div>")
            lines.append("  </div><!--container Elements-->")
            lines.append("")
            lines.append('  <div class="container grid max-width">')
            
            prev_type = ctype
        
        lines.append(generate_card(cred))
    
    if prev_type is not None:
        lines.append("  </div><!--container Elements-->")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"Generated {output_file} with {len(creds)} credentials")
    return 0

def generate_card(c):
    ctype = c.get('type', 'certificate')
    issued = c.get('issuedOn', '')
    year = issued[:4] if issued else 'Unknown'
    
    skills_html = ""
    for s in c.get('skills', []):
        skills_html += '          <span class="credential-skill">' + s + '</span>\n'
    if len(c.get('skills', [])) > 0:
        skills_html += '          <span class="skills-more"></span>'
    
    link_html = ""
    link = c.get('link', '')
    if link:
        if link.endswith('.pdf') or link.startswith('./'):
            link_text = "((en))Verify((/en))((es))Verificar((/es)) PDF"
        else:
            link_text = "((en))Verify credential((/en))((es))Verificar credencial((/es))"
        link_html = '''
        <span class="credential-date">((en))Issued on: ''' + issued + '''((/en))((es))Fecha: ''' + issued + '''((/es))</span>
        [''' + link_text + '''](''' + link + '''){:target="_blank" class="credential-link"}'''
    
    image = c.get('image', '')
    if image:
        title = c.get('title', '')
        if '((en))' in title:
            en_match = re.search(r'\(\(en\)\)(.*?)\(\(/en\)\)', title)
            es_match = re.search(r'\(\(es\)\)(.*?)\(\(/es\)\)', title)
            if en_match and es_match:
                alt_text = '((en))' + en_match.group(1) + ' image((/en))((es))' + es_match.group(1) + ' imagen((/es))'
            else:
                alt_text = '((en))image((/en))((es))imagen((/es))'
        else:
            alt_text = title + ' ((en))image((/en))((es))imagen((/es))'
        image_html = '''
      <div class="credential-preview">
        ![loading="lazy" alt="''' + alt_text + '"](''' + image + ''')
      </div>'''
    else:
        image_html = ""
    
    desc_en = c.get('description', {}).get('en', '')
    desc_es = c.get('description', {}).get('es', '')
    
    issuer_en = c.get('issuer', '')
    issuer_text = '((en))Issuer: ' + issuer_en + '((/en))((es))Emitido por: ' + issuer_en + '((/es))'

    score = c.get('score', '')
    if score:
        if '((en))' in score or '((es))' in score:
            score_text = score
        else:
            score_text = '((en))' + score + '((/en))((es))' + score + '((/es))'
    else:
        score_text = ''
    
    card = '''    <div class="card" data-tags="''' + ctype + '''">
      <div class="credential-header">
        <div class="credential-title">
          <span class="title-main">''' + c.get('title', '') + '''</span>
          <span class="title-rank">''' + c.get('level', '') + '''</span>
          <span class="title-score">''' + score_text + '''</span>
        </div>
        <div class="credential-skills">
 ''' + skills_html + '''        </div>
      </div>''' + image_html + '''
      <div class="credential-meta">
        <span class="credential-issuer">''' + issuer_text + '''</span>''' + link_html + '''
      </div>
      <div class="credential-description justify">
        ((en))''' + desc_en + '''((/en))((es))''' + desc_es + '''((/es))
        <span class="see-more"></span>
      </div>
    </div>'''
    return card

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    
    command = sys.argv[1]
    args = {}
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg.startswith('--'):
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('-'):
                args[arg] = sys.argv[i + 1]
                i += 2
            else:
                args[arg] = ""
                i += 1
        elif arg.startswith('-') and len(arg) > 1:
            args[arg] = ""
            i += 1
        elif arg.isdigit():
            args['<id>'] = arg
            i += 1
        else:
            args['<id>'] = arg
            i += 1
    
    commands = {
        'add': cmd_add,
        'list': cmd_list,
        'get': cmd_get,
        'delete': cmd_delete,
        'sort': cmd_sort,
        'generate': cmd_generate,
    }
    
    if command not in commands:
        print(f"Unknown command: {command}")
        print(__doc__)
        return 1
    
    return commands[command](args)

if __name__ == '__main__':
    sys.exit(main())