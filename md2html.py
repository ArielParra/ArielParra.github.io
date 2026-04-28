"""
Author: Ariel Parra
"""
import re
import sys
import io
import argparse
import html

def parse_md(md_content):
    md_dict = {}
    md_content = md_content.strip('---').strip()
    for line in md_content.split('\n'):
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        if value.startswith('[') and value.endswith(']'):
            value = [v.strip() for v in value[1:-1].split(',')]
        else:
            value = value
        md_dict[key] = value
    
    if 'css' not in md_dict:
        md_dict['css'] = []
    if 'js' not in md_dict:
        md_dict['js'] = []
        
    return md_dict

def extract_i18n_from_attr(attr_value):
    """Extract i18n content from an attribute value.
    
    Args:
        attr_value: The attribute value string to check for i18n tags
        
    Returns:
        tuple: (plain_text, en_content, es_content)
        - If attr contains i18n: plain_text is empty, en/es are the translations
        - If attr has no i18n: plain_text is the original value, en/es are None
    """
    en_match = re.search(r'\(\(en\)\)(.*?)\(\(/en\)\)', attr_value)
    es_match = re.search(r'\(\(es\)\)(.*?)\(\(/es\)\)', attr_value)
    if en_match and es_match:
        prefix = attr_value[:en_match.start()]
        suffix = attr_value[es_match.end():]
        en_content = prefix + en_match.group(1) + suffix
        es_content = prefix + es_match.group(1) + suffix
        return ('', en_content, es_content)
    return (attr_value, None, None)

