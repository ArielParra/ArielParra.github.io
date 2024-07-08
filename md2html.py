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
    md_content = re.sub(r'### (.*?)\n', r'<h3>\1</h3>\n', md_content)
    md_content = re.sub(r'## (.*?)\n', r'<h2>\1</h2>\n', md_content)
    md_content = re.sub(r'# (.*?)\n', r'<h1>\1</h1>\n', md_content)
    md_content = re.sub(r'\[\]: <> \("(.*?)"\)', r'<!--\1-->', md_content)
    md_content = re.sub(r'(- .*)', r'<li>\1</li>', md_content)
    md_content = re.sub(r'<li>- (.*?)</li>', r'<ul><li>\1</li></ul>', md_content, flags=re.DOTALL)
    md_content = re.sub(r'</ul>\s*<ul>', '', md_content)  # Merge consecutive <ul> tags

    md_content = re.sub(r'\n\n', '</p><p>', md_content)
    return md_content

def generate_html(md_dict, md_content):
    language = md_dict['lang']
    if language == "en":
        home_title_text = "Home Page"
        portfolio_label_text = "portfolio"
        achivements_label_text = "achivements"
        contact_label_text = "contact"
        webDev_label_text = "Web dev"
        servers_label_text = "Servers"
    else:  # Spanish
        home_title_text = "Página Principal"
        portfolio_label_text = "portafolio"
        achivements_label_text = "logros"
        contact_label_text = "contacto"
        webDev_label_text = "Desarrollo Web"
        servers_label_text = "Servidores"
        
    nav_items = [
        {"href": "./", "title": home_title_text, "label": "~/"},
        {"href": "./portfolio/", "title": "", "label": portfolio_label_text},
        {"href": "./achivements/", "title": "", "label": achivements_label_text},
        {"href": "./contact/", "title": "", "label": contact_label_text},
        {"href": "./blog/", "title": "", "label": "blog"},
    ]
    blog_items = [
        {"href": "./blog/webDev", "title": home_title_text, "label": webDev_label_text},
        {"href": "./blog/competitive/", "title": "", "label": "C++"},
        {"href": "./blog/linux/", "title": "", "label": "Linux"},
        {"href": "./blog/servers/", "title": "", "label": servers_label_text},
    ]
    
    nav_current = int(md_dict['nav_current'])
    blog_current = int(md_dict['blog_current'])
    html_content = f"""<!DOCTYPE html>
<html lang="{language}">

<head>
    <!-- Info -->
    <base href="{md_dict['base_href']}">
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
        if js_file == "main":
            html_content += f'    <link   rel="preload"          href="./{js_file}.js"    {space_padding(js_file)}as="script">\n'	
        else:
            html_content += f'    <link   rel="preload"          href="./js/{js_file}.js" {space_padding(js_file)}as="script">\n'
    
    html_content += """    <!-- Java Scripts defers -->
"""
    for js_file in md_dict['js']:
        if js_file == "main":
            html_content += f'    <script defer                  src ="./{js_file}.js">    {space_padding(js_file)}</script>\n'
        else:    
            html_content += f'    <script defer                  src ="./js/{js_file}.js"> {space_padding(js_file)}</script>\n'
    
    
    html_content += """    <!-- Favicons -->  
    <link   rel="apple-touch-icon" href="./images/foto.webp"   type="image/webp" sizes="180x180">
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
    <button type="button" onclick="toggleMenu(this)" id="navButton" data-nav-shown="true">{nav_button_text}</button>
    <button type="button" onclick="langButton(this)" id="langButton" title="Change language to">{lang_button_text}</button>
    <button type="button" onclick="toggleTheme(this)" id="themeButton" title="{theme_button_title}"> 🌗 </button>
    </div><!-- Buttons -->

    <nav>
"""

    for idx, item in enumerate(nav_items, start=1):
        class_name = "current" if idx == nav_current else "NotCurrent"
        html_content += f'        <a href="{item["href"]}" class="{class_name}" title="{item["title"]}"> <span>{item["label"]}</span></a>\n'
    
    html_content += """  </nav>
"""
    

    if nav_current == 3:
        type_tag_text_value = ["all", "certification", "certificate", "badge"]
        topic_tag_text_value = ["cybersecurity", "devOps", "networks", "cloud", "blockchain", "progamming", "datascience", "ai"]

        if language == "en":
            filterType_text = "Filter by type"
            filterTopic_text = "Filter by topic"
            type_tag_text = ["All", "Certifications", "Certificates", "Badges"]
            topic_tag_text = ["Cybersecurity", "Networks", "Cloud", "Blockchain", "Programming", "Data Science", "AI"]
        else:  # assuming Spanish
            filterType_text = "Filtrado por tipo"
            filterTopic_text = "Filtrado por tema"
            type_tag_text = ["Todos", "Certificaciones", "Certificados", "Insignias"]
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



    if blog_current != 0: 
        html_content += """  <nav>"""
        
        for idx, item in enumerate(blog_items, start=1):
            class_name = "current" if idx == blog_current else "NotCurrent"
            html_content += f'    <a href="{item["href"]}" class="{class_name}" title="{item["title"]}"> <span>{item["label"]}</span></a>\n'
        html_content += """  </nav>
    """
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
        md_content = md_parts[2].strip()
    else:
        raise ValueError("Invalid markdown format. Ensure the file starts with a header block delimited by '---'.")

    md_dict = parse_md(md_header)
    html_content = generate_html(md_dict, md_content)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == '__main__':
    main()
