#!/usr/bin/env python3
import os
import datetime
from pathlib import Path


def main():
    root_dir = Path(__file__).resolve().parent.parent
    sitemap_file = root_dir / "sitemap.xml"

    pages = [
        {"path": "", "freq": "monthly", "priority": "1.0", "md": "index.md"},
        {"path": "credentials/", "freq": "monthly", "priority": "0.9", "md": "credentials/index.md"},
        {"path": "portfolio/", "freq": "monthly", "priority": "0.8", "md": "portfolio/index.md"},
        {"path": "contact/", "freq": "annually", "priority": "0.6", "md": "contact/index.md"}
    ]

    base_url = "https://ArielParra.github.io/"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:
        md_file = root_dir / page["md"]
        if md_file.exists():
            mtime = os.path.getmtime(md_file)
            lastmod = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        else:
            lastmod = datetime.datetime.now().strftime("%Y-%m-%d")

        # English (default route)
        lines.append('    <url>')
        lines.append(f'        <loc>{base_url}{page["path"]}</loc>')
        lines.append(f'        <lastmod>{lastmod}</lastmod>')
        lines.append(f'        <changefreq>{page["freq"]}</changefreq>')
        lines.append(f'        <priority>{page["priority"]}</priority>')
        lines.append('    </url>')
        
        # Other languages
        for lang in ['es', 'fr', 'pt']:
            lang_path = f"{lang}/{page['path']}"
            lines.append('    <url>')
            lines.append(f'        <loc>{base_url}{lang_path}</loc>')
            lines.append(f'        <lastmod>{lastmod}</lastmod>')
            lines.append(f'        <changefreq>{page["freq"]}</changefreq>')
            lines.append(f'        <priority>{float(page["priority"]) - 0.1:.1f}</priority>')
            lines.append('    </url>')

    lines.append('</urlset>')

    with open(sitemap_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Generated {sitemap_file.name} with updated timestamps.")


if __name__ == '__main__':
    main()
