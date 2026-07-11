#!/usr/bin/env python3
"""
Validation script for HTML and CSS using W3C APIs.
Requires no external dependencies (only standard library).
"""
import json
import urllib.request
import urllib.parse
from pathlib import Path
import sys


def validate_html(file_path):
    print(f"Validating HTML: {file_path}")
    url = "https://validator.w3.org/nu/?out=json"

    with open(file_path, "rb") as f:
        data = f.read()

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "text/html; charset=utf-8")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            messages = result.get('messages', [])
            errors = [m for m in messages if m.get('type') == 'error']
            warnings = [m for m in messages if m.get('type') == 'info' and m.get('subType') == 'warning']
            # Filter out false-positive CSP warnings caused by validating local files without an origin
            warnings = [m for m in warnings if "Content Security Policy" not in m.get('message', '')]

            if not errors and not warnings:
                print("  ✅ Passed")
                return True

            for m in errors:
                line = m.get('lastLine', '?')
                print(f"  ❌ ERROR (Line {line}): {m.get('message')}")
            for m in warnings:
                line = m.get('lastLine', '?')
                print(f"  ⚠️  WARNING (Line {line}): {m.get('message')}")

            return len(errors) == 0
    except Exception as e:
        print(f"  ❌ Failed to connect or validate: {e}")
        return False


def validate_css(file_path):
    print(f"Validating CSS: {file_path}")
    url = "https://jigsaw.w3.org/css-validator/validator"

    with open(file_path, "r", encoding="utf-8") as f:
        css_text = f.read()

    boundary = "----WebKitFormBoundaryPythonScript"
    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"output\"\r\n\r\n"
        f"json\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"style.css\"\r\n"
        f"Content-Type: text/css\r\n\r\n"
        f"{css_text}\r\n"
        f"--{boundary}--\r\n"
    ).encode('utf-8')

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            css_result = result.get('cssvalidation', {})
            errors = css_result.get('errors', [])

            if not errors:
                print("  ✅ Passed")
                return True

            for e in errors:
                line = e.get('line', '?')
                msg = e.get('message', '').strip()
                print(f"  ❌ ERROR (Line {line}): {msg}")

            return False
    except Exception as e:
        print(f"  ❌ Failed to connect or validate: {e}")
        return False


def main():
    root_dir = Path(__file__).resolve().parent.parent

    # HTML Files
    html_files = list(root_dir.rglob("*.html"))
    html_files = [f for f in html_files if "node_modules" not in str(f) and "templates" not in str(f)]

    # CSS Files
    css_files = list(root_dir.rglob("*.css"))
    css_files = [f for f in css_files if "node_modules" not in str(f)]

    all_passed = True

    print("=== HTML Validation ===")
    for f in html_files:

        if not validate_html(f):
            all_passed = False

    print("\n=== CSS Validation ===")
    for f in css_files:

        if not validate_css(f):
            all_passed = False

    if all_passed:
        print("\n🎉 All HTML and CSS files passed validation!")
        sys.exit(0)
    else:
        print("\n⚠️  Some files failed validation. Check logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