def md_to_html_phase1(text):
    # Process linked images: [![alt](url)](link){: target="_blank"}
    def fix_linked_img(m):
        full_match = m.group(0)
        img_part = m.group(1) # ![alt](url)

        img_alt_match = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', img_part)
        img_url = img_alt_match.group(2) if img_alt_match else ""
        img_alt_raw = img_alt_match.group(1) if img_alt_match else "image"
        
        # Extract alt attribute value
        alt_match = re.search(r'alt="([^"]*)"', img_alt_raw)
        img_alt = alt_match.group(1) if alt_match else ""
        if not img_alt and not re.search(r'\w+="[^"]*"', img_alt_raw):
            img_alt = img_alt_raw.strip()
        
        # Check for i18n in alt
        img_alt_plain, img_alt_en, img_alt_es = extract_i18n_from_attr(img_alt)

        other_img_attrs = []
        title_val = ""
        for attr_match in re.finditer(r'(\w+)="([^"]*)"', img_alt_raw):
            key = attr_match.group(1)
            val = attr_match.group(2)
            if key == 'alt':
                continue
            elif key == 'title':
                title_val = val
            else:
                other_img_attrs.append(attr_match.group(0))

        title_plain, title_en, title_es = extract_i18n_from_attr(title_val)

        # Find all ](...) patterns - the non-image one is the link URL
        all_urls = re.findall(r'\]\(([^)]+)\)', full_match)
        link_url = "#"
        for url in reversed(all_urls):
            url_lower = url.lower()
            # Skip URLs that look like image paths (have img/ and common extensions)
            if not ('img/' in url or url.startswith('./img/') or url.startswith('/img/')) or \
               (url_lower.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.ico')) and 'monero' in url_lower):
                link_url = url
                break

        target_match = re.search(r'target="([^"]+)"', full_match)
        target = target_match.group(1) if target_match else "_blank"

        # Build img tag with i18n data attributes if applicable
        img_parts = [f'<img src="{img_url}"']
        
        if other_img_attrs:
            img_parts.extend(other_img_attrs)

        if img_alt_en and img_alt_es:
            img_parts.append(f'data-i18n-alt-en="{html.escape(img_alt_en)}"')
            img_parts.append(f'data-i18n-alt-es="{html.escape(img_alt_es)}"')
            img_parts.append(f'alt="{img_alt_en}"')
        elif img_alt:
            img_parts.append(f'alt="{img_alt}"')
        else:
            img_parts.append('alt=""')
            
        if title_en and title_es:
            img_parts.append(f'data-i18n-title-en="{html.escape(title_en)}"')
            img_parts.append(f'data-i18n-title-es="{html.escape(title_es)}"')
            img_parts.append(f'title="{title_en}"')
        elif title_val:
            img_parts.append(f'title="{title_val}"')
        
        img_tag = ' '.join(img_parts) + '>'
        return f'<a href="{link_url}" target="{target}">{img_tag}</a>'

    text = re.sub(r'\[(!?\[[^\]]*\]\([^)]+\))\]\(([^)]+)\)(?:\{:([^\}]*)\})?', fix_linked_img, text)

    # Process regular images: ![alt](url){: title="..."}
    def fix_image(m):
        alt_raw = m.group(1)
        url = m.group(2)
        attrs = m.group(3) or ""
        
        # Extract alt value
        alt_match = re.search(r'alt="([^"]*)"', alt_raw)
        alt = alt_match.group(1) if alt_match else ""
        if not alt and not re.search(r'\w+="[^"]*"', alt_raw):
            alt = alt_raw.strip()

        other_img_attrs = []
        title_val = ""
        for attr_match in re.finditer(r'(\w+)="([^"]*)"', alt_raw):
            key = attr_match.group(1)
            val = attr_match.group(2)
            if key == 'alt':
                continue
            elif key == 'title':
                title_val = val
            else:
                other_img_attrs.append(attr_match.group(0))

        # Extract title from attrs {: title="..."}
        title_match = re.search(r'title="([^"]+)"', attrs)
        if title_match:
            title_val = title_match.group(1)
        
        # Check for i18n in alt
        alt_plain, alt_en, alt_es = extract_i18n_from_attr(alt)
        
        # Check for i18n in title
        title_plain, title_en, title_es = extract_i18n_from_attr(title_val)
        
        # Build img tag with i18n data attributes if applicable
        img_parts = [f'<img src="{url}"']
        
        if other_img_attrs:
            img_parts.extend(other_img_attrs)

        if alt_en and alt_es:
            img_parts.append(f'data-i18n-alt-en="{html.escape(alt_en)}"')
            img_parts.append(f'data-i18n-alt-es="{html.escape(alt_es)}"')
            img_parts.append(f'alt="{alt_en}"')
        elif alt:
            img_parts.append(f'alt="{alt}"')
        else:
            img_parts.append('alt=""')
        
        if title_en and title_es:
            img_parts.append(f'data-i18n-title-en="{html.escape(title_en)}"')
            img_parts.append(f'data-i18n-title-es="{html.escape(title_es)}"')
            img_parts.append(f'title="{title_en}"')
        elif title_val:
            img_parts.append(f'title="{title_val}"')
        
        return ' '.join(img_parts) + '>'

    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)(?:\{:([^\}]*)\})?', fix_image, text)

    # Process links: [text](url){: target="..." class="..."}
    def fix_link(m):
        text_content = m.group(1)
        url = m.group(2)
        attrs = m.group(3) or ""
        # Extract all attributes from the {:...} block
        attr_parts = [f'href="{url}"']
        for attr_match in re.finditer(r'(\w+)="([^"]*)"', attrs):
            key = attr_match.group(1)
            val = attr_match.group(2)
            attr_parts.append(f'{key}="{val}"')
        return f'<a {" ".join(attr_parts)}>{text_content}</a>'

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)(?:\{:([^\}]*)\})?', fix_link, text)

    return text

def md_to_html_phase2(text):
    # Headings
    text = re.sub(r'##### (.*?)(?:\n|$)', r'<h5>\1</h5>\n', text)
    text = re.sub(r'#### (.*?)(?:\n|$)', r'<h4>\1</h4>\n', text)
    text = re.sub(r'### (.*?)(?:\n|$)', r'<h3>\1</h3>\n', text)
    text = re.sub(r'## (.*?)(?:\n|$)', r'<h2>\1</h2>\n', text)
    text = re.sub(r'# (.*?)(?:\n|$)', r'<h1>\1</h1>\n', text)

    # Lists
    lines = text.split('\n')
    new_lines = []
    in_list = False
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(line)
    if in_list:
        new_lines.append('</ul>')
    text = '\n'.join(new_lines)

    # Bold and Italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)

    return text

def get_translations(text):
    """Extracts both English and Spanish translations from i18n tags or objects.
    
    Args:
        text: The text containing i18n tags or a dict with en/es keys.
        
    Returns:
        tuple: (en_content, es_content)
    """
    if isinstance(text, dict):
        return text.get('en', ''), text.get('es', '')
    if not isinstance(text, str):
        return text, text
    pattern = re.compile(r'\(\((en|es)\)\)(.*?)\(\(/\1\)\)', re.DOTALL)
    matches = pattern.findall(text)
    if not matches:
        return text, text
    
    results = {'en': text, 'es': text}
    for l, content in matches:
        results[l] = content
    return results['en'], results['es']

