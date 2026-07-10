# Tech Stack

## Frontend

- **HTML5** — hand-authored and generated; must pass W3C Nu HTML Checker validation
- **CSS3** — modular stylesheets in `css/`; must pass W3C Jigsaw CSS validation
- **JavaScript (ES2021)** — vanilla, no frameworks, no bundlers; files live in `js/`
- **Pixelify Sans** — Google Font loaded via `<link>` in the generated `<head>`

## Build System

- **Make** — `Makefile` at project root drives all builds (cross-platform: Linux/macOS and Windows)
- **Python 3** — custom static site generator (`scripts/md2html.py`) converts `.md` → `.html`

## Tooling (dev only)

- **ESLint 8** with `eslint-config-airbnb-base` — JS linting (`npx eslint "js/**/*.js"`)
- **Flake8** — Python linting with PEP8, E501 ignored (`python -m flake8 scripts/ --extend-ignore=E501`)
- **autopep8** — Python auto-formatter for scripts
- **scripts/validate.py** — calls W3C HTML and CSS validation APIs against generated files

## Common Commands

```bash
# Build everything
make

# Build individual pages
make index
make portfolio        # also runs manage_portfolio.py generate first
make credentials      # also runs manage_credentials.py sort + generate first
make contact
make 404

# Validate HTML & CSS via W3C APIs
make validate

# Lint JS (ESLint) and Python (Flake8)
make lint

# Remove all generated HTML files
make clean
```

## Data Management Scripts

```bash
# Portfolio
python scripts/manage_portfolio.py generate   # Rebuild portfolio/index.md from JSON
python scripts/manage_portfolio.py add        # Add new project interactively
python scripts/manage_portfolio.py list       # List all projects
python scripts/manage_portfolio.py sort       # Sort projects alphabetically
python scripts/manage_portfolio.py get <id>   # View one project
python scripts/manage_portfolio.py delete <id>

# Credentials
python scripts/manage_credentials.py generate           # Rebuild credentials/index.md from JSON
python scripts/manage_credentials.py add                # Add new credential interactively
python scripts/manage_credentials.py list               # List all credentials
python scripts/manage_credentials.py list --sort year   # Sort by date
python scripts/manage_credentials.py list --type certification
python scripts/manage_credentials.py sort               # Sort JSON by type then date
python scripts/manage_credentials.py get <id>
python scripts/manage_credentials.py delete <id>
```

## No Runtime Dependencies

The website has zero frontend runtime dependencies. `node_modules/` exists only for ESLint (dev tooling). Do not introduce frontend libraries or bundlers.
