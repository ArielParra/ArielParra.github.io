#!/usr/bin/env python3
"""
Credentials Management CLI
"""
import json
import sys
import re
from pathlib import Path

from base_manager import BaseManager
from i18n import format_date_i18n, get_i18n_field, get_i18n_tags

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
        <span class="desc-text">((en)){desc_en}((/en))((es)){desc_es}((/es))</span>
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
                "((en))Education((/en))((es))Educación((/es))((fr))Éducation((/fr))((pt))Educação((/pt))",
                "((en))Academic background and degrees.((/en))((es))Antecedentes académicos y títulos.((/es))((fr))Parcours académique et diplômes.((/fr))((pt))Formação acadêmica e diplomas.((/pt))"),
            "certification": (
                "((en))Certifications((/en))((es))Certificaciones((/es))((fr))Certifications((/fr))((pt))Certificações((/pt))",
                "((en))Proctored exam-based credentials.((/en))((es))Acreditaciones basadas en exámenes.((/es))((fr))Diplômes basés sur des examens.((/fr))((pt))Credenciais baseadas em exames.((/pt))"),
            "certificate": (
                "((en))Certificates((/en))((es))Certificados((/es))((fr))Certificats((/fr))((pt))Certificados((/pt))",
                "((en))Course completion certificates.((/en))((es))Certificados de finalización.((/es))((fr))Certificats de fin de cours.((/fr))((pt))Certificados de conclusão de curso.((/pt))"),
            "badge": (
                "((en))Badges((/en))((es))Insignias((/es))((fr))Badges((/fr))((pt))Emblemas((/pt))",
                "((en))Micro-credentials.((/en))((es))Micro-acreditaciones.((/es))((fr))Micro-certifications.((/fr))((pt))Microcredenciais.((/pt))"),
            "award": (
                "((en))Awards and Honors((/en))((es))Premios y Reconocimientos((/es))((fr))Prix et Distinctions((/fr))((pt))Prêmios e Honrarias((/pt))",
                "((en))Honors and contest wins.((/en))((es))Honores y premios.((/es))((fr))Honneurs et prix.((/fr))((pt))Honrarias e prêmios.((/pt))"),
        }

        lines = []

        lines.append("---")
        lines.append("lang: en")
        lines.append("base_href: ../")
        lines.append(
            "keywords: [((en))Ariel Parra, certifications, certificates, badges, achievements, degree, diploma((/en))((es))Ariel Parra, certificaciones, certificados, insignias, logros, título, diploma((/es))((fr))Ariel Parra, certifications, certificats, badges, réalisations, diplôme((/fr))((pt))Ariel Parra, certificações, certificados, emblemas, conquistas, diploma((/pt))]")
        lines.append("description: ((en))Ariel Parra multiple achievements((/en))((es))Logros múltiples de Ariel Parra((/es))((fr))Réalisations multiples d'Ariel Parra((/fr))((pt))Múltiplas conquistas de Ariel Parra((/pt))")
        lines.append(
            "title: ((en))achievements((/en))((es))acreditaciones((/es))((fr))réalisations((/fr))((pt))conquistas((/pt))")
        lines.append(
            "js: [cookies, language, theme, menu, favicon, tags, credentials]")
        lines.append("css: [theme, common, credentials]")
        lines.append("nav_current: 3")
        lines.append("---")
        lines.append("")
        lines.append(
            '<h1 class="sr-only">((en))Credentials((/en))((es))Acreditaciones((/es))</h1>')
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
                    " ## " +
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
