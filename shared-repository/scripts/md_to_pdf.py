#!/usr/bin/env python3
"""Markdown to PDF converter for Recoveri review packs.

Uses markdown + weasyprint. Produces clean, mobile-readable PDFs.
"""

import sys
import os
import markdown
from weasyprint import HTML

CSS = """
@page {
    margin: 2cm;
    size: A4;
    @bottom-center {
        content: "RECOVERI — Confidential";
        font-size: 8pt;
        color: #999;
    }
}
body {
    font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #222;
    max-width: 100%;
}
h1 { font-size: 18pt; color: #1a1a2e; border-bottom: 2px solid #1a1a2e; padding-bottom: 6px; }
h2 { font-size: 14pt; color: #16213e; margin-top: 1.5em; }
h3 { font-size: 12pt; color: #0f3460; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 10pt; }
th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; }
th { background-color: #f0f0f0; font-weight: bold; }
tr:nth-child(even) { background-color: #fafafa; }
code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-size: 10pt; }
pre { background: #f4f4f4; padding: 12px; border-radius: 5px; overflow-x: auto; font-size: 9pt; }
blockquote { border-left: 3px solid #1a1a2e; margin-left: 0; padding-left: 1em; color: #555; }
hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
ul, ol { padding-left: 1.5em; }
"""

EXTENSIONS = ['tables', 'fenced_code', 'codehilite', 'toc', 'sane_lists']


def convert(input_path, output_path=None):
    """Convert a markdown file to PDF."""
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '.pdf'

    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=EXTENSIONS)
    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{html_content}</body></html>"""

    HTML(string=full_html).write_pdf(output_path)
    return output_path


def convert_batch(input_dir, output_dir, pattern=None):
    """Convert all .md files in a directory to PDF."""
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for fname in sorted(os.listdir(input_dir)):
        if not fname.endswith('.md'):
            continue
        if pattern and pattern not in fname:
            continue

        input_path = os.path.join(input_dir, fname)
        output_name = os.path.splitext(fname)[0] + '.pdf'
        output_path = os.path.join(output_dir, output_name)

        try:
            convert(input_path, output_path)
            size_kb = os.path.getsize(output_path) / 1024
            results.append((fname, output_name, size_kb, 'OK'))
            print(f"  OK: {fname} -> {output_name} ({size_kb:.0f} KB)")
        except Exception as e:
            results.append((fname, None, 0, str(e)))
            print(f"  FAIL: {fname} -> {e}")

    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: md_to_pdf.py <input.md> [output.pdf]")
        print("       md_to_pdf.py --batch <input_dir> <output_dir> [pattern]")
        sys.exit(1)

    if sys.argv[1] == '--batch':
        input_dir = sys.argv[2]
        output_dir = sys.argv[3]
        pattern = sys.argv[4] if len(sys.argv) > 4 else None
        results = convert_batch(input_dir, output_dir, pattern)
        print(f"\nConverted {sum(1 for r in results if r[3] == 'OK')}/{len(results)} files.")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        result = convert(input_path, output_path)
        print(f"Created: {result}")