def extract_translation(text, lang):
    """Extracts the translation for the given language from i18n tags or objects.
    
    Args:
        text: The text containing i18n tags or a dict with en/es keys.
        lang: The language to extract ('en' or 'es').
        
    Returns:
        The translated text or the original text if no tags are found.
    """
    if isinstance(text, dict):
        return text.get(lang, text.get('en', ''))
    if not isinstance(text, str):
        return text
    pattern = re.compile(r'\(\((en|es)\)\)(.*?)\(\(/\1\)\)', re.DOTALL)
    matches = pattern.findall(text)
    if not matches:
        return text
    for l, content in matches:
        if l == lang:
            return content
    return text

def md_to_html(md_content, page_lang):
    md_content = md_to_html_phase1(md_content)

    def is_inside_attribute(text, pos):
        """Check if position is inside a quoted attribute value.
        
        We scan backwards from pos to find the last unquoted ="
        """
        before = text[:pos]
        last_unquoted_eq = -1
        in_quote = False
        for i in range(len(before)):
            if before[i] == '"':
                in_quote = not in_quote
            elif before[i] == '=' and not in_quote:
                last_unquoted_eq = i
        
        if last_unquoted_eq == -1:
            return False
        
        after_eq = before[last_unquoted_eq+1:]
        return after_eq.count('"') % 2 == 1
    
    # Pattern to find i18n blocks
    pattern = re.compile(r'\(\((en|es)\)\)(.*?)\(\(/\1\)\)', re.DOTALL)

    parts = []
    last_pos = 0
    matches = list(pattern.finditer(md_content))

    i = 0
    while i < len(matches):
        m = matches[i]
        
        # Skip i18n blocks that are inside attribute values
        if is_inside_attribute(md_content, m.start()):
            i += 1
            continue
        
        # Append part before match
        parts.append(('text', md_content[last_pos:m.start()]))

        lang = m.group(1)
        content = m.group(2)
        complement = 'es' if lang == 'en' else 'en'

        if i + 1 < len(matches):
            next_m = matches[i+1]
            if next_m.group(1) == complement and md_content[m.end():next_m.start()].strip() == "":
                en_text = content if lang == 'en' else next_m.group(2)
                es_text = next_m.group(2) if lang == 'en' else content
                parts.append(('i18n', (en_text, es_text)))
                last_pos = next_m.end()
                i += 2
                continue

        parts.append(('single', (lang, content)))
        last_pos = m.end()
        i += 1

    parts.append(('text', md_content[last_pos:]))
    
    final_html = []
    for ptype, val in parts:
        if ptype == 'text':
            final_html.append(val)
        elif ptype == 'i18n':
            en_text, es_text = val
            en_html = md_to_html_phase2(en_text).strip()
            es_html = md_to_html_phase2(es_text).strip()
            display_html = en_html if page_lang == 'en' else es_html
            en_attr = html.escape(en_html, quote=True)
            es_attr = html.escape(es_html, quote=True)
            final_html.append(f'<span class="i18n" data-i18n-en="{en_attr}" data-i18n-es="{es_attr}">{display_html}</span>')
        elif ptype == 'single':
            lang, content = val
            final_html.append(md_to_html_phase2(content).strip())

    result = "".join(final_html)
    result = md_to_html_phase2(result)

