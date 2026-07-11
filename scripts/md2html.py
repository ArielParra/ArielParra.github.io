"""
Author: Ariel Parra
"""
import argparse
from md_parser import parse_md
from html_generator import generate_html


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to HTML.')
    parser.add_argument('input_file', type=str, help='Input markdown file')
    parser.add_argument('output_file', type=str, help='Output HTML file')
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    md_parts = md_text.split('---', 2)
    if len(md_parts) == 3:
        md_header = md_parts[1].strip()
        md_content = md_parts[2]
    else:
        raise ValueError(
            "Invalid markdown format. Ensure the file starts with a header block delimited by '---'.")

    md_dict = parse_md(md_header)
    html_content = generate_html(md_dict, md_content)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == '__main__':
    main()
