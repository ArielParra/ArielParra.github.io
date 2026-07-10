# Product

Ariel Parra's personal website — a lightweight, framework-free portfolio hosted at [arielparra.github.io](https://arielparra.github.io).

## Purpose

Showcases the owner's portfolio projects, credentials (certifications, education, awards), and contact information. Supports English/Spanish bilingual content with auto language detection.

## Key Principles

- **KISS philosophy**: No frontend frameworks, no bundlers, no unnecessary dependencies
- **Vanilla stack**: Plain HTML, CSS, and JavaScript only for the frontend
- **Bilingual by default**: Every user-facing string must support both English (`en`) and Spanish (`es`)
- **Standards-compliant**: HTML and CSS must pass W3C validation; JS must pass ESLint (airbnb-base)
- **Privacy-respecting**: Minimal external requests; no analytics or tracking

## Pages

| Page | Source | Description |
|------|--------|-------------|
| Home | `index.md` | Bio, skills, philosophy |
| Portfolio | `portfolio/index.md` | Project cards generated from `projects.json` |
| Credentials | `credentials/index.md` | Cards generated from `credentials.json` |
| Contact | `contact/index.md` | Contact information |
| 404 | `404.md` | Custom error page with animated visualization |
