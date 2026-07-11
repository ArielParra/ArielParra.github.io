import re
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
        md_dict[key] = value

    if 'css' not in md_dict:
        md_dict['css'] = []
    if 'js' not in md_dict:
        md_dict['js'] = []

    return md_dict


def extract_i18n_from_attr(attr_value):
    en_match = re.search(r'\(\(en\)\)(.*?)\(\(/en\)\)', attr_value)
    es_match = re.search(r'\(\(es\)\)(.*?)\(\(/es\)\)', attr_value)
    if en_match and es_match:
        prefix = attr_value[:en_match.start()]
        suffix = attr_value[es_match.end():]
        en_content = prefix + en_match.group(1) + suffix
        es_content = prefix + es_match.group(1) + suffix
        return ('', en_content, es_content)
    return (attr_value, None, None)


def process_linked_image_match(m):
    full_match = m.group(0)
    img_part = m.group(1)

    img_alt_match = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', img_part)
    img_url = img_alt_match.group(2) if img_alt_match else ""
    img_alt_raw = img_alt_match.group(1) if img_alt_match else "image"

    alt_match = re.search(r'alt="([^"]*)"', img_alt_raw)
    img_alt = alt_match.group(1) if alt_match else ""
    if not img_alt and not re.search(r'\w+="[^"]*"', img_alt_raw):
        img_alt = img_alt_raw.strip()

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


def process_image_match(m):
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

    alt_plain, alt_en, alt_es = extract_i18n_from_attr(alt)
    title_plain, title_en, title_es = extract_i18n_from_attr(title_val)

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


def replace_linked_images(text):
    return re.sub(
        r'\[(!?\[[^\]]*\]\([^)]+\))\]\(([^)]+)\)(?:\{:([^\}]*)\})?',
        process_linked_image_match,
        text)


def replace_images(text):
    return re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)(?:\{:([^\}]*)\})?',
        process_image_match,
        text)


def replace_links(text):
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)(?:\{:([^\}]*)\})?', process_link_match, text)


def md_to_html_phase1(text):
    text = replace_linked_images(text)
    text = replace_images(text)
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


def get_translations(text):
    if isinstance(text, dict):
        return text.get('en', ''), text.get('es', '')
    if not isinstance(text, str):
        return text, text
    pattern = re.compile(r'\(\((en|es)\)\)(.*?)\(\(/\1\)\)', re.DOTALL)
    matches = pattern.findall(text)
    if not matches:
        return text, text

    results = {'en': text, 'es': text}
    for lang_key, content in matches:
        results[lang_key] = content
    return results['en'], results['es']


def extract_translation(text, lang):
    if isinstance(text, dict):
        return text.get(lang, text.get('en', ''))
    if not isinstance(text, str):
        return text
    pattern = re.compile(r'\(\((en|es)\)\)(.*?)\(\(/\1\)\)', re.DOTALL)
    matches = pattern.findall(text)
    if not matches:
        return text
    for lang_key, content in matches:
        if lang_key == lang:
            return content
    return text


def md_to_html(md_content, page_lang):
    md_content = md_to_html_phase1(md_content)

    def is_inside_attribute(text, pos):
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

        after_eq = before[last_unquoted_eq + 1:]
        return after_eq.count('"') % 2 == 1

    pattern = re.compile(r'\(\((en|es)\)\)(.*?)\(\(/\1\)\)', re.DOTALL)

    parts = []
    last_pos = 0
    matches = list(pattern.finditer(md_content))

    i = 0
    while i < len(matches):
        m = matches[i]

        if is_inside_attribute(md_content, m.start()):
            i += 1
            continue

        parts.append(('text', md_content[last_pos:m.start()]))

        lang = m.group(1)
        content = m.group(2)
        complement = 'es' if lang == 'en' else 'en'

        if i + 1 < len(matches):
            next_m = matches[i + 1]
            if next_m.group(
                    1) == complement and md_content[m.end():next_m.start()].strip() == "":
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
            final_html.append(
                f'<span class="i18n" data-i18n-en="{en_attr}" data-i18n-es="{es_attr}">{display_html}</span>')
        elif ptype == 'single':
            lang, content = val
            final_html.append(md_to_html_phase2(content).strip())

    result = "".join(final_html)
    result = md_to_html_phase2(result)

    return result
