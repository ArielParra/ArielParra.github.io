#!/usr/bin/env python3
"""
Base Manager for Portfolio and Credentials
"""
import json
import sys
from pathlib import Path


class BaseManager:
    def __init__(self, file_path, data_key):
        self.file_path = Path(file_path).resolve()
        self.data_key = data_key  # 'projects' or 'credentials'

    def load_data(self):
        if not self.file_path.exists():
            return {self.data_key: []}
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, data):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved to {self.file_path}")

    def prompt_yesno(self, question):
        while True:
            ans = input(f"{question} [y/n]: ").strip().lower()
            if ans in ('y', 'yes'):
                return True
            if ans in ('n', 'no'):
                return False

    def get_i18n_field(self, value, page_lang='en'):
        """Extract value from i18n object or string"""
        if isinstance(value, dict):
            return value.get(page_lang, value.get('en', ''))
        return value

    def get_i18n_tags(self, value):
        """Get i18n tags string from object or plain value"""
        if isinstance(value, dict):
            en = value.get('en', '')
            es = value.get('es', en)
            if en and es:
                return f"((en)){en}((/en))((es)){es}((/es))"
            return en
        if isinstance(value, str):
            if '((en))' in value or '((es))' in value:
                return value
            return value
        return str(value) if value else ""

    def format_date_i18n(self, date_str):
        """Convert date like 2025-04 to April 2025 / Abril 2025"""
        if not date_str:
            return ""

        en_months = [
            "",
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"]
        es_months = [
            "",
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre"]

        parts = date_str.split("-")
        if len(parts) >= 2:
            year = parts[0]
            try:
                month = int(parts[1])
            except BaseException:
                return date_str
            en_month = en_months[month] if 1 <= month <= 12 else ""
            es_month = es_months[month] if 1 <= month <= 12 else ""

            if en_month and es_month:
                return f"((en)){en_month} {year}((/en))((es)){es_month} {year}((/es))"

        return date_str

    def cmd_delete(self, args):
        data = self.load_data()
        items = data.get(self.data_key, [])

        item_id = args.get('<id>')
        if not item_id:
            print(f"Usage: delete <{self.data_key[:-1]}-id>")
            return 1

        new_items = [item for item in items if item.get('id') != item_id]

        if len(new_items) == len(items):
            print(f"{self.data_key.capitalize()[:-1]} '{item_id}' not found.")
            return 1

        if self.prompt_yesno(f"Delete '{item_id}'?"):
            data[self.data_key] = new_items
            self.save_data(data)
            print(f"Deleted '{item_id}'.")
        else:
            print("Aborted.")
            return 0
        return 0

    # These should be overridden by child classes
    def cmd_add(self, args):
        raise NotImplementedError

    def cmd_list(self, args):
        raise NotImplementedError

    def cmd_sort(self, args):
        raise NotImplementedError

    def cmd_generate(self, args):
        raise NotImplementedError

    def cmd_get(self, args):
        raise NotImplementedError

    def run(self):
        """Generic command dispatcher for CLI"""
        if len(sys.argv) < 2:
            print("Commands: generate, sort, list, add, delete, get")
            return 0

        command = sys.argv[1]
        args = {}
        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg.startswith('--'):
                if i + \
                        1 < len(sys.argv) and not sys.argv[i + 1].startswith('-'):
                    args[arg] = sys.argv[i + 1]
                    i += 2
                else:
                    args[arg] = ""
                    i += 1
            elif arg.startswith('-') and len(arg) > 1:
                args[arg] = ""
                i += 1
            elif arg.isdigit():
                args['<id>'] = arg
                i += 1
            else:
                args['<id>'] = arg
                i += 1

        commands = {
            'add': self.cmd_add,
            'list': self.cmd_list,
            'get': self.cmd_get,
            'delete': self.cmd_delete,
            'sort': self.cmd_sort,
            'generate': self.cmd_generate,
        }

        if command not in commands:
            print(f"Unknown command: {command}")
            return 1

        return commands[command](args)
