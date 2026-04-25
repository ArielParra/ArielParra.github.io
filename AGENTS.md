# AGENTS.md

## Build Commands

```bash
make              # Build all pages
make index        # Build specific page
make clean        # Remove generated HTML
```

## Architecture

- **Source**: `*.md` files with YAML frontmatter (`---key: value---`)
- **Generator**: `md2html.py` - custom Python converter (no dependencies)
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

- `md2html.py` - HTML generator (544 lines)
- `style.css` - imports css/ folder (backward compatibility)
- `css/` - modular CSS files
- `js/` - JavaScript modules
- `index.md`, `portfolio/`, `contact/`, `credentials/` - Content sources