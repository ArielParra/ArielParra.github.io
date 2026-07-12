# Ariel Parra Website

A lightweight, dependency-free personal website built with vanilla HTML/CSS/JS. Features a custom Python static site generator, dark mode, and built-in i18n supporting the 4 major languages of the Americas and transatlantic connections (EN, ES, FR, PT).

Built with plain HTML, CSS, and JavaScript—following HTML5 standards without bloated frameworks. Features custom mobile responsiveness, auto language detection, design, animations, and a Python-based static site generator.

## Quick Start

```bash
make              # Build changed pages incrementally
make index        # Build specific page
make sitemap      # Update sitemap.xml
make humans       # Update humans.txt
make clean        # Remove generated HTML
```

## Project Structure

```text
├── Makefile            # Build automation
├── *.md                # Source files with YAML frontmatter
├── scripts/            # Python build and management scripts
│   ├── md2html.py             # Orchestrator for the static site generator
│   ├── md_parser.py           # Markdown parsing logic
│   ├── html_generator.py      # HTML generation logic
│   ├── i18n.py                # Internationalization helper
│   ├── generate_sitemap.py    # Auto-updates sitemap.xml dates
│   ├── update_humans.py       # Auto-updates humans.txt date
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
│   │   ├── projects.json          # All portfolio projects data
│   │   └── projects.schema.json   # JSON Schema for projects validation
│   ├── index.md               # Source markdown
│   └── index.html             # Generated output
├── contact/            # Contact page sources
└── credentials/        # Credentials page sources
    ├── data/
    │   ├── credentials.json         # All credentials data (education, certs, etc.)
    │   └── credentials.schema.json  # JSON Schema for credentials validation
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

- **No dependencies for core website**: Vanilla HTML, CSS, JavaScript
- **Lightweight**: No frameworks, no bundlers for the frontend.
- **Custom site generator**: Python-based generator (`md2html.py`, `md_parser.py`, `html_generator.py`)
- **Theming**: Manual light/dark mode support
- **Internationalization**: Auto language detection and full translation support for the 4 most spoken languages in the Americas (North and South America) and transatlantic connections to Europe and the rest of the world (English, Spanish, French, and Portuguese).
- **Responsive**: Custom mobile-first design
- **Animated**: Subtle CSS animations

## Quality Assurance & Validation

To maintain high code quality and standard compliance, the project includes an automated linting and validation pipeline:

- **HTML & CSS Validation**: Uses `scripts/validate.py` to check all generated HTML and CSS files against the official W3C Validation APIs (Nu HTML Checker & Jigsaw CSS Validator). Gracefully handles rate limits.
- **Lighthouse Auditing**: Uses Google's Lighthouse (`npx lighthouse`) to automatically audit performance, accessibility, best practices, and SEO. Generates an HTML report during validation.
- **Cross-Browser UI Testing**: Uses **Playwright** (`test_firefox.py`) to run headless tests in the Firefox Gecko engine, ensuring perfect layout stability and zero console errors across different browsers.
- **JavaScript Linting**: Uses **ESLint** with a relaxed `airbnb-base` configuration tailored for a vanilla global-scope architecture.
- **Python Linting**: Uses **Flake8** to enforce PEP8 standards and **Autopep8** for automatic formatting of the custom CLI tools.
- **JSON Schema Validation**: Uses `scripts/validate_json.py` to validate `projects.json` and `credentials.json` against their respective schemas.

Run the full validation suite using:

```bash
make validate  # Validates HTML/CSS via W3C and runs Lighthouse
make lint      # Lints JS via ESLint, Python via Flake8, and validates JSON schemas
```

## Credentials Management

The site uses a JSON-based data source for credentials, processed into HTML by `manage_credentials.py`.

### credentials.json

Contains all education records, certifications, certificates, and badges organized by type:

- `type`: Category (education, certification, certificate, badge, award)
- `issuer`: Issuing organization
- `title`: Credential name (with i18n syntax)
- `level`: Rank or level achieved
- `score`: Achievement score
- `startedOn`: (Optional) Date started, useful for ongoing education (YYYY-MM format)
- `issuedOn`: Date issued or completed (YYYY-MM format)
- `expiresOn`: (Optional) Date credential expires (YYYY-MM format)
- `topics`: Tags (cybersecurity, devops, ai, cloud, etc.)
- `skills`: List of skills gained
- `image`: Path to credential image
- `link`: Verification URL or PDF
- `description`: Multilingual description (en/es/fr/pt)

### manage_credentials.py

A CLI tool for managing credentials data:

```bash
python scripts/manage_credentials.py list        # List all credentials
python scripts/manage_credentials.py list --sort year    # Sort by year
python scripts/manage_credentials.py list --type certification  # Filter by type
python scripts/manage_credentials.py get <id>    # View specific credential
python scripts/manage_credentials.py delete <id>  # Delete credential
python scripts/manage_credentials.py sort           # Sort credentials by type then date
python scripts/manage_credentials.py generate    # Generate credentials/index.md from JSON
```

After adding or modifying credentials in `credentials.json`, run `generate` to rebuild `credentials/index.md`, then run `make credentials` to build the final HTML.

## Portfolio Projects Management

Similar to credentials, the portfolio uses a JSON-based data source, processed into HTML by `manage_portfolio.py`.

### projects.json

Contains all your portfolio projects:

- `id`: Unique identifier for the project
- `title`: Project name
- `date`: Project date (YYYY-MM format)
- `technologies`: Array of technology tags used in the project
- `description`: Multilingual description (en/es/fr/pt)
- `image`: Path or URL to project preview image/gif
- `link`: URL to the project repository or live demo

### manage_portfolio.py

A CLI tool for managing portfolio data:

```bash
python scripts/manage_portfolio.py list         # List all projects
python scripts/manage_portfolio.py get <id>     # View specific project
python scripts/manage_portfolio.py delete <id>  # Delete project
python scripts/manage_portfolio.py sort         # Sort projects alphabetically
python scripts/manage_portfolio.py generate     # Generate portfolio/index.md from JSON
```

After adding or modifying projects in `projects.json`, run `generate` to rebuild `portfolio/index.md`, then run `make portfolio` to build the final HTML.

## Credits

- Unknown Pleasures visualization for 404 page, originally from [Max Halford/procedural-art](https://github.com/MaxHalford/procedural-art/blob/master/3_unknown_pleasures.html)
- 88x31 Button Maker by [sadgrl](https://goblin-heart.net/sadgrl/projects/88x31-button-maker)
- Favicon Space Invader imagery inspired by Taito and French street artist Invader under fair use, made using [LibreSprite](https://libresprite.github.io/)
