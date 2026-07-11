#!/usr/bin/env python3
import datetime
import re
from pathlib import Path


def main():
    root_dir = Path(__file__).resolve().parent.parent
    humans_file = root_dir / "humans.txt"

    if not humans_file.exists():
        print(f"{humans_file.name} not found.")
        return

    with open(humans_file, 'r', encoding='utf-8') as f:
        content = f.read()

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Regex to find and replace the "Last update: YYYY-MM-DD" line
    new_content = re.sub(r'Last update: \d{4}-\d{2}-\d{2}', f'Last update: {today}', content)

    if new_content != content:
        with open(humans_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {humans_file.name} with today's date ({today}).")
    else:
        print(f"{humans_file.name} is already up to date.")


if __name__ == '__main__':
    main()
