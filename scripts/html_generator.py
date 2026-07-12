import html
import os
from md_parser import extract_translation, md_to_html


def generate_html(md_dict, md_content, language='en'):
    # base_href adjustment for nested language folders
    base_href_original = md_dict.get('base_href', './')
    if language == 'en':
        base_href = base_href_original
    else:
        if base_href_original == './':
            base_href = '../'
        else:
            base_href = '../' + base_href_original

    nav_current = int(md_dict.get('nav_current', 1))
    current_path_map = {1: "", 2: "portfolio/", 3: "credentials/", 4: "contact/"}
    current_page_path = current_path_map.get(nav_current, "")

    lang_links = ""
    for lang_code in ['en', 'es', 'fr', 'pt']:
        href = current_page_path if lang_code == 'en' else f"{lang_code}/{current_page_path}"
        if lang_code == language:
            lang_links += f'<button type="button" style="background-color: var(--btn-hover_BG); border-color: var(--btn-hover_border); pointer-events: none;">{lang_code.upper()}</button>\n'
        else:
            lang_links += f'<button type="button" onclick="changeLanguage(\'{lang_code}\', \'{base_href}{href}\')" title="Change language to {lang_code.upper()}">{lang_code.upper()}</button>\n'

    title_content = extract_translation(md_dict.get('title', ''), language)
    keys_raw = ', '.join(md_dict.get('keywords', []))
    keys_content = extract_translation(keys_raw, language)
    desc_content = extract_translation(md_dict.get('description', ''), language)

    # Translations for nav items
    lbl_portfolio = extract_translation("((en))portfolio((/en))((es))portafolio((/es))((fr))portfolio((/fr))((pt))portfólio((/pt))", language)
    lbl_credentials = extract_translation("((en))credentials((/en))((es))acreditaciones((/es))((fr))accréditations((/fr))((pt))credenciais((/pt))", language)
    lbl_contact = extract_translation("((en))contact((/en))((es))contacto((/es))((fr))contact((/fr))((pt))contato((/pt))", language)

    nav_items = [{"href": "./" if language == 'en' else f"{language}/",
                  "title": "Home Page",
                  "label": "~/"},
                 {"href": "portfolio/" if language == 'en' else f"{language}/portfolio/",
                  "title": "Portfolio Page",
                  "label": lbl_portfolio},
                 {"href": "credentials/" if language == 'en' else f"{language}/credentials/",
                  "title": "Credentials Page",
                  "label": lbl_credentials},
                 {"href": "contact/" if language == 'en' else f"{language}/contact/",
                  "title": "Contact Page",
                  "label": lbl_contact},
                 ]

    csp = "default-src 'self'; script-src 'self' 'unsafe-inline'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;"

    def space_padding(css_file):
        if not md_dict['css']:
            return ""
        return " " * (max(len(cf) for cf in md_dict['css']) - len(css_file))

    css_links = ""
    for css_file in md_dict.get('css', []):
        css_links += f'<link rel="stylesheet" href="./css/{css_file}.min.css">\n{space_padding(css_file)}'

    def space_padding_js(js_file):
        if not md_dict['js']:
            return ""
        return " " * (max(len(jf) for jf in md_dict['js']) - len(js_file))

    js_preloads = ""
    for js_file in md_dict.get('js', []):
        if js_file:
            js_preloads += f'  <link rel="preload" href="./js/{js_file}.min.js" {space_padding_js(js_file)}as="script">\n'

    js_defers = ""
    for js_file in md_dict.get('js', []):
        js_defers += f'  <script defer src="./js/{js_file}.min.js"> {space_padding_js(js_file)}</script>\n'

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
        topic_tag_text_value = ["programming", "cloud", "devops", "ai", "cybersecurity", "data-science", "database", "networking", "professional", "languages", "finance", "blockchain"]

        search_text = extract_translation("((en))Search((/en))((es))Buscar((/es))((fr))Chercher((/fr))((pt))Pesquisar((/pt))", language)
        filterType_text = extract_translation("((en))Filter by type((/en))((es))Filtrado por tipo((/es))((fr))Filtrer par type((/fr))((pt))Filtrar por tipo((/pt))", language)
        filterTopic_text = extract_translation("((en))Filter by topic((/en))((es))Filtrado por tema((/es))((fr))Filtrer par sujet((/fr))((pt))Filtrar por tópico((/pt))", language)
        stats_text = extract_translation("((en))Stats((/en))((es))Estadísticas((/es))((fr))Statistiques((/fr))((pt))Estatísticas((/pt))", language)
        reset_text = extract_translation("((en))↺ Clear filters((/en))((es))↺ Limpiar filtros((/es))((fr))↺ Effacer les filtres((/fr))((pt))↺ Limpar filtros((/pt))", language)
        search_placeholder = extract_translation("((en))Title, issuer or description…((/en))((es))Título, emisor o descripción…((/es))((fr))Titre, émetteur ou description…((/fr))((pt))Título, emissor ou descrição…((/pt))", language)

        type_tag_text = [
            extract_translation("((en))All((/en))((es))Todos((/es))((fr))Tous((/fr))((pt))Todos((/pt))", language),
            extract_translation("((en))Education((/en))((es))Educación((/es))((fr))Éducation((/fr))((pt))Educação((/pt))", language),
            extract_translation("((en))Certifications((/en))((es))Certificaciones((/es))((fr))Certifications((/fr))((pt))Certificações((/pt))", language),
            extract_translation("((en))Certificates((/en))((es))Certificados((/es))((fr))Certificats((/fr))((pt))Certificados((/pt))", language),
            extract_translation("((en))Badges((/en))((es))Insignias((/es))((fr))Insignes((/fr))((pt))Emblemas((/pt))", language),
            extract_translation("((en))Awards((/en))((es))Premios((/es))((fr))Prix((/fr))((pt))Prêmios((/pt))", language)
        ]

        topic_tag_text = [
            extract_translation("((en))Programming((/en))((es))Programación((/es))((fr))Programmation((/fr))((pt))Programação((/pt))", language),
            extract_translation("((en))Cloud((/en))((es))Nube((/es))((fr))Nuage((/fr))((pt))Nuvem((/pt))", language),
            extract_translation("((en))DevOps((/en))((es))DevOps((/es))((fr))DevOps((/fr))((pt))DevOps((/pt))", language),
            extract_translation("((en))AI((/en))((es))IA((/es))((fr))IA((/fr))((pt))IA((/pt))", language),
            extract_translation("((en))Cybersecurity((/en))((es))Ciberseguridad((/es))((fr))Cybersécurité((/fr))((pt))Cibersegurança((/pt))", language),
            extract_translation("((en))Data Science((/en))((es))Ciencia de Datos((/es))((fr))Science des Données((/fr))((pt))Ciência de Dados((/pt))", language),
            extract_translation("((en))Database((/en))((es))Base de datos((/es))((fr))Base de données((/fr))((pt))Banco de dados((/pt))", language),
            extract_translation("((en))Networking((/en))((es))Redes((/es))((fr))Réseaux((/fr))((pt))Redes((/pt))", language),
            extract_translation("((en))Professional((/en))((es))Profesional((/es))((fr))Professionnel((/fr))((pt))Profissional((/pt))", language),
            extract_translation("((en))Languages((/en))((es))Idiomas((/es))((fr))Langues((/fr))((pt))Idiomas((/pt))", language),
            extract_translation("((en))Finance((/en))((es))Finanzas((/es))((fr))Finance((/fr))((pt))Finanças((/pt))", language),
            extract_translation("((en))Blockchain((/en))((es))Blockchain((/es))((fr))Blockchain((/fr))((pt))Blockchain((/pt))", language)
        ]

        lbl_total = extract_translation("((en))Total((/en))((es))Total((/es))((fr))Total((/fr))((pt))Total((/pt))", language)

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
                   placeholder="{search_placeholder}"
                   autocomplete="off" aria-label="{search_text}">
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
                <span class="stat-item" data-type="education"><span class="stat-label">{type_tag_text[1]}</span>: <span class="stat-count" data-type="education">0</span></span>
                <span class="stat-item" data-type="certification"><span class="stat-label">{type_tag_text[2]}</span>: <span class="stat-count" data-type="certification">0</span></span>
                <span class="stat-item" data-type="certificate"><span class="stat-label">{type_tag_text[3]}</span>: <span class="stat-count" data-type="certificate">0</span></span>
                <span class="stat-item" data-type="badge"><span class="stat-label">{type_tag_text[4]}</span>: <span class="stat-count" data-type="badge">0</span></span>
                <span class="stat-item" data-type="award"><span class="stat-label">{type_tag_text[5]}</span>: <span class="stat-count" data-type="award">0</span></span>
                <span class="stat-item total"><span class="stat-label">{lbl_total}:</span> <span class="stat-count" id="global-total-credentials">0</span></span>
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
    lbl_hide_menu = extract_translation("((en))Hide Menu((/en))((es))Ocultar Menú((/es))((fr))Masquer menu((/fr))((pt))Ocultar Menu((/pt))", language)
    lbl_show_menu = extract_translation("((en))Show Menu((/en))((es))Mostrar Menú((/es))((fr))Afficher menu((/fr))((pt))Mostrar Menu((/pt))", language)

    # Initial redirection script for English home page
    redirect_script = ""
    if language == 'en' and nav_current == 1:
        redirect_script = """
  <script>
    document.addEventListener("DOMContentLoaded", function() {
        var savedLang = getCookie('language');
        var browserLang = navigator.language || navigator.userLanguage;
        var langCode = savedLang || browserLang.substring(0, 2);
        
        if (!document.cookie.includes('langRedirected=true')) {
            document.cookie = "langRedirected=true; path=/; max-age=86400";
            if (langCode === 'es') window.location.replace('es/');
            if (langCode === 'fr') window.location.replace('fr/');
            if (langCode === 'pt') window.location.replace('pt/');
        }
    });
  </script>
"""

    # Read the template from templates/base.html
    template_path = os.path.join(os.path.dirname(__file__), "..", "templates", "base.html")
    with open(template_path, 'r', encoding='utf-8') as f:
        html_template = f.read()

    json_ld = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ProfilePage",
    "mainEntity": {{
      "@type": "Person",
      "name": "Ariel Parra",
      "url": "https://ArielParra.github.io",
      "image": "https://ArielParra.github.io/img/ArielParra.jpg",
      "description": "{html.escape(desc_content)}",
      "sameAs": [
        "https://github.com/ArielParra",
        "https://www.linkedin.com/in/arielparra/"
      ]
    }}
  }}
  </script>
"""

    # Apply variables
    replacements = {
        "language": language,
        "base_href": base_href,
        "csp": csp,
        "keys_content": html.escape(keys_content),
        "desc_content": html.escape(desc_content),
        "title_content": html.escape(title_content),
        "css_links": css_links.rstrip('\n'),
        "js_preloads": js_preloads.rstrip('\n'),
        "js_defers": js_defers.rstrip('\n'),
        "nav_html": nav_html.rstrip('\n'),
        "credentials_filters": credentials_filters,
        "main_content": main_content,
        "lang_links": lang_links.rstrip('\n'),
        "lbl_hide_menu": html.escape(lbl_hide_menu),
        "lbl_show_menu": html.escape(lbl_show_menu),
        "redirect_script": redirect_script.strip('\n'),
        "json_ld": json_ld.strip('\n')
    }

    for key, val in replacements.items():
        html_template = html_template.replace(f"{{{{ {key} }}}}", str(val))

    return html_template
