#!/usr/bin/env python3
"""
Credentials Management CLI
"""
import json
import sys
import re
from pathlib import Path

from base_manager import BaseManager
from utils.i18n import format_date_i18n, get_i18n_field, get_i18n_tags
from utils.cli import prompt_yesno

CREDENTIALS_FILE = Path(__file__).resolve(
).parent.parent / "data" / "credentials.json"
if not CREDENTIALS_FILE.exists():
    CREDENTIALS_FILE = Path(__file__).resolve(
    ).parent.parent / "credentials" / "data" / "credentials.json"


class CredentialsManager(BaseManager):
    CARD_TYPES = [
        "certification",
        "certificate",
        "badge",
        "award",
        "education"]
    TYPE_PRIORITY = {
        "education": 4,
        "certification": 3,
        "certificate": 2,
        "badge": 1,
        "award": 0}
    TOPIC_OPTIONS = [
        "ai",
        "blockchain",
        "cloud",
        "cybersecurity",
        "data-science",
        "database",
        "devops",
        "finance",
        "languages",
        "networking",
        "professional",
        "programming"]

    def __init__(self):
        super().__init__(file_path=CREDENTIALS_FILE, data_key="credentials")

    def generate_id(self, title, issued_on):
        clean = re.sub(r'[^a-zA-Z0-9]', '', title.lower().replace(' ', '-'))
        date_part = issued_on.replace('-', '')[:4] if issued_on else "unknown"
        return f"{clean}-{date_part}"

    def prompt_credit_type(self):
        print("\nCredential type (choose from):")
        for i, t in enumerate(self.CARD_TYPES, 1):
            print(f"  {i}) {t}")
        while True:
            choice = input("Type [1]: ").strip()
            if not choice:
                return self.CARD_TYPES[0]
            if choice.isdigit() and 1 <= int(choice) <= len(self.CARD_TYPES):
                return self.CARD_TYPES[int(choice) - 1]
            if choice in self.CARD_TYPES:
                return choice
            print("Invalid. Choose a number or type name.")

    def prompt_topics(self):
        print("\nTopics (comma-separated, choose from):")
        for i, t in enumerate(self.TOPIC_OPTIONS, 1):
            print(f"  {i}) {t}")
        while True:
            inp = input("Topics []: ").strip()
            if not inp:
                return []
            topics = []
            for part in inp.split(','):
                part = part.strip()
                if part.isdigit() and 1 <= int(part) <= len(self.TOPIC_OPTIONS):
                    topics.append(self.TOPIC_OPTIONS[int(part) - 1])
                elif part.lower() in self.TOPIC_OPTIONS:
                    topics.append(part.lower())
                else:
                    topics.append(part)
            return list(set(topics))

    def prompt_skills(self):
        print("\nSkills (comma-separated, free text):")
        while True:
            inp = input("Skills []: ").strip()
            if not inp:
                return []
            return [s.strip() for s in inp.split(',') if s.strip()]

    def cmd_add(self, args):
        data = self.load_data()
        print("\n=== Add New Credential ===")

        title_en = input("Title (English): ").strip()
        if not title_en:
            print("Title required.")
            return 1
        title_es = input("Title (Spanish): ").strip()
        if not title_es:
            title_es = title_en

        ctype = self.prompt_credit_type()
        issuer = input("Issuer: ").strip()

        level_en = input("Level/Rank (English): ").strip()
        level_es = input("Level/Rank (Spanish): ").strip()

        score = input("Score (optional): ").strip()
        started_on = ""
        if ctype == "education":
            started_on = input("Started on (YYYY-MM or YYYY-MM-DD): ").strip()
            if started_on and not re.match(r'^\d{4}-\d{2}(-\d{2})?$', started_on):
                print("Format: YYYY-MM or YYYY-MM-DD (e.g., 2022-08)")
                return 1
        issued_on = input("Issued on (YYYY-MM or YYYY-MM-DD): ").strip()
        if issued_on:
            if not re.match(r'^\d{4}-\d{2}(-\d{2})?$', issued_on):
                print("Format: YYYY-MM or YYYY-MM-DD (e.g., 2025-01 or 2025-01-15)")
                return 1

        topics = self.prompt_topics()
        print("\nSkills (comma-separated):")
        skills_en = input("  English: ").strip()
        skills_es = input("  Spanish: ").strip()

        image = input("Image path (e.g., ./credentials/img/...): ").strip()
        if not image:
            if ctype in ("certification", "certificate"):
                safe_title = re.sub(r'[^a-zA-Z0-9]', '_', title_en)
                image = f"./credentials/img/{safe_title}.png"
            else:
                image = ""

        link = input("Verify URL (or local PDF path): ").strip()

        print("\n--- Description ---")
        desc_en = input("English description: ").strip()
        desc_es = input("Spanish description: ").strip()

        cred_id = args.get('<id>') or input("ID [auto-generated]: ").strip()
        if not cred_id:
            cred_id = self.generate_id(title_en, issued_on)

        new_cred = {
            "id": cred_id,
            "type": ctype,
            "issuer": issuer,
            "title": {"en": title_en, "es": title_es},
            "level": {"en": level_en, "es": level_es} if level_en else "",
            "score": score,
            "startedOn": started_on,
            "issuedOn": issued_on,
            "expiresOn": "",
            "topics": topics,
            "skills": [{"en": e.strip(), "es": s.strip() if i < len(skills_es.split(',')) and skills_es else e.strip()} for i, (e, s) in enumerate(zip(skills_en.split(','), (skills_es.split(',') if skills_es else skills_en.split(','))))] if skills_en else [],
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
                if prompt_yesno(
                        f"Credential '{cred_id}' exists. Overwrite?"):
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
        self.save_data(data)
        return 0

    def cmd_list(self, args):
        data = self.load_data()
        creds = data.get('credentials', [])

        if not creds:
            print("No credentials found.")
            return 0

        sort_by = args.get('--sort', 'type')
        reverse = not args.get('--asc')

        if sort_by == 'year' or sort_by == 'date':
            creds = sorted(
                creds, key=lambda c: c.get(
                    'issuedOn', ''), reverse=reverse)
        elif sort_by == 'type':
            def sort_key(c):
                ctype = c.get('type', 'certificate')
                type_order = self.TYPE_PRIORITY.get(ctype, 99)
                issued = c.get('issuedOn', '')
                return (type_order, issued if reverse else '')
            creds = sorted(creds, key=sort_key, reverse=reverse)
        elif sort_by == 'issuer':
            creds = sorted(
                creds,
                key=lambda c: c.get(
                    'issuer',
                    '').lower(),
                reverse=reverse)

        filter_type = args.get('--type')
        if filter_type:
            creds = [c for c in creds if c.get('type') == filter_type]

        filter_topic = args.get('--topic')
        if filter_topic:
            creds = [c for c in creds if filter_topic in c.get('topics', [])]

        limit = args.get('--limit')
        if limit and limit.isdigit():
            creds = creds[:int(limit)]

        print(f"\n{'=' * 60}")
        print(f"{'ID':<30} {'TYPE':<14} {'ISSUED':<10}")
        print(f"{'=' * 60}")

        for c in creds:
            cid = c.get('id', '')
            ctype = c.get('type', '')
            issued = c.get('issuedOn', '')
            title = get_i18n_field(c.get('title', ''), 'en')
            print(f"{cid:<30} {ctype:<14} {issued:<10}")
            print(f"  {title}")

        print(f"\nTotal: {len(creds)} credential(s)")
        return 0

    def cmd_get(self, args):
        data = self.load_data()
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

    def cmd_sort(self, args):
        data = self.load_data()
        creds = data.get('credentials', [])

        if not creds:
            print("No credentials to sort.")
            return 0

        order = args.get('--order', 'desc')
        reverse = (order == 'desc')

        def sort_key(c):
            ctype = c.get('type', 'certificate')
            type_order = self.TYPE_PRIORITY.get(ctype, 99)
            issued = c.get('issuedOn', '')
            return (type_order, issued if reverse else '')

        sorted_creds = sorted(creds, key=sort_key, reverse=reverse)
        data['credentials'] = sorted_creds
        self.save_data(data)

        order_text = "newest first" if reverse else "oldest first"
        print(
            f"Sorted by type then date ({order_text}): {
                len(sorted_creds)} credentials.")
        return 0

    def generate_card(self, c):
        ctype = c.get('type', 'certificate')
        issued = c.get('issuedOn', '')

        skills_html = ""
        for s in c.get('skills', []):
            skill_text = get_i18n_tags(s)
            if skill_text:
                skills_html += f'          <span class="credential-skill">{skill_text}</span>\n'
        if len(c.get('skills', [])) > 0:
            skills_html += '          <span class="skills-more"></span>'

        link_html = ""
        link = c.get('link', '')
        issued_formatted = format_date_i18n(issued)
        started = c.get('startedOn', '')
        if ctype == 'education' and started:
            started_formatted = format_date_i18n(started)
            date_range = f"{started_formatted} – {issued_formatted}"
        else:
            date_range = issued_formatted
        if link:
            if link.endswith('.pdf') or link.startswith('./'):
                link_text = "((en))Verify((/en))((es))Verificar((/es)) PDF"
            else:
                link_text = "((en))Verify credential((/en))((es))Verificar credencial((/es))"
            link_html = f'''
        <span class="credential-date">{date_range}</span>
        [{link_text}]({link}){{:target="_blank" class="credential-link"}}'''

        image = c.get('image', '')
        title_en = get_i18n_field(c.get('title', ''), 'en')
        title_es = get_i18n_field(c.get('title', ''), 'es')
        if image:
            alt_text = f"((en)){title_en} image((/en))((es)){title_es} imagen((/es))"
            image_html = f'''
      <div class="credential-preview">
        ![loading="lazy" alt="{alt_text}"]({image})
      </div>'''
        else:
            image_html = ""

        desc_en = c.get('description', {}).get('en', '')
        desc_es = c.get('description', {}).get('es', '')

        issuer_en = c.get('issuer', '')
        issuer_text = f"((en))Issuer: {issuer_en}((/en))((es))Emitido por: {issuer_en}((/es))"

        score = c.get('score', '')
        if score:
            if isinstance(score, dict):
                score_en = score.get('en', '')
                score_es = score.get('es', '')
                score_text = f"((en)){score_en}((/en))((es)){score_es}((/es))"
            else:
                score_text = f"((en)){score}((/en))((es)){score}((/es))"
        else:
            score_text = ''

        level_en = get_i18n_field(c.get('level', ''), 'en')
        level_es = get_i18n_field(c.get('level', ''), 'es')
        level = f"((en)){level_en}((/en))((es)){level_es}((/es))" if level_en or level_es else ""
        title = f"((en)){title_en}((/en))((es)){title_es}((/es))" if title_en or title_es else title_en

        topics = c.get('topics', [])
        data_tags = f"{ctype} {' '.join(topics)}" if topics else ctype

        return f'''    <div class="card" data-tags="{data_tags.strip()}">
      <div class="credential-header">
        <div class="credential-title">
          <span class="title-main">{title}</span>
          <span class="title-rank">{level}</span>
          <span class="title-score">{score_text}</span>
        </div>
        <div class="credential-skills">
{skills_html}        </div>
      </div>{image_html}
      <div class="credential-meta">
        <span class="credential-issuer">{issuer_text}</span>{link_html}
      </div>
      <div class="credential-description justify">
        ((en)){desc_en}((/en))((es)){desc_es}((/es))
        <span class="see-more"></span>
      </div>
    </div>'''

    def cmd_generate(self, args):
        """Generate credentials/index.md from JSON"""
        data = self.load_data()
        creds = data.get('credentials', [])

        if not creds:
            print("No credentials to generate.")
            return 0

        output_file = Path(__file__).resolve(
        ).parent.parent / "credentials" / "index.md"

        TYPE_LABELS = {
            "education": (
                "((en))Education((/en))((es))Educación((/es))",
                "((en))Academic background and degrees.((/en))((es))Antecedentes académicos y títulos.((/es))"),
            "certification": (
                "((en))Certifications((/en))((es))Certificaciones((/es))",
                "((en))Proctored exam-based credentials.((/en))((es))Acreditaciones basadas en exámenes.((/es))"),
            "certificate": (
                "((en))Certificates((/en))((es))Certificados((/es))",
                "((en))Course completion certificates.((/en))((es))Certificados de finalización.((/es))"),
            "badge": (
                "((en))Badges((/en))((es))Insignias((/es))",
                "((en))Micro-credentials.((/en))((es))Micro-acreditaciones.((/es))"),
            "award": (
                "((en))Awards and Honors((/en))((es))Premios y Reconocimientos((/es))",
                "((en))Honors and contest wins.((/en))((es))Honores y premios.((/es))"),
        }

        lines = []

        lines.append("---")
        lines.append("lang: en")
        lines.append("base_href: ../")
        lines.append(
            "keywords: [Ariel Parra, certifications, certificates, badges, achievements, degree, diploma]")
        lines.append("description: Ariel Parra multiple achievements")
        lines.append(
            "title: ((en))achievements((/en))((es))acreditaciones((/es))")
        lines.append(
            "js: [cookies, language, theme, menu, favicon, tags, credentials]")
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

                type_info = TYPE_LABELS.get(ctype, (ctype.capitalize(), ""))
                type_label, type_desc = type_info

                lines.append('  <div class="container">')
                lines.append('  <div class="card" data-tags="' + ctype + '">')
                lines.append(" <hr>")
                lines.append(' <div class="center">')
                lines.append(
                    " ### " +
                    type_label +
                    ' <span class="section-count" data-type="' +
                    ctype +
                    '">0</span>')
                if type_desc:
                    lines.append(
                        ' <div class="credential-description center">')
                    lines.append(type_desc)
                    lines.append(' </div>')
                lines.append(" </div>")
                lines.append(" <hr>")
                lines.append(" </div>")
                lines.append(" </div><!--container Elements-->")
                lines.append("")
                lines.append('  <div class="container grid max-width">')

                prev_type = ctype

            lines.append(self.generate_card(cred))

        if prev_type is not None:
            lines.append("  </div><!--container Elements-->")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Generated {output_file} with {len(creds)} credentials")
        return 0


if __name__ == '__main__':
    manager = CredentialsManager()
    sys.exit(manager.run())
