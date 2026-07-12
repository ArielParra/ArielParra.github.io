import re

LANGUAGES = ['en', 'es', 'fr', 'pt']


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
        md_dict[key] = value

    if 'css' not in md_dict:
        md_dict['css'] = []
    if 'js' not in md_dict:
        md_dict['js'] = []

    return md_dict


def extract_translation(text, lang):
    if isinstance(text, dict):
        return text.get(lang, text.get('en', ''))
    if not isinstance(text, str):
        return text

    # Find contiguous language blocks (allowing whitespace between them)
    pattern = re.compile(r'(?:\s*\(\((?:en|es|fr|pt)\)\).*?\(\(/(?:en|es|fr|pt)\)\)\s*)+', re.DOTALL)

    def replacer(match):
        full_text = match.group(0)

        # Preserve leading and trailing whitespace
        match_leading = re.match(r'^\s*', full_text).group(0)
        match_trailing = re.search(r'\s*$', full_text).group(0)

        blocks = re.findall(r'\(\((en|es|fr|pt)\)\)(.*?)\(\(/\1\)\)', full_text, re.DOTALL)
        lang_dict = {lang_key: content for lang_key, content in blocks}

        content = ""
        if lang in lang_dict:
            content = lang_dict[lang]
        elif 'en' in lang_dict:
            content = lang_dict['en']
        elif blocks:
            content = blocks[0][1]

        return match_leading + content + match_trailing

    return pattern.sub(replacer, text)


def process_linked_image_match(m, page_lang):
    full_match = m.group(0)
    img_part = m.group(1)

    img_alt_match = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', img_part)
    img_url = img_alt_match.group(2) if img_alt_match else ""
    img_alt_raw = img_alt_match.group(1) if img_alt_match else "image"

    alt_match = re.search(r'alt="([^"]*)"', img_alt_raw)
    img_alt = alt_match.group(1) if alt_match else ""
    if not img_alt and not re.search(r'\w+="[^"]*"', img_alt_raw):
        img_alt = img_alt_raw.strip()

    img_alt_translated = extract_translation(img_alt, page_lang)

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

    title_translated = extract_translation(title_val, page_lang)

    all_urls = re.findall(r'\]\(([^)]+)\)', full_match)
    link_url = "#"
    for url in reversed(all_urls):
        url_lower = url.lower()
        if not (
            'img/' in url or url.startswith('./img/') or url.startswith('/img/')) or (
            url_lower.endswith(
                ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.ico')) and 'monero' in url_lower):
            link_url = url
            break

    target_match = re.search(r'target="([^"]+)"', full_match)
    target = target_match.group(1) if target_match else "_blank"

    img_parts = [f'<img src="{img_url}"']

    if other_img_attrs:
        img_parts.extend(other_img_attrs)

    img_parts.append(f'alt="{img_alt_translated}"')
    if title_translated:
        img_parts.append(f'title="{title_translated}"')

    img_tag = ' '.join(img_parts) + '>'
    return f'<a href="{link_url}" target="{target}">{img_tag}</a>'


def process_image_match(m, page_lang):
    alt_raw = m.group(1)
    url = m.group(2)
    attrs = m.group(3) or ""

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

    title_match = re.search(r'title="([^"]+)"', attrs)
    if title_match:
        title_val = title_match.group(1)

    alt_translated = extract_translation(alt, page_lang)
    title_translated = extract_translation(title_val, page_lang)

    img_parts = [f'<img src="{url}"']

    if other_img_attrs:
        img_parts.extend(other_img_attrs)

    img_parts.append(f'alt="{alt_translated}"')
    if title_translated:
        img_parts.append(f'title="{title_translated}"')

    return ' '.join(img_parts) + '>'


def process_link_match(m):
    text_content = m.group(1)
    url = m.group(2)
    attrs = m.group(3) or ""
    attr_parts = [f'href="{url}"']
    for attr_match in re.finditer(r'(\w+)="([^"]*)"', attrs):
        key = attr_match.group(1)
        val = attr_match.group(2)
        attr_parts.append(f'{key}="{val}"')
    return f'<a {" ".join(attr_parts)}>{text_content}</a>'


def replace_linked_images(text, page_lang):
    return re.sub(
        r'\[(!?\[[^\]]*\]\([^)]+\))\]\(([^)]+)\)(?:\{:([^\}]*)\})?',
        lambda m: process_linked_image_match(m, page_lang),
        text)


def replace_images(text, page_lang):
    return re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)(?:\{:([^\}]*)\})?',
        lambda m: process_image_match(m, page_lang),
        text)


def replace_links(text):
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)(?:\{:([^\}]*)\})?', process_link_match, text)


def md_to_html_phase1(text, page_lang):
    text = replace_linked_images(text, page_lang)
    text = replace_images(text, page_lang)
    text = replace_links(text)
    return text


def md_to_html_phase2(text):
    text = re.sub(r'##### (.*?)(?:\n|$)', r'<h5>\1</h5>\n', text)
    text = re.sub(r'#### (.*?)(?:\n|$)', r'<h4>\1</h4>\n', text)
    text = re.sub(r'### (.*?)(?:\n|$)', r'<h3>\1</h3>\n', text)
    text = re.sub(r'## (.*?)(?:\n|$)', r'<h2>\1</h2>\n', text)
    text = re.sub(r'# (.*?)(?:\n|$)', r'<h1>\1</h1>\n', text)

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

    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)

    return text


def md_to_html(md_content, page_lang):
    md_content = md_to_html_phase1(md_content, page_lang)

    # Handle language blocks in the text
    md_content = extract_translation(md_content, page_lang)

    result = md_to_html_phase2(md_content)

    return result
