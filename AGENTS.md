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
---

content here
```

## i18n Syntax

```markdown
((en))English text((/en))((es))Texto en español((/es))
```

## Key Files

- `md2html.py` - HTML generator (507 lines)
- `style.css` - All styling
- `js/` - JavaScript modules
- `index.md`, `portfolio/`, `contact/`, `credentials/` - Content sources