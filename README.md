# Ariel Parra Website

A simple, lightweight personal website. Previously hosted at arielparra.tech.

Built with plain HTML, CSS, and JavaScript—following HTML5 standards without bloated frameworks. Features custom mobile responsiveness, auto language detection, design, animations, and a Python-based static site generator.

## Quick Start

```bash
make              # Build all pages
make index        # Build specific page
make clean        # Remove generated HTML
```

## Project Structure

```
├── Makefile            # Build automation
├── *.md                # Source files with YAML frontmatter
├── scripts/            # Python build and management scripts
│   ├── md2html.py             # Python static site generator
│   ├── manage_portfolio.py    # CLI tool to manage portfolio JSON
│   ├── manage_credentials.py  # CLI tool to manage credentials JSON
│   └── base_manager.py        # OOP Base class for CLI tools
├── css/                # Modular stylesheets
│   ├── theme.css       # Color palette, light/dark themes
│   ├── common.css      # Base styles (nav, buttons, cards, scrollbar)
│   ├── credentials.css # Credentials card styles
│   ├── portfolio.css   # Portfolio grid styles
│   └── 404.css         # 404 page styles
├── js/                 # JavaScript modules
├── portfolio/          # Portfolio page sources
│   ├── data/
│   │   └── projects.json      # All portfolio projects data
│   ├── index.md               # Source markdown
│   └── index.html             # Generated output
├── contact/            # Contact page sources
└── credentials/        # Credentials page sources
    ├── data/
    │   └── credentials.json   # All credentials data (education, certs, etc.)
    ├── docs/                  # PDF documentation files
    ├── img/                   # Credential images
    ├── index.md               # Source markdown
    └── index.html             # Generated output
```

## Markdown Frontmatter Format

```markdown
---
title: Page Title
lang: en
base_href: ./
nav_current: 1
js: [main, menu, theme, language]
css: [theme, common, credentials]
---

content here
```

## i18n Syntax

```markdown
((en))English text((/en))((es))Texto en español((/es))
```

## Features

- **No dependencies**: Vanilla HTML, CSS, JavaScript
- **Lightweight**: No frameworks, no bundlers, no node_modules
- **Custom site generator**: Python-based `md2html.py`
- **Theming**: Manual light/dark mode support
- **Internationalization**: Auto language detection
- **Responsive**: Custom mobile-first design
- **Animated**: Subtle CSS animations

## Credentials Management

The site uses a JSON-based data source for credentials, processed into HTML by `manage_credentials.py`.

### credentials.json

Contains all education records, certifications, certificates, and badges organized by type:
- `type`: Category (education, certification, certificate, badge, award)
- `issuer`: Issuing organization
- `title`: Credential name (with i18n syntax)
- `level`: Rank or level achieved
- `score`: Achievement score
- `issuedOn`: Date issued (YYYY-MM format)
- `topics`: Tags (cybersecurity, devops, ai, cloud, etc.)
- `skills`: List of skills gained
- `image`: Path to credential image
- `link`: Verification URL or PDF
- `description`: Bilingual description (en/es)

### manage_credentials.py

A CLI tool for managing credentials data:

```bash
python scripts/manage_credentials.py add          # Add new credential (interactive)
python scripts/manage_credentials.py list        # List all credentials
python scripts/manage_credentials.py list --sort year    # Sort by year
python scripts/manage_credentials.py list --type certification  # Filter by type
python scripts/manage_credentials.py get <id>    # View specific credential
python scripts/manage_credentials.py delete <id>  # Delete credential
python scripts/manage_credentials.py sort           # Sort credentials by type then date
python scripts/manage_credentials.py generate    # Generate credentials/index.md from JSON
```

After adding or modifying credentials in `credentials.json`, run `generate` to rebuild `credentials/index.md`, then run `make credentials` to build the final HTML.

## Credits

- Unknown Pleasures visualization for 404 page, originally from [Max Halford/procedural-art](https://github.com/MaxHalford/procedural-art/blob/master/3_unknown_pleasures.html)
- 88x31 Button Maker by [sadgrl](https://goblin-heart.net/sadgrl/projects/88x31-button-maker)