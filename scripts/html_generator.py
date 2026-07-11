import html
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

    nav_items = [{"href": home_path,
                  "title": "Home Page",
                  "label": '<span class="i18n" data-i18n-en="~/" data-i18n-es="~/">~/</span>'},
                 {"href": portfolio_path,
                  "title": "",
                  "label": '<span class="i18n" data-i18n-en="portfolio" data-i18n-es="portafolio">portfolio</span>'},
                 {"href": credentials_path,
                  "title": "",
                  "label": '<span class="i18n" data-i18n-en="credentials" data-i18n-es="acreditaciones">credentials</span>'},
                 {"href": contact_path,
                  "title": "",
                  "label": '<span class="i18n" data-i18n-en="contact" data-i18n-es="contacto">contact</span>'},
                 ]

    nav_current = int(md_dict['nav_current'])

    csp = "default-src 'self'; script-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;"

    html_content = f"""<!DOCTYPE html>
<html lang="{language}" data-i18n-title-en="{html.escape(title_en)}" data-i18n-title-es="{html.escape(title_es)}">

<head>
  <base href="{md_dict['base_href']}">
  <link rel="manifest" href="./manifest.json">
  <!--fonts-->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400..700&display=swap" rel="stylesheet">
  <!--metadatas-->
  <meta   charset="UTF-8">
  <meta   name="viewport"        content="width=device-width, initial-scale=1">
  <meta   http-equiv="Content-Security-Policy" content="{csp}">
  <meta   name="keywords"        data-i18n-keywords-en="{html.escape(keys_en)}" data-i18n-keywords-es="{html.escape(keys_es)}" content="{html.escape(extract_translation(keys_raw, language))}">
  <meta   name="description"     data-i18n-description-en="{html.escape(desc_en)}" data-i18n-description-es="{html.escape(desc_es)}" content="{html.escape(extract_translation(md_dict['description'], language))}">
  <meta   name="author"          content="Ariel Parra">
  <title> {extract_translation(md_dict['title'], language)} </title>
"""

    def space_padding(css_file):
        return " " * (max(len(cf) for cf in md_dict['css']) - len(css_file))

    html_content += '  <!-- CSS files -->\n'
    for css_file in md_dict['css']:
        if css_file:
            html_content += f'  <link   rel="stylesheet"       href="./css/{css_file}.css" {space_padding(css_file)}>\n'

    def space_padding_js(js_file):
        return " " * (max(len(jf) for jf in md_dict['js']) - len(js_file))

    html_content += '  <!-- Java Scripts preloads -->\n'
    for js_file in md_dict['js']:
        if js_file:
            html_content += f'  <link   rel="preload"          href="./js/{js_file}.js" {space_padding_js(js_file)}as="script">\n'

    html_content += '  <!-- Java Scripts defers -->\n'
    for js_file in md_dict['js']:
        if js_file == "main":
            html_content += f'  <script defer                  src ="./{js_file}.js">    {space_padding_js(js_file)}</script>\n'
        else:
            html_content += f'  <script defer                  src ="./js/{js_file}.js"> {space_padding_js(js_file)}</script>\n'

    html_content += """  <!-- Favicons -->
  <link   rel="apple-touch-icon" href="./img/apple-touch-icon.png" sizes="180x180">
</head>

<body>
"""
    nav_button_text = '<span class="i18n" data-i18n-en="Hide Menu" data-i18n-es="Mostrar Menú">Hide Menu</span>'
    lang_button_text = '<span class="i18n" data-i18n-en="Español" data-i18n-es="English">Español</span>'
    lang_button_title_en = "Change language to"
    lang_button_title_es = "Cambiar idioma a"
    theme_button_title_en = "Change color theme to"
    theme_button_title_es = "Cambiar tema de color a"

    html_content += f"""
  <div class="container">
    <button type="button" id="menuButton"   data-nav-shown="true" aria-label="Toggle menu">{nav_button_text}</button>
    <button type="button" id="langButton"  data-i18n-title-en="{lang_button_title_en}" data-i18n-title-es="{lang_button_title_es}" title="{lang_button_title_en}" aria-label="Toggle language">{lang_button_text}</button>
    <button type="button" id="themeButton" data-i18n-title-en="{theme_button_title_en}" data-i18n-title-es="{theme_button_title_es}" title="{theme_button_title_en}" aria-label="Toggle theme"> 🌗 </button>
  </div><!-- Buttons -->

  <nav>
"""
    max_href_length = max(len(item["href"]) for item in nav_items)
    max_class_length = max(len("current"), len("NotCurrent"))
    max_title_length = max(len(item["title"]) for item in nav_items)
    max_label_length = max(len(item["label"]) for item in nav_items)

    for idx, item in enumerate(nav_items, start=1):
        class_name = "current" if idx == nav_current else "NotCurrent"
        html_content += (f'    <a href="{item["href"]}"' +
                         " " *
                         (max_href_length -
                          len(item["href"])) +
                         f' class="{class_name}"' +
                         " " *
                         (max_class_length -
                          len(class_name)) +
                         f' title="{item["title"]}' +
                         " " *
                         (max_title_length -
                          len(item["title"])) +
                         f'"> <span>{item["label"]}' +
                         " " *
                         (max_label_length -
                          len(item["label"])) +
                         '</span></a>\n')

    html_content += """  </nav>
"""

    if nav_current == 3:
        type_tag_text_value = [
            "all",
            "education",
            "certification",
            "certificate",
            "badge",
            "award"]
        topic_tag_text_value = [
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
        search_text = '<span class="i18n" data-i18n-en="Search" data-i18n-es="Buscar">Search</span>'
        filterType_text = '<span class="i18n" data-i18n-en="Filter by type" data-i18n-es="Filtrado por tipo">Filter by type</span>'
        filterTopic_text = '<span class="i18n" data-i18n-en="Filter by topic" data-i18n-es="Filtrado por tema">Filter by topic</span>'
        stats_text = '<span class="i18n" data-i18n-en="Stats" data-i18n-es="Estadísticas">Stats</span>'
        reset_text = '<span class="i18n" data-i18n-en="↺ Clear filters" data-i18n-es="↺ Limpiar filtros">↺ Clear filters</span>'
        type_tag_text = [
            '<span class="i18n" data-i18n-en="All" data-i18n-es="Todos">All</span>',
            '<span class="i18n" data-i18n-en="Education" data-i18n-es="Educación">Education</span>',
            '<span class="i18n" data-i18n-en="Certifications" data-i18n-es="Certificaciones">Certifications</span>',
            '<span class="i18n" data-i18n-en="Certificates" data-i18n-es="Certificados">Certificates</span>',
            '<span class="i18n" data-i18n-en="Badges" data-i18n-es="Insignias">Badges</span>',
            '<span class="i18n" data-i18n-en="Awards" data-i18n-es="Premios">Awards</span>']
        topic_tag_text = [
            '<span class="i18n" data-i18n-en="AI" data-i18n-es="IA">AI</span>',
            '<span class="i18n" data-i18n-en="Blockchain" data-i18n-es="Blockchain">Blockchain</span>',
            '<span class="i18n" data-i18n-en="Cloud" data-i18n-es="Nube">Cloud</span>',
            '<span class="i18n" data-i18n-en="Cybersecurity" data-i18n-es="Ciberseguridad">Cybersecurity</span>',
            '<span class="i18n" data-i18n-en="Data Science" data-i18n-es="Ciencia de Datos">Data Science</span>',
            '<span class="i18n" data-i18n-en="Database" data-i18n-es="Base de datos">Database</span>',
            '<span class="i18n" data-i18n-en="DevOps" data-i18n-es="DevOps">DevOps</span>',
            '<span class="i18n" data-i18n-en="Finance" data-i18n-es="Finanzas">Finance</span>',
            '<span class="i18n" data-i18n-en="Languages" data-i18n-es="Idiomas">Languages</span>',
            '<span class="i18n" data-i18n-en="Networking" data-i18n-es="Redes">Networking</span>',
            '<span class="i18n" data-i18n-en="Professional" data-i18n-es="Profesional">Professional</span>',
            '<span class="i18n" data-i18n-en="Programming" data-i18n-es="Programación">Programming</span>']

        html_content += f"""
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
            tag_text = type_tag_text[idx] if idx < len(
                type_tag_text) else tag_value.capitalize()
            html_content += f"""          <label><input type="radio" name="type" value="{tag_value}" {
                'checked' if idx == 0 else ''}> {tag_text} </label>\n"""

        html_content += f"""        </div>
        <hr>
        <div class="center">
            <h4>{filterTopic_text}</h4>
        </div>
        <hr>
        <div class="center row">
"""
        for idx, tag_value in enumerate(topic_tag_text_value):
            tag_text = topic_tag_text[idx] if idx < len(
                topic_tag_text) else tag_value.capitalize()
            html_content += f"""          <label><input type="checkbox" name="topic" value="{tag_value}"> {tag_text} </label>\n"""

        html_content += f"""        </div>
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

    html_content += md_to_html(md_content, language)

    html_content += """
</body>
</html>"""
    return html_content
