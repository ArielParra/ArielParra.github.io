import html
import os
from md_parser import get_translations, extract_translation, md_to_html


def generate_html(md_dict, md_content):
    language = md_dict.get('lang', 'en')
    portfolio_path = "./portfolio/"
    credentials_path = "./credentials/"
    contact_path = "./contact/"
    home_path = "./"

    title_en, title_es = get_translations(md_dict['title'])
    desc_en, desc_es = get_translations(md_dict['description'])
    keys_raw = ', '.join(md_dict['keywords'])
    keys_en, keys_es = get_translations(keys_raw)

    title_content = extract_translation(md_dict['title'], language)
    keys_content = extract_translation(keys_raw, language)
    desc_content = extract_translation(md_dict['description'], language)

    nav_items = [{"href": home_path,
                  "title": "Home Page",
                  "label": '<span class="i18n" data-i18n-en="~/" data-i18n-es="~/">~/</span>'},
                 {"href": portfolio_path,
                  "title": "Portfolio Page",
                  "label": '<span class="i18n" data-i18n-en="portfolio" data-i18n-es="portafolio">portfolio</span>'},
                 {"href": credentials_path,
                  "title": "Credentials Page",
                  "label": '<span class="i18n" data-i18n-en="credentials" data-i18n-es="acreditaciones">credentials</span>'},
                 {"href": contact_path,
                  "title": "Contact Page",
                  "label": '<span class="i18n" data-i18n-en="contact" data-i18n-es="contacto">contact</span>'},
                 ]

    nav_current = int(md_dict['nav_current'])
    csp = "default-src 'self'; script-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;"

    def space_padding(css_file):
        return " " * (max(len(cf) for cf in md_dict['css']) - len(css_file))

    css_links = ""
    for css_file in md_dict['css']:
        if css_file:
            css_links += f'  <link rel="stylesheet" href="./css/{css_file}.css" {space_padding(css_file)}>\n'

    def space_padding_js(js_file):
        return " " * (max(len(jf) for jf in md_dict['js']) - len(js_file))

    js_preloads = ""
    for js_file in md_dict['js']:
        if js_file:
            js_preloads += f'  <link rel="preload" href="./js/{js_file}.js" {space_padding_js(js_file)}as="script">\n'

    js_defers = ""
    for js_file in md_dict['js']:
        if js_file == "main":
            js_defers += f'  <script defer src="./{js_file}.js">    {space_padding_js(js_file)}</script>\n'
        else:
            js_defers += f'  <script defer src="./js/{js_file}.js"> {space_padding_js(js_file)}</script>\n'

    max_href_length = max(len(item["href"]) for item in nav_items)
    max_class_length = max(len("current"), len("NotCurrent"))
    max_label_length = max(len(item["label"]) for item in nav_items)

    nav_html = ""
    for idx, item in enumerate(nav_items, start=1):
        class_name = "current" if idx == nav_current else "NotCurrent"
        nav_html += (f'    <a href="{item["href"]}"' +
                     " " * (max_href_length - len(item["href"])) +
                     f' class="{class_name}"' +
                     " " * (max_class_length - len(class_name)) +
                     f' title="{item["title"]}"> <span>{item["label"]}' +
                     " " * (max_label_length - len(item["label"])) +
                     '</span></a>\n')

    credentials_filters = ""
    if nav_current == 3:
        type_tag_text_value = ["all", "education", "certification", "certificate", "badge", "award"]
        topic_tag_text_value = ["ai", "blockchain", "cloud", "cybersecurity", "data-science", "database", "devops", "finance", "languages", "networking", "professional", "programming"]
        search_text = '<span class="i18n" data-i18n-en="Search" data-i18n-es="Buscar">Search</span>'
        filterType_text = '<span class="i18n" data-i18n-en="Filter by type" data-i18n-es="Filtrado por tipo">Filter by type</span>'
        filterTopic_text = '<span class="i18n" data-i18n-en="Filter by topic" data-i18n-es="Filtrado por tema">Filter by topic</span>'
        stats_text = '<span class="i18n" data-i18n-en="Stats" data-i18n-es="Estadísticas">Stats</span>'
        reset_text = '<span class="i18n" data-i18n-en="↺ Clear filters" data-i18n-es="↺ Limpiar filtros">↺ Clear filters</span>'
        type_tag_text = ['<span class="i18n" data-i18n-en="All" data-i18n-es="Todos">All</span>', '<span class="i18n" data-i18n-en="Education" data-i18n-es="Educación">Education</span>', '<span class="i18n" data-i18n-en="Certifications" data-i18n-es="Certificaciones">Certifications</span>', '<span class="i18n" data-i18n-en="Certificates" data-i18n-es="Certificados">Certificates</span>', '<span class="i18n" data-i18n-en="Badges" data-i18n-es="Insignias">Badges</span>', '<span class="i18n" data-i18n-en="Awards" data-i18n-es="Premios">Awards</span>']
        topic_tag_text = ['<span class="i18n" data-i18n-en="AI" data-i18n-es="IA">AI</span>', '<span class="i18n" data-i18n-en="Blockchain" data-i18n-es="Blockchain">Blockchain</span>', '<span class="i18n" data-i18n-en="Cloud" data-i18n-es="Nube">Cloud</span>', '<span class="i18n" data-i18n-en="Cybersecurity" data-i18n-es="Ciberseguridad">Cybersecurity</span>', '<span class="i18n" data-i18n-en="Data Science" data-i18n-es="Ciencia de Datos">Data Science</span>', '<span class="i18n" data-i18n-en="Database" data-i18n-es="Base de datos">Database</span>', '<span class="i18n" data-i18n-en="DevOps" data-i18n-es="DevOps">DevOps</span>', '<span class="i18n" data-i18n-en="Finance" data-i18n-es="Finanzas">Finance</span>', '<span class="i18n" data-i18n-en="Languages" data-i18n-es="Idiomas">Languages</span>', '<span class="i18n" data-i18n-en="Networking" data-i18n-es="Redes">Networking</span>', '<span class="i18n" data-i18n-en="Professional" data-i18n-es="Profesional">Professional</span>', '<span class="i18n" data-i18n-en="Programming" data-i18n-es="Programación">Programming</span>']

        credentials_filters += f"""
<div class="container max-width">
    <div class="card max-width" id="filter-checks">
        <hr>
        <div class="center">
            <h4><label for="f-search">{search_text}</label></h4>
        </div>
        <hr>
        <div class="center">
            <input type="text" id="f-search" name="search"
                   data-i18n-placeholder-en="Title, issuer or description…"
                   data-i18n-placeholder-es="Título, emisor o descripción…"
                   placeholder="Title, issuer or description…"
                   autocomplete="off" aria-label="Search credentials">
        </div>
        <hr>
        <div class="center">
            <h4>{filterType_text}</h4>
        </div>
        <hr>
        <div class="center row">
"""
        for idx, tag_value in enumerate(type_tag_text_value):
            tag_text = type_tag_text[idx] if idx < len(type_tag_text) else tag_value.capitalize()
            checked = 'checked' if idx == 0 else ''
            credentials_filters += f"""          <label><input type="radio" name="type" value="{tag_value}" {checked}> {tag_text} </label>\n"""

        credentials_filters += f"""        </div>
        <hr>
        <div class="center">
            <h4>{filterTopic_text}</h4>
        </div>
        <hr>
        <div class="center row">
"""
        for idx, tag_value in enumerate(topic_tag_text_value):
            tag_text = topic_tag_text[idx] if idx < len(topic_tag_text) else tag_value.capitalize()
            credentials_filters += f"""          <label><input type="checkbox" name="topic" value="{tag_value}"> {tag_text} </label>\n"""

        credentials_filters += f"""        </div>
        <hr>
        <div class="center">
            <h4>{stats_text}</h4>
        </div>
        <hr>
        <div class="center">
            <span class="credential-counts" aria-live="polite">
                <span class="stat-item" data-type="education"><span class="stat-label i18n" data-i18n-en="Education" data-i18n-es="Educación">Education</span>: <span class="stat-count" data-type="education">0</span></span>
                <span class="stat-item" data-type="certification"><span class="stat-label i18n" data-i18n-en="Certifications" data-i18n-es="Certificaciones">Certifications</span>: <span class="stat-count" data-type="certification">0</span></span>
                <span class="stat-item" data-type="certificate"><span class="stat-label i18n" data-i18n-en="Certificates" data-i18n-es="Certificados">Certificates</span>: <span class="stat-count" data-type="certificate">0</span></span>
                <span class="stat-item" data-type="badge"><span class="stat-label i18n" data-i18n-en="Badges" data-i18n-es="Insignias">Badges</span>: <span class="stat-count" data-type="badge">0</span></span>
                <span class="stat-item" data-type="award"><span class="stat-label i18n" data-i18n-en="Awards" data-i18n-es="Premios">Awards</span>: <span class="stat-count" data-type="award">0</span></span>
                <span class="stat-item total"><span class="stat-label">Total:</span> <span class="stat-count" id="global-total-credentials">0</span></span>
            </span>
        </div>
        <hr>
        <div class="center">
            <button type="button" id="reset-btn" class="credential-link">{reset_text}</button>
        </div>
    </div><!--filters card-->
</div><!--filters container-->
"""

    main_content = md_to_html(md_content, language)

    # Read the template from templates/base.html
    template_path = os.path.join(os.path.dirname(__file__), "..", "templates", "base.html")
    with open(template_path, 'r', encoding='utf-8') as f:
        html_template = f.read()

    # Apply variables
    replacements = {
        "language": language,
        "title_en": html.escape(title_en),
        "title_es": html.escape(title_es),
        "base_href": md_dict['base_href'],
        "csp": csp,
        "keys_en": html.escape(keys_en),
        "keys_es": html.escape(keys_es),
        "keys_content": html.escape(keys_content),
        "desc_en": html.escape(desc_en),
        "desc_es": html.escape(desc_es),
        "desc_content": html.escape(desc_content),
        "title_content": html.escape(title_content),
        "css_links": css_links.rstrip('\n'),
        "js_preloads": js_preloads.rstrip('\n'),
        "js_defers": js_defers.rstrip('\n'),
        "nav_html": nav_html.rstrip('\n'),
        "credentials_filters": credentials_filters,
        "main_content": main_content
    }

    for key, val in replacements.items():
        html_template = html_template.replace(f"{{{{ {key} }}}}", str(val))

    return html_template
