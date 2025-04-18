"""
Author: Ariel Parra
"""
import re
import sys
import io
import argparse

def parse_md(md_content):
    md_dict = {}
    md_content = md_content.strip('---').strip()
    for line in md_content.split('\n'):
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        if value.startswith('[') and value.endswith(']'):
            value = [v.strip() for v in value[1:-1].split(',')]
        md_dict[key] = value
    return md_dict

def md_to_html(md_content):
    md_content = re.sub(r'!\[([^\]]+)\]\((.*?)\)', r'<img src="\2" \1>', md_content)
    md_content = re.sub(r'\[([^\]]+)\]\((.*?)\){:(.*?)}', r'<a href="\2" \3>\1</a>', md_content)
    md_content = re.sub(r'\[([^\]]+)\]\((.*?)\)', r'<a href="\2">\1</a>', md_content)
    md_content = re.sub(r'##### (.*?)\n', r'<h5>\1</h5>\n', md_content)
    md_content = re.sub(r'#### (.*?)\n', r'<h4>\1</h4>\n', md_content)
    md_content = re.sub(r'### (.*?)\n', r'<h3>\1</h3>\n', md_content)
    md_content = re.sub(r'## (.*?)\n', r'<h2>\1</h2>\n', md_content)
    md_content = re.sub(r'# (.*?)\n', r'<h1>\1</h1>\n', md_content)
    md_content = re.sub(r'(- .*)', r'<li>\1</li>', md_content)
    md_content = re.sub(r'<li>- (.*?)</li>', r'<ul><li>\1</li></ul>', md_content, flags=re.DOTALL)
    md_content = re.sub(r'</ul>\s*<ul>', '', md_content)  # Merge consecutive <ul> tags
    md_content = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', md_content)
    md_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', md_content)
    md_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', md_content)
    md_content = re.sub(r'\[comment\]: <> \(\n?(.*?)\n?\)\n', r'<!-- \1 -->\n', md_content, flags=re.DOTALL)

    return md_content

def generate_html(md_dict, md_content):
    language = md_dict['lang']
    cpp_label_text = "C++"
    linux_label_text = "Linux"
    portfolio_path = "./portfolio/"
    credentials_path = "./credentials/"
    contact_path = "./contact/"
    home_path = "./"

    es_path = "es/"
    if language == "en":
        home_title_text = "Home Page"
        portfolio_label_text = "portfolio"
        credentials_label_text = "credentials"
        contact_label_text = "contact"
        webDev_label_text = "Web dev"
        servers_label_text = "Servers"
        servers_label_text = "Servers"
    else:  # Spanish
        home_title_text = "Página Principal"
        portfolio_label_text = "portafolio"
        credentials_label_text = "acreditaciones"
        contact_label_text = "contacto"
        webDev_label_text = "Desarrollo Web"
        servers_label_text = "Servidores"
        servers_label_text = "Servidores"
        portfolio_path += es_path
        credentials_path += es_path
        contact_path += es_path
        home_path += es_path


    nav_items = [
        {"href": home_path, "title": home_title_text, "label": "~/"},
        {"href": portfolio_path, "title": "", "label": portfolio_label_text},
        {"href": credentials_path, "title": "", "label": credentials_label_text},
        {"href": contact_path, "title": "", "label": contact_label_text},
    ]

    
    nav_current = int(md_dict['nav_current'])

    html_content = f"""<!DOCTYPE html>
<html lang="{language}">

<head>
  <base href="{md_dict['base_href']}">
  <!-- App manifest -->
  <link rel="manifest" href="./manifest.json">
  <!-- Info -->
  <meta   charset="UTF-8">
  <meta   name="viewport"        content="width=device-width, initial-scale=1">
  <meta   name="keywords"        content="{', '.join(md_dict['keywords'])}">
  <meta   name="description"     content="{md_dict['description']}">
  <meta   name="author"          content="Ariel Parra">
  <title> {md_dict['title']} </title>
  <!-- CSS stylesheet -->
  <link   rel="preload"          href="./style.css" as="style">
  <link   rel="stylesheet"       href="./style.css">
  <!-- Java Scripts Preloads -->
"""
    def space_padding(js_file):
        return " " * (max(len(js_file) for js_file in md_dict['js']) - len(js_file))
    
    for js_file in md_dict['js']:
        html_content += f'  <link   rel="preload"          href="./js/{js_file}.js" {space_padding(js_file)}as="script">\n'
    
    html_content += """  <!-- Java Scripts defers -->
"""
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
    if language == "es":
        nav_button_text = "Mostrar Menú"
        lang_button_text = "Inglés"
        theme_button_title = "Cambiar tema de color a"
    else:  # English
        nav_button_text = "Hide Menu"
        lang_button_text = "Spanish"
        theme_button_title = "Change color theme to"

    html_content += f"""
  <div class="container">
    <button type="button" onclick="toggleMenu(this)"  id="menuButton"   data-nav-shown="true">{nav_button_text}</button>
    <button type="button" onclick="langButton(this)"  id="langButton"  title="Change language to">{lang_button_text}</button>
    <button type="button" onclick="toggleTheme(this)" id="themeButton" title="{theme_button_title}"> 🌗 </button>
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
        type_tag_text_value = ["all", "certification", "certificate", "badge", "award"]
        topic_tag_text_value = ["cybersecurity", "devOps", "networks", "cloud", "blockchain", "programming", "datascience", "ai"]

        if language == "en":
            filterType_text = "Filter by type"
            filterTopic_text = "Filter by topic"
            type_tag_text = ["All", "Certifications", "Certificates", "Badges", "Awards"]
            topic_tag_text = ["Cybersecurity", "DevOps","Networks", "Cloud", "Blockchain", "Programming", "Data Science", "AI"]
        else:  # Spanish
            filterType_text = "Filtrado por tipo"
            filterTopic_text = "Filtrado por tema"
            type_tag_text = ["Todos", "Certificaciones", "Certificados", "Insignias", "Reconocimientos"]
            topic_tag_text = ["Ciberseguridad", "DevOps", "Redes", "Nube", "Blockchain", "Programación", "Ciencia de Datos", "IA"]

        html_content += f"""
<div class="container max-width">
    <div class="card max-width" id="filter-checks">
        <hr>
        <div class="center">
            <h4>{filterType_text}</h4>
        </div>
        <hr>
        <div class="center">
"""
        # Generate radio buttons for "Filter by type"
        for idx, tag_value in enumerate(type_tag_text_value):
            tag_text = type_tag_text[idx] if idx < len(type_tag_text) else tag_value.capitalize()
            html_content += f"""          <label><input type="radio" name="type" value="{tag_value}" {'checked' if idx == 0 else ''} onchange="filterCards()"> {tag_text} </label>\n"""

        html_content += f"""        </div>
        <hr>
        <div class="center">
            <h4>{filterTopic_text}</h4>
        </div>
        <hr>
        <div class="center">
"""
        # Generate checkboxes for "Filter by topic"
        for idx, tag_value in enumerate(topic_tag_text_value):
            tag_text = topic_tag_text[idx] if idx < len(topic_tag_text) else tag_value.capitalize()
            html_content += f"""          <label><input type="checkbox" value="{tag_value}" onchange="filterCards()"> {tag_text} </label>\n"""

        html_content += """        </div>
    </div><!--filters card-->
</div><!--filters container-->
"""
    # all the content from md file
    html_content += md_to_html(md_content)
        
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
