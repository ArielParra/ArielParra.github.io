#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError


def validate_file(json_path, schema_path):
    print(
        f"Validating JSON: {json_path.relative_to(json_path.parent.parent.parent)}")
    try:
        with open(json_path, 'r', encoding='utf-8') as jf, \
                open(schema_path, 'r', encoding='utf-8') as sf:
            data = json.load(jf)
            schema = json.load(sf)
            validate(instance=data, schema=schema)
            print("  ✅ Passed")
            return True
    except ValidationError as e:
        print(f"  ❌ Validation Error: {e.message}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    base_dir = Path(__file__).resolve().parent.parent

    files_to_validate = [
        (base_dir / "portfolio" / "data" / "projects.json",
         base_dir / "portfolio" / "data" / "projects.schema.json"),
        (base_dir / "credentials" / "data" / "credentials.json",
         base_dir / "credentials" / "data" / "credentials.schema.json")
    ]

    all_passed = True
    print("=== JSON Schema Validation ===")
    for json_path, schema_path in files_to_validate:
        if not json_path.exists():
            print(f"  ⚠️  Warning: {json_path.name} not found. Skipping.")
            continue
        if not schema_path.exists():
            print(f"  ⚠️  Warning: {schema_path.name} not found. Skipping.")
            continue

        if not validate_file(json_path, schema_path):
            all_passed = False

    if all_passed:
        print("🎉 All JSON files passed schema validation!")
        sys.exit(0)
    else:
        print("⚠️  Some JSON files failed validation.")
        sys.exit(1)


if __name__ == '__main__':
    main()
