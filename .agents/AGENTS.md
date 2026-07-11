# AGENTS.md

## Build Commands

```bash
make              # Build changed pages incrementally
make index        # Build specific page
make validate     # Validates HTML and CSS via W3C
make lint         # Lints JS, Python, and validates JSON schemas
make sitemap      # Update sitemap.xml timestamps
make humans       # Update humans.txt timestamp
make clean        # Remove generated HTML
```

## Architecture

- **Source**: `*.md` files with YAML frontmatter (`---key: value---`)
- **Generator**: `scripts/md2html.py` (orchestrator), `scripts/md_parser.py`, `scripts/html_generator.py` - custom Python converter
- **Output**: Static HTML in same directory

## Markdown Format

```markdown
---
title: Page Title
lang: en
base_href: ./
nav_current: 1
js: [main, menu, theme, language]
css: [common, credentials]
---

content here
```

## CSS Architecture

- **CSS Loading Order**: User-specified CSS in `css:` frontmatter
- **Theme** (manually included): `css/theme.css` - color palette, light/dark themes
- **Page-specific CSS**: Explicitly list in `css:` frontmatter

### Example MD Files

- `index.md`: `css: [theme, common]`
- `portfolio/index.md`: `css: [theme, common, portfolio]`
- `credentials/index.md`: `css: [theme, common, credentials]`
- `contact/index.md`: `css: [theme, common]`
- `404.md`: `css: [theme, common, 404]`

### Key CSS Files

- `css/theme.css` - color palette, light/dark themes
- `css/common.css` - base styles (nav, buttons, cards, scrollbar, responsive)
- `css/credentials.css` - credentials card styles
- `css/portfolio.css` - portfolio grid styles
- `css/404.css` - 404 page styles

## i18n Syntax

```markdown
((en))English text((/en))((es))Texto en español((/es))
```

## Key Files

- `scripts/md2html.py` - HTML generator orchestrator
- `scripts/md_parser.py` - Markdown to HTML parsing logic
- `scripts/html_generator.py` - HTML template assembly
- `scripts/generate_sitemap.py` - Generates `sitemap.xml`
- `scripts/update_humans.py` - Updates `humans.txt` date
- `scripts/manage_portfolio.py` - CLI tool for portfolio.json
- `scripts/manage_credentials.py` - CLI tool for credentials.json
- `scripts/base_manager.py` - OOP base class for data managers
- `scripts/validate.py` - W3C HTML/CSS Validator
- `scripts/validate_json.py` - JSON schema validator
- `style.css` - imports css/ folder (backward compatibility)
- `css/` - modular CSS files
- `js/` - JavaScript modules
- `index.md`, `portfolio/`, `contact/`, `credentials/` - Content sources