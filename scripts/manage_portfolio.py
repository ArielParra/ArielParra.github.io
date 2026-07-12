#!/usr/bin/env python3
"""
Portfolio Management CLI
Usage:
  manage_portfolio.py generate    Generate portfolio/index.md from JSON
  manage_portfolio.py sort        Sort projects in JSON
  manage_portfolio.py list        List all projects
  manage_portfolio.py delete <id> Delete a project by ID
"""
import json
import sys
import re
from pathlib import Path

from base_manager import BaseManager
from i18n import format_date_i18n
PROJECTS_FILE = Path(__file__).resolve().parent.parent / \
    "portfolio" / "data" / "projects.json"
if not PROJECTS_FILE.exists():
    PROJECTS_FILE = Path(__file__).resolve(
    ).parent.parent / "data" / "projects.json"


class PortfolioManager(BaseManager):
    TECH_OPTIONS = [
        "c", "cpp", "java", "python", "javascript", "typescript",
        "html", "css", "sql", "dart", "ruby", "assembly",
        "flutter", "firebase", "spring", "flask", "jekyll",
        "raylib", "libpcap", "winapi", "llm",
        "algorithms", "networking", "browser-extension",
        "dos", "markdown"
    ]

    TECH_LABELS = {
        "c": "C",
        "cpp": "C++",
        "java": "Java",
        "python": "Python",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "html": "HTML",
        "css": "CSS",
        "sql": "SQL",
        "dart": "Dart",
        "ruby": "Ruby",
        "assembly": "Assembly",
        "flutter": "Flutter",
        "firebase": "Firebase",
        "spring": "Spring",
        "flask": "Flask",
        "jekyll": "Jekyll",
        "raylib": "Raylib",
        "libpcap": "Libpcap",
        "winapi": "WinAPI",
        "llm": "LLM",
        "algorithms": {"en": "Algorithms", "es": "Algoritmos"},
        "networking": {"en": "Networking", "es": "Redes"},
        "browser-extension": {"en": "Browser Extension", "es": "Extensión de Navegador"},
        "dos": "DOS",
        "markdown": "Markdown",
    }

    def __init__(self):
        super().__init__(file_path=PROJECTS_FILE, data_key="projects")

    def generate_id(self, title):
        return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    def get_tech_label(self, tech):
        """Return i18n tag string for a technology label."""
        label = self.TECH_LABELS.get(tech, tech)
        if isinstance(label, dict):
            en = label.get("en", tech)
            es = label.get("es", tech)
            return f"((en)){en}((/en))((es)){es}((/es))"
        return label

    def generate_project_card(self, p):
        """Generate markdown card HTML for a single project."""
        techs = p.get('technologies', [])
        data_tags = ' '.join(techs)

        # Tech tags HTML
        tech_tags_html = ""
        for t in techs:
            label = self.get_tech_label(t)
            tech_tags_html += f'          <span class="project-tech">{label}</span>\n'
        tech_tags_html += '          <span class="techs-more"></span>\n'

        # Image
        image = p.get('image', '')
        title = p.get('title', '')
        if image:
            image_html = f'''
      <div class="project-preview">
        ![loading="lazy" alt="{title}"]({image})
      </div>'''
        else:
            image_html = ""

        # Description
        desc_en = p.get('description', {}).get('en', '')
        desc_es = p.get('description', {}).get('es', '')

        # Date
        date_str = p.get('date', '')
        date_formatted = format_date_i18n(date_str)
        date_html = f'\n        <span class="project-date">{date_formatted}</span>' if date_formatted else ''

        # Link
        link = p.get('link', '')
        link_html = ""
        if link:
            link_html = f'\n        [((en))View Project((/en))((es))Ver Proyecto((/es))]({link}){{:target="_blank" class="project-link"}}'

        card = f"""    <div class="card" data-tags="{data_tags}">
      <div class="project-header">
        <span class="project-title">{title}</span>
      </div>
      <div class="project-techs">{tech_tags_html}</div>
      {image_html}
      <div class="project-meta">{date_html}{link_html}</div>
      <div class="project-description justify">
        <span class="desc-text">((en)){desc_en}((/en))((es)){desc_es}((/es))</span>
        <span class="see-more"></span>
      </div>
    </div>"""
        return card

    def cmd_generate(self, args):
        """Generate portfolio/index.md from JSON"""
        data = self.load_data()
        projects = data.get('projects', [])

        if not projects:
            print("No projects to generate.")
            return 0

        output_file = Path(__file__).resolve(
        ).parent.parent / "portfolio" / "index.md"

        # Collect all unique techs across all projects
        all_techs = []
        seen = set()
        for p in projects:
            for t in p.get('technologies', []):
                if t not in seen:
                    seen.add(t)
                    all_techs.append(t)

        lines = []

        # --- Frontmatter ---
        lines.append("---")
        lines.append("base_href: ../")
        lines.append(
            "keywords: [((en))Ariel Parra, portfolio((/en))((es))Ariel Parra, portafolio((/es))((fr))Ariel Parra, portefeuille((/fr))((pt))Ariel Parra, portfólio((/pt))]")
        lines.append(
            "description: ((en))Ariel Parra portfolio((/en))((es))Portafolio de Ariel Parra((/es))((fr))Portefeuille d'Ariel Parra((/fr))((pt))Portfólio de Ariel Parra((/pt))")
        lines.append("title: ((en))portfolio((/en))((es))portafolio((/es))((fr))portefeuille((/fr))((pt))portfólio((/pt))")
        lines.append(
            "js: [cookies, language, theme, menu, favicon, portfolio]")
        lines.append("css: [theme, common, portfolio]")
        lines.append("nav_current: 2")
        lines.append("---")
        lines.append("")
        lines.append(
            '<h1 class="sr-only">((en))Portfolio((/en))((es))Portafolio((/es))</h1>')
        lines.append("")

        # --- Build tech data JSON for autocomplete ---
        tech_data = []
        for tech in all_techs:
            label = self.TECH_LABELS.get(tech, tech)
            if isinstance(label, dict):
                tech_data.append({"value": tech, "en": label.get(
                    "en", tech), "es": label.get("es", tech)})
            else:
                tech_data.append({"value": tech, "en": label, "es": label})
        tech_data_json = json.dumps(tech_data, ensure_ascii=False)

        # --- Filter card ---
        lines.append('  <div class="container" style="position: relative; z-index: 10;">')
        lines.append('  <div class="card" id="filter-techs">')
        lines.append("  <hr>")
        lines.append('  <div class="center">')
        lines.append(
            "  ## ((en))Filter by Technology((/en))((es))Filtrar por Tecnología((/es))")
        lines.append(
            f'  <span id="tech-data" data-techs=\'{tech_data_json}\' style="display:none;"></span>')
        lines.append('  <div class="tech-search-wrapper">')
        lines.append('    <input type="text" id="tech-search" placeholder="Search technology..." data-placeholder-en="Search technology..." data-placeholder-es="Buscar tecnología..." data-placeholder-fr="Rechercher une technologie..." data-placeholder-pt="Pesquisar tecnologia..." autocomplete="off">')
        lines.append('    <div id="tech-suggestions"></div>')
        lines.append("  <hr>")
        lines.append("  </div>")
        lines.append('  <div id="selected-techs"></div>')
        lines.append("  </div>")
        lines.append("  </div>")
        lines.append("  </div>")
        lines.append("")

        # --- Project cards ---
        lines.append('  <div class="container grid max-width">')
        for p in projects:
            lines.append(self.generate_project_card(p))
        lines.append("  </div><!-- container grid -->")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Generated {output_file} with {len(projects)} projects")
        return 0

    def cmd_sort(self, args):
        data = self.load_data()
        projects = data.get('projects', [])

        if not projects:
            print("No projects to sort.")
            return 0

        # Sort by title first so that identical dates are ordered alphabetically
        sorted_by_title = sorted(
            projects, key=lambda p: p.get(
                'title', '').lower())

        # Then sort by date descending (newest first)
        sorted_projects = sorted(
            sorted_by_title, key=lambda p: p.get(
                'date', ''), reverse=True)

        data['projects'] = sorted_projects
        self.save_data(data)

        print(
            f"Sorted {len(sorted_projects)} projects by date (newest first).")
        return 0

    def cmd_list(self, args):
        data = self.load_data()
        projects = data.get('projects', [])

        if not projects:
            print("No projects found.")
            return 0

        print(f"\n{'=' * 60}")
        print(f"{'ID':<25} {'TITLE':<20} {'TECHS'}")
        print(f"{'=' * 60}")

        for p in projects:
            pid = p.get('id', '')
            title = p.get('title', '')
            techs = ', '.join(p.get('technologies', []))
            print(f"{pid:<25} {title:<20} {techs}")

        print(f"\nTotal: {len(projects)} project(s)")
        return 0

    def cmd_get(self, args):
        data = self.load_data()
        projects = data.get('projects', [])

        item_id = args.get('<id>')
        if not item_id:
            print("Usage: get <project-id>")
            return 1

        for p in projects:
            if p.get('id') == item_id:
                print(json.dumps(p, indent=2, ensure_ascii=False))
                return 0

        print(f"Project '{item_id}' not found.")
        return 1


if __name__ == '__main__':
    manager = PortfolioManager()
    sys.exit(manager.run())