# Post-process: Removed automatic </span>(url) to <a href="url"> conversion
    # Users must now use proper Markdown link format: [text](url) for links
    # This ensures that plain text followed by (url) is not mistakenly converted to a link
    # Example: ((es))ejemplo:((/es))(https://) will NOT become a link
    #          Only [((en))LINK((/en))((es))LINK((/es))](https://) will be a link
    result = result

    return result


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


    nav_items = [
        {"href": home_path, "title": "Home Page", "label": '<span class="i18n" data-i18n-en="~/" data-i18n-es="~/">~/</span>'},
        {"href": portfolio_path, "title": "", "label": '<span class="i18n" data-i18n-en="portfolio" data-i18n-es="portafolio">portfolio</span>'},
        {"href": credentials_path, "title": "", "label": '<span class="i18n" data-i18n-en="credentials" data-i18n-es="acreditaciones">credentials</span>'},
        {"href": contact_path, "title": "", "label": '<span class="i18n" data-i18n-en="contact" data-i18n-es="contacto">contact</span>'},
    ]
    
    nav_current = int(md_dict['nav_current'])
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

    def space_padding(js_file):
        return " " * (max(len(jf) for jf in md_dict['js']) - len(js_file))

    html_content += '  <!-- Java Scripts preloads -->\n' 
    for js_file in md_dict['js']:
        if js_file:
            html_content += f'  <link   rel="preload"          href="./js/{js_file}.js" {space_padding(js_file)}as="script">\n'
    
    html_content += '  <!-- Java Scripts defers -->\n'
    for js_file in md_dict['js']:
        if js_file == "main":
            html_content += f'  <script defer                  src ="./{js_file}.js">    {space_padding(js_file)}</script>\n'
        else:    
            html_content += f'  <script defer                  src ="./js/{js_file}.js"> {space_padding(js_file)}</script>\n'
    
    html_content += """  <!-- Favicons -->  
  <link   rel="apple-touch-icon" href="./img/ArielParra.jpg"   type="image/webp" sizes="180x180">
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
    <button type="button" onclick="toggleMenu(this)"  id="menuButton"   data-nav-shown="true">{nav_button_text}</button>
    <button type="button" onclick="langButton(this)"  id="langButton"  data-i18n-title-en="{lang_button_title_en}" data-i18n-title-es="{lang_button_title_es}" title="{lang_button_title_en}">{lang_button_text}</button>
    <button type="button" onclick="toggleTheme(this)" id="themeButton" data-i18n-title-en="{theme_button_title_en}" data-i18n-title-es="{theme_button_title_es}" title="{theme_button_title_en}"> 🌗 </button>
  </div><!-- Buttons -->

  <nav>
"""
    max_href_length = max(len(item["href"]) for item in nav_items)
    max_class_length = max(len("current"), len("NotCurrent"))
    max_title_length = max(len(item["title"]) for item in nav_items)
    max_label_length = max(len(item["label"]) for item in nav_items)
    
    for idx, item in enumerate(nav_items, start=1):
        class_name = "current" if idx == nav_current else "NotCurrent"
        html_content += (f'    <a href="{item["href"]}"' + " " * (max_href_length - len(item["href"])) +
                         f' class="{class_name}"' + " " * (max_class_length - len(class_name)) +
                         f' title="{item["title"]}' + " " * (max_title_length - len(item["title"])) +
                         f'"> <span>{item["label"]}' + " " * (max_label_length - len(item["label"])) +
                         '</span></a>\n')
        
    html_content += """  </nav>
"""
    
    if nav_current == 3:
        type_tag_text_value = ["all", "education", "certification", "certificate", "badge", "award"]
        topic_tag_text_value = ["Language", "ai", "backend", "blockchain", "cloud", "cybersecurity", "database", "datascience", "devops", "finance", "networks", "programming", "softskills", "web3"]
        filterType_text = '<span class="i18n" data-i18n-en="Filter by type" data-i18n-es="Filtrado por tipo">Filter by type</span>'
        filterTopic_text = '<span class="i18n" data-i18n-en="Filter by topic" data-i18n-es="Filtrado por tema">Filter by topic</span>'
        stats_text = '<span class="i18n" data-i18n-en="Stats" data-i18n-es="Estadísticas">Stats</span>'
        type_tag_text = ['<span class="i18n" data-i18n-en="All" data-i18n-es="Todos">All</span>',
                        '<span class="i18n" data-i18n-en="Education" data-i18n-es="Educación">Education</span>',
                        '<span class="i18n" data-i18n-en="Certifications" data-i18n-es="Certificaciones">Certifications</span>',
                        '<span class="i18n" data-i18n-en="Certificates" data-i18n-es="Certificados">Certificates</span>',
                        '<span class="i18n" data-i18n-en="Badges" data-i18n-es="Insignias">Badges</span>',
                        '<span class="i18n" data-i18n-en="Awards" data-i18n-es="Premios">Awards</span>']
        topic_tag_text = ['<span class="i18n" data-i18n-en="Language" data-i18n-es="Idioma">Language</span>',
                         '<span class="i18n" data-i18n-en="AI" data-i18n-es="IA">AI</span>',
                         '<span class="i18n" data-i18n-en="Back-end" data-i18n-es="Back-end">Back-end</span>',
                         '<span class="i18n" data-i18n-en="Blockchain" data-i18n-es="Blockchain">Blockchain</span>',
                         '<span class="i18n" data-i18n-en="Cloud" data-i18n-es="Nube">Cloud</span>',
                         '<span class="i18n" data-i18n-en="Cybersecurity" data-i18n-es="Ciberseguridad">Cybersecurity</span>',
                         '<span class="i18n" data-i18n-en="Database" data-i18n-es="Base de datos">Database</span>',
                         '<span class="i18n" data-i18n-en="Data Science" data-i18n-es="Ciencia de Datos">Data Science</span>',
                         '<span class="i18n" data-i18n-en="DevOps" data-i18n-es="DevOps">DevOps</span>',
                         '<span class="i18n" data-i18n-en="Finance" data-i18n-es="Finanzas">Finance</span>',
                         '<span class="i18n" data-i18n-en="Networks" data-i18n-es="Redes">Networks</span>',
                         '<span class="i18n" data-i18n-en="Programming" data-i18n-es="Programación">Programming</span>',
                         '<span class="i18n" data-i18n-en="Soft Skills" data-i18n-es="Habilidades blandas">Soft Skills</span>',
                         '<span class="i18n" data-i18n-en="Web3" data-i18n-es="Web3">Web3</span>']

        html_content += f"""
<div class="container max-width">
    <div class="card max-width" id="filter-checks">
        <hr>
        <div class="center">
            <h4>{filterType_text}</h4>
        </div>
        <hr>
        <div class="center row">
"""
        for idx, tag_value in enumerate(type_tag_text_value):
            tag_text = type_tag_text[idx] if idx < len(type_tag_text) else tag_value.capitalize()
            html_content += f"""          <label><input type="radio" name="type" value="{tag_value}" {'checked' if idx == 0 else ''} onchange="filterCards()"> {tag_text} </label>\n"""

        html_content += f"""        </div>
        <hr>
        <div class="center">
            <h4>{filterTopic_text}</h4>
        </div>
        <hr>
        <div class="center row">
"""
        for idx, tag_value in enumerate(topic_tag_text_value):
            tag_text = topic_tag_text[idx] if idx < len(topic_tag_text) else tag_value.capitalize()
            html_content += f"""          <label><input type="checkbox" value="{tag_value}" onchange="filterCards()"> {tag_text} </label>\n"""

        html_content += f"""        </div>
        <hr>
        <div class="center">
            <h4>{stats_text}</h4>
        </div>
        <hr>
        <div class="center">
            <span class="credential-counts">
                <span class="stat-item" data-type="education"><span class="stat-label i18n" data-i18n-en="Education" data-i18n-es="Educación">Education</span>: <span class="stat-count" data-type="education">0</span></span>
                <span class="stat-item" data-type="certification"><span class="stat-label i18n" data-i18n-en="Certifications" data-i18n-es="Certificaciones">Certifications</span>: <span class="stat-count" data-type="certification">0</span></span>
                <span class="stat-item" data-type="certificate"><span class="stat-label i18n" data-i18n-en="Certificates" data-i18n-es="Certificados">Certificates</span>: <span class="stat-count" data-type="certificate">0</span></span>
                <span class="stat-item" data-type="badge"><span class="stat-label i18n" data-i18n-en="Badges" data-i18n-es="Insignias">Badges</span>: <span class="stat-count" data-type="badge">0</span></span>
                <span class="stat-item" data-type="award"><span class="stat-label i18n" data-i18n-en="Awards" data-i18n-es="Premios">Awards</span>: <span class="stat-count" data-type="award">0</span></span>
                <span class="stat-item total"><span class="stat-label">Total:</span> <span class="stat-count" id="global-total-credentials">0</span></span>
            </span>
        </div>
    </div><!--filters card-->
</div><!--filters container-->
"""
    
    html_content += md_to_html(md_content, language)
        
    html_content += """ 
</body>
</html>"""
    return html_content

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML.')
    parser.add_argument('input_file', type=str, help='Input markdown file')
    parser.add_argument('output_file', type=str, help='Output HTML file')
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    md_parts = md_text.split('---', 2)
    if len(md_parts) == 3:
        md_header = md_parts[1].strip()
        md_content = md_parts[2]
    else:
        raise ValueError("Invalid markdown format. Ensure the file starts with a header block delimited by '---'.")

    md_dict = parse_md(md_header)
    html_content = generate_html(md_dict, md_content)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    main()
