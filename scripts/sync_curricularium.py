#!/usr/bin/env python3
"""
Sync canonical career records from Curricularium (private/career-data.tex)
into ArielParra.github.io JSON data files (credentials.json & projects.json).

Merges by stable record ID:
- Curricularium owns core facts: title, organization/issuer, date, English
  description, and link (when provided in .tex).
- Website JSON keeps presentation & i18n fields: translations (es/fr/pt),
  images, topic/technology tags, level, score, startedOn, expiresOn, skills.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_TEX_PATH = ROOT_DIR.parent / "Curricularium" / "private" / "career-data.tex"
CREDENTIALS_JSON = ROOT_DIR / "credentials" / "data" / "credentials.json"
PROJECTS_JSON = ROOT_DIR / "portfolio" / "data" / "projects.json"

CREDENTIAL_TYPES = {"education", "credential", "award"}
ISO_DATE_RE = re.compile(r"^\d{4}(?:-\d{2}(?:-\d{2})?)?$")
SKIP_ID_PREFIXES = (
    "original-",
    "european-source-",
    "european-sidebar-",
    "business-card-",
    "resume-contact",
)


def unescape_latex(text):
    """Convert basic LaTeX escapes and \\href links to Markdown/plain text."""
    text = re.sub(r"\\href\{([^}]+)\}\{([^}]+)\}", r"[\2](\1)", text)
    for latex_esc, plain in (
        (r"\&", "&"),
        (r"\%", "%"),
        (r"\_", "_"),
        (r"\#", "#"),
    ):
        text = text.replace(latex_esc, plain)
    return text


def escape_latex(text):
    """Escape special LaTeX characters and convert Markdown http(s) links to \\href."""
    for plain, latex_esc in (
        ("&", r"\&"),
        ("%", r"\%"),
        ("_", r"\_"),
        ("#", r"\#"),
    ):
        text = text.replace(plain, latex_esc)
    return re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\\href{\2}{\1}", text)


def json_to_career_entry(item, kind):
    """Format a credentials.json or projects.json item as a \\CareerEntry line."""
    eid = item["id"]
    if kind == "credential":
        raw_type = item.get("type", "credential")
        entry_type = raw_type if raw_type in {"education", "award"} else "credential"
        raw_title = item.get("title", "")
        title_en = raw_title.get("en", "") if isinstance(raw_title, dict) else raw_title
        org_val = item.get("issuer", "")
        date_val = item.get("issuedOn", "")
        source_val = "credentials/data/credentials.json"
    else:
        entry_type = "project"
        title_en = item.get("title", "")
        org_val = ""
        date_val = item.get("date", "")
        source_val = "portfolio/data/projects.json"

    raw_desc = item.get("description", "")
    desc_en = raw_desc.get("en", "") if isinstance(raw_desc, dict) else raw_desc
    link_val = item.get("link", "")

    parts = [
        f"title={{{escape_latex(title_en)}}}",
        f"organization={{{escape_latex(org_val)}}}",
        f"date={{{escape_latex(date_val)}}}",
        f"description={{{escape_latex(desc_en)}}}",
    ]
    if isinstance(link_val, str) and link_val.startswith(("http://", "https://")):
        parts.append(f"link={{{escape_latex(link_val)}}}")
    parts.append(f"source={{{source_val}}}")
    return f"\\CareerEntry{{{entry_type}}}{{{eid}}}{{{','.join(parts)}}}"


def recover_to_tex(output_path, creds_data, projs_data, dry_run=False):
    """Recover or backfill career-data.tex from credentials.json and projects.json."""
    creds_list = creds_data.get("credentials", [])
    projs_list = projs_data.get("projects", [])
    header = (
        "% Recovered from ArielParra.github.io JSON data; verify and add private contact details as needed.\n"
        "\\CareerProfile{name={Ariel Emilio Parra Martínez},first-name={Ariel Emilio},"
        "last-name={Parra Martínez},website={arielparra.github.io},"
        "linkedin={parra-ariel},github={ArielParra}}\n"
    )

    if output_path.exists():
        existing_text = output_path.read_text(encoding="utf-8")
        existing_ids = {e["id"] for e in parse_career_entries(existing_text)}
        new_lines = []
        creds_added = 0
        projs_added = 0
        for item in creds_list:
            if item.get("id") and item["id"] not in existing_ids:
                new_lines.append(json_to_career_entry(item, "credential"))
                existing_ids.add(item["id"])
                creds_added += 1
        for item in projs_list:
            if item.get("id") and item["id"] not in existing_ids:
                new_lines.append(json_to_career_entry(item, "project"))
                existing_ids.add(item["id"])
                projs_added += 1
        if new_lines and not dry_run:
            sep = "" if existing_text.endswith("\n") else "\n"
            output_path.write_text(
                existing_text + sep + "\n".join(new_lines) + "\n",
                encoding="utf-8",
            )
        return {"mode": "backfill", "creds_added": creds_added, "projs_added": projs_added}

    lines = [json_to_career_entry(item, "credential") for item in creds_list if item.get("id")]
    lines.extend(json_to_career_entry(item, "project") for item in projs_list if item.get("id"))
    if not dry_run:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
    return {
        "mode": "full",
        "creds_added": sum(1 for item in creds_list if item.get("id")),
        "projs_added": sum(1 for item in projs_list if item.get("id")),
    }


def _read_braced(text, pos):
    """Read one brace-delimited argument starting at or before '{'."""
    length = len(text)
    while pos < length and text[pos].isspace():
        pos += 1
    if pos >= length or text[pos] != "{":
        raise ValueError(f"Expected '{{' at offset {pos}")
    depth = 1
    start = pos + 1
    pos += 1
    while pos < length and depth > 0:
        if text[pos] == "\\" and pos + 1 < length:
            pos += 2
            continue
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
        pos += 1
    if depth != 0:
        raise ValueError(f"Unclosed '{{' starting at offset {start - 1}")
    return text[start:pos - 1], pos


def _parse_kv(kv_str):
    """Parse key={value} or key=value pairs from a \\CareerEntry payload."""
    fields = {}
    pos = 0
    length = len(kv_str)
    while pos < length:
        while pos < length and (kv_str[pos].isspace() or kv_str[pos] == ","):
            pos += 1
        if pos >= length:
            break
        eq = kv_str.find("=", pos)
        if eq == -1:
            break
        key = kv_str[pos:eq].strip()
        pos = eq + 1
        while pos < length and kv_str[pos].isspace():
            pos += 1
        if pos < length and kv_str[pos] == "{":
            val, pos = _read_braced(kv_str, pos)
        else:
            comma = kv_str.find(",", pos)
            if comma == -1:
                val = kv_str[pos:].strip()
                pos = length
            else:
                val = kv_str[pos:comma].strip()
                pos = comma + 1
        fields[key] = val
    return fields


def parse_career_entries(tex_content):
    """Parse all \\CareerEntry{type}{id}{fields} records from LaTeX text."""
    entries = []
    marker = r"\CareerEntry"
    idx = 0
    while True:
        found = tex_content.find(marker, idx)
        if found == -1:
            break
        pos = found + len(marker)
        entry_type, pos = _read_braced(tex_content, pos)
        entry_id, pos = _read_braced(tex_content, pos)
        kv_raw, pos = _read_braced(tex_content, pos)
        fields = _parse_kv(kv_raw)
        entries.append(
            {
                "id": entry_id.strip(),
                "type": entry_type.strip(),
                "title": unescape_latex(fields.get("title", "")),
                "organization": unescape_latex(fields.get("organization", "")),
                "date": unescape_latex(fields.get("date", "")),
                "description": unescape_latex(fields.get("description", "")),
                "link": unescape_latex(fields.get("link", "")),
                "source": unescape_latex(fields.get("source", "")),
            }
        )
        idx = pos
    return entries


def _should_add_new(entry, target_kind, include_new):
    """Decide whether an entry absent from JSON should be created."""
    eid = entry["id"]
    if eid.startswith(SKIP_ID_PREFIXES) or eid == "amazon-role":
        return False
    source = entry["source"]
    if target_kind == "credential":
        if source == "credentials/data/credentials.json":
            return True
        return include_new and entry["type"] in CREDENTIAL_TYPES and bool(
            ISO_DATE_RE.match(entry["date"])
        )
    if target_kind == "project":
        if source == "portfolio/data/projects.json":
            return True
        return include_new and entry["type"] == "project" and bool(
            ISO_DATE_RE.match(entry["date"])
        )
    return False


def _sync_credential_item(item, entry):
    """Update a credential dict in place from a CareerEntry; return True if changed."""
    changed = False
    if entry["organization"] and item.get("issuer") != entry["organization"]:
        item["issuer"] = entry["organization"]
        changed = True
    if entry["date"] and item.get("issuedOn") != entry["date"]:
        item["issuedOn"] = entry["date"]
        changed = True

    title_val = item.get("title")
    if isinstance(title_val, dict):
        if entry["title"] and title_val.get("en") != entry["title"]:
            title_val["en"] = entry["title"]
            changed = True
    elif entry["title"] and title_val != entry["title"]:
        item["title"] = entry["title"]
        changed = True

    desc_val = item.get("description")
    if isinstance(desc_val, dict):
        if entry["description"] and desc_val.get("en") != entry["description"]:
            desc_val["en"] = entry["description"]
            changed = True
    elif entry["description"]:
        item["description"] = {"en": entry["description"], "es": entry["description"]}
        changed = True

    if entry["link"] and item.get("link") != entry["link"]:
        item["link"] = entry["link"]
        changed = True
    return changed


def _sync_project_item(item, entry):
    """Update a project dict in place from a CareerEntry; return True if changed."""
    changed = False
    if entry["title"] and item.get("title") != entry["title"]:
        item["title"] = entry["title"]
        changed = True
    if entry["date"] and item.get("date") != entry["date"]:
        item["date"] = entry["date"]
        changed = True

    desc_val = item.get("description")
    if isinstance(desc_val, dict):
        if entry["description"] and desc_val.get("en") != entry["description"]:
            desc_val["en"] = entry["description"]
            changed = True
    elif entry["description"]:
        item["description"] = {"en": entry["description"], "es": entry["description"]}
        changed = True

    if entry["link"] and item.get("link") != entry["link"]:
        item["link"] = entry["link"]
        changed = True
    return changed


def _new_credential_item(entry):
    """Build a schema-valid credential object for a newly synced CareerEntry."""
    cred_type = entry["type"]
    if cred_type == "credential":
        cred_type = "certificate"
    return {
        "id": entry["id"],
        "type": cred_type,
        "issuer": entry["organization"] or "Unknown",
        "title": entry["title"],
        "level": "",
        "score": "",
        "issuedOn": entry["date"] or "",
        "expiresOn": "",
        "topics": [],
        "skills": [],
        "image": "",
        "link": entry["link"],
        "description": {
            "en": entry["description"],
            "es": entry["description"],
        },
    }


def _new_project_item(entry):
    """Build a schema-valid project object for a newly synced CareerEntry."""
    return {
        "id": entry["id"],
        "title": entry["title"],
        "date": entry["date"],
        "technologies": [],
        "description": {
            "en": entry["description"],
            "es": entry["description"],
        },
        "image": "",
        "link": entry["link"],
    }


def sync_datasets(entries, creds_data, projs_data, include_new=False):
    """Merge CareerEntry records into credentials and projects JSON dicts."""
    creds_list = creds_data.setdefault("credentials", [])
    projs_list = projs_data.setdefault("projects", [])
    creds_by_id = {c["id"]: c for c in creds_list if "id" in c}
    projs_by_id = {p["id"]: p for p in projs_list if "id" in p}

    stats = {
        "creds_matched": 0,
        "creds_updated": 0,
        "creds_added": 0,
        "projs_matched": 0,
        "projs_updated": 0,
        "projs_added": 0,
    }

    for entry in entries:
        eid = entry["id"]
        if eid in creds_by_id:
            stats["creds_matched"] += 1
            if _sync_credential_item(creds_by_id[eid], entry):
                stats["creds_updated"] += 1
        elif _should_add_new(entry, "credential", include_new):
            new_item = _new_credential_item(entry)
            creds_list.append(new_item)
            creds_by_id[eid] = new_item
            stats["creds_added"] += 1

        if eid in projs_by_id:
            stats["projs_matched"] += 1
            if _sync_project_item(projs_by_id[eid], entry):
                stats["projs_updated"] += 1
        elif _should_add_new(entry, "project", include_new):
            new_item = _new_project_item(entry)
            projs_list.append(new_item)
            projs_by_id[eid] = new_item
            stats["projs_added"] += 1

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Sync Curricularium career-data.tex into website JSON files."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_TEX_PATH,
        help="Path to Curricularium career-data.tex",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report planned updates without writing JSON files",
    )
    parser.add_argument(
        "--include-new",
        action="store_true",
        help="Also add new non-template CareerEntry records with ISO dates",
    )
    parser.add_argument(
        "--export-json",
        type=Path,
        help="Optional path to export all parsed CareerEntry records as JSON",
    )
    parser.add_argument(
        "--recover",
        action="store_true",
        help="Recover or backfill career-data.tex from website JSON files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output .tex path for --recover (defaults to --source)",
    )
    args = parser.parse_args()

    creds_raw = CREDENTIALS_JSON.read_text(encoding="utf-8")
    projs_raw = PROJECTS_JSON.read_text(encoding="utf-8")
    creds_data = json.loads(creds_raw)
    projs_data = json.loads(projs_raw)

    if args.recover:
        target_tex = args.output or args.source
        result = recover_to_tex(target_tex, creds_data, projs_data, dry_run=args.dry_run)
        mode = " [dry-run]" if args.dry_run else ""
        print(
            f"Recovered ({result['mode']}) to {target_tex}{mode}: "
            f"credentials added={result['creds_added']}; "
            f"projects added={result['projs_added']}"
        )
        return 0

    if not args.source.exists():
        print(f"Error: source database not found: {args.source}", file=sys.stderr)
        return 1

    tex_content = args.source.read_text(encoding="utf-8")
    entries = parse_career_entries(tex_content)

    if args.export_json:
        args.export_json.parent.mkdir(parents=True, exist_ok=True)
        args.export_json.write_text(
            json.dumps({"entries": entries}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Exported {len(entries)} entries to {args.export_json}")

    stats = sync_datasets(entries, creds_data, projs_data, include_new=args.include_new)

    creds_changed = stats["creds_updated"] > 0 or stats["creds_added"] > 0
    projs_changed = stats["projs_updated"] > 0 or stats["projs_added"] > 0

    if not args.dry_run:
        if creds_changed:
            CREDENTIALS_JSON.write_text(
                json.dumps(creds_data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        if projs_changed:
            PROJECTS_JSON.write_text(
                json.dumps(projs_data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    mode = " [dry-run]" if args.dry_run else ""
    print(
        f"Synced from {args.source}{mode}: "
        f"credentials matched={stats['creds_matched']} "
        f"(updated={stats['creds_updated']}, added={stats['creds_added']}); "
        f"projects matched={stats['projs_matched']} "
        f"(updated={stats['projs_updated']}, added={stats['projs_added']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
