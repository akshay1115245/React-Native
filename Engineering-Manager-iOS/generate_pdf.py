#!/usr/bin/env python3
"""Combine all Markdown files into a single styled PDF."""

import markdown2
import sys
import os
from pathlib import Path

# All docs in reading order
DOCS = [
    ("README.md", "Engineering Manager - iOS: Complete Roadmap"),
    ("01-ios-technical-depth.md", "iOS Technical Depth"),
    ("02-management-playbook.md", "Management Playbook"),
    ("03-system-design-mobile.md", "Mobile System Design"),
    ("04-interview-preparation.md", "Interview Preparation"),
    ("05-skill-building-plan.md", "Skill-Building Plan"),
]

BASE_DIR = Path(__file__).parent

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

@page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-right {
        content: counter(page);
        font-size: 9pt;
        color: #9ca3af;
        font-family: Inter, sans-serif;
    }
}

body {
    font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 10pt;
    line-height: 1.65;
    color: #1f2937;
    background: #ffffff;
}

/* Cover page */
.cover-page {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 260mm;
    text-align: center;
    background: linear-gradient(160deg, #0f172a 0%, #1e3a5f 60%, #1d4ed8 100%);
    color: white;
    padding: 40px;
    margin: -18mm -16mm 0 -16mm;
}

.cover-page .cover-icon {
    font-size: 64pt;
    margin-bottom: 24px;
}

.cover-page h1 {
    font-size: 30pt;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 12px;
    line-height: 1.2;
    letter-spacing: -0.5px;
}

.cover-page .cover-subtitle {
    font-size: 14pt;
    color: #93c5fd;
    margin-bottom: 32px;
}

.cover-page .cover-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-bottom: 40px;
}

.cover-page .pill {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.25);
    color: #e0f2fe;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 9pt;
}

.cover-page .cover-meta {
    font-size: 9pt;
    color: #93c5fd;
    border-top: 1px solid rgba(255,255,255,0.15);
    padding-top: 20px;
    width: 100%;
}

/* Chapter separator */
.chapter-separator {
    page-break-before: always;
    background: linear-gradient(135deg, #1e3a5f 0%, #1d4ed8 100%);
    color: white;
    padding: 28px 32px;
    margin: -18mm -16mm 32px -16mm;
    display: flex;
    align-items: center;
    gap: 16px;
}

.chapter-number {
    font-size: 36pt;
    font-weight: 700;
    opacity: 0.25;
    line-height: 1;
    font-family: Inter, sans-serif;
}

.chapter-title {
    font-size: 18pt;
    font-weight: 700;
    line-height: 1.2;
}

/* Headings */
h1 {
    font-size: 20pt;
    font-weight: 700;
    color: #0f172a;
    margin: 28px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 2.5px solid #1d4ed8;
    line-height: 1.25;
    page-break-after: avoid;
}

h2 {
    font-size: 14pt;
    font-weight: 700;
    color: #1e3a5f;
    margin: 24px 0 10px 0;
    padding-left: 10px;
    border-left: 4px solid #1d4ed8;
    page-break-after: avoid;
}

h3 {
    font-size: 11pt;
    font-weight: 600;
    color: #1d4ed8;
    margin: 18px 0 8px 0;
    page-break-after: avoid;
}

h4 {
    font-size: 10pt;
    font-weight: 600;
    color: #374151;
    margin: 14px 0 6px 0;
    page-break-after: avoid;
}

/* Paragraphs */
p {
    margin-bottom: 10px;
}

/* Lists */
ul, ol {
    margin: 8px 0 12px 20px;
}

li {
    margin-bottom: 4px;
}

/* Code */
code {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}

pre {
    background: #0f172a;
    color: #e2e8f0;
    padding: 14px 16px;
    border-radius: 8px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 8pt;
    line-height: 1.55;
    overflow-x: auto;
    margin: 12px 0 16px 0;
    page-break-inside: avoid;
    border-left: 3px solid #1d4ed8;
}

pre code {
    background: none;
    color: #e2e8f0;
    border: none;
    padding: 0;
    font-size: 8pt;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 9pt;
    page-break-inside: avoid;
}

thead tr {
    background: #1e3a5f;
    color: white;
}

th {
    padding: 8px 10px;
    text-align: left;
    font-weight: 600;
    font-size: 8.5pt;
}

td {
    padding: 7px 10px;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
}

tbody tr:nth-child(even) {
    background: #f8fafc;
}

tbody tr:hover {
    background: #eff6ff;
}

/* Blockquotes */
blockquote {
    border-left: 4px solid #3b82f6;
    margin: 12px 0;
    padding: 10px 16px;
    background: #eff6ff;
    color: #1e3a5f;
    border-radius: 0 6px 6px 0;
    font-style: italic;
}

blockquote p { margin: 0; }

/* Horizontal rules */
hr {
    border: none;
    border-top: 1.5px solid #e2e8f0;
    margin: 20px 0;
}

/* Checkboxes in task lists */
input[type="checkbox"] {
    margin-right: 6px;
}

/* Strong / bold */
strong {
    color: #0f172a;
    font-weight: 700;
}

/* Callout-style blockquotes that start with > */
blockquote strong:first-child {
    color: #1d4ed8;
}

/* TOC */
.toc-section {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 20px 24px;
    margin: 16px 0 24px 0;
}

.toc-section h2 {
    border: none;
    padding: 0;
    margin: 0 0 12px 0;
    color: #0f172a;
    font-size: 12pt;
}
"""

def md_to_html(md_path: Path) -> str:
    content = md_path.read_text(encoding="utf-8")
    html = markdown2.markdown(
        content,
        extras=[
            "tables",
            "fenced-code-blocks",
            "strike",
            "task_list",
            "header-ids",
            "break-on-newline",
        ],
    )
    return html


def build_combined_html() -> str:
    parts = []

    # Cover page
    parts.append("""
<div class="cover-page">
  <div class="cover-icon">🍎</div>
  <h1>Engineering Manager<br>iOS</h1>
  <p class="cover-subtitle">Complete Career Roadmap &amp; Interview Preparation Guide</p>
  <div class="cover-pills">
    <span class="pill">Swift &amp; Objective-C</span>
    <span class="pill">UIKit &amp; SwiftUI</span>
    <span class="pill">Architecture Patterns</span>
    <span class="pill">Swift Concurrency</span>
    <span class="pill">Performance Optimization</span>
    <span class="pill">CI/CD &amp; DevOps</span>
    <span class="pill">People Management</span>
    <span class="pill">Hiring &amp; Onboarding</span>
    <span class="pill">System Design</span>
    <span class="pill">STAR Interview Stories</span>
    <span class="pill">30-60-90 Day Plan</span>
    <span class="pill">Skill-Building Roadmap</span>
  </div>
  <div class="cover-meta">
    6 Documents · 3,700+ Lines · Basic to Advanced · Apple · Google · Meta · Amazon
  </div>
</div>
""")

    chapter_icons = ["📖", "⚙️", "👥", "🏗️", "🎯", "📋"]

    for idx, (filename, title) in enumerate(DOCS):
        md_path = BASE_DIR / filename
        if not md_path.exists():
            print(f"Warning: {md_path} not found, skipping.", file=sys.stderr)
            continue

        chapter_num = str(idx + 1).zfill(2)
        icon = chapter_icons[idx]

        parts.append(f"""
<div class="chapter-separator">
  <div class="chapter-number">{chapter_num}</div>
  <div>
    <div style="font-size:9pt;opacity:0.7;margin-bottom:4px;">{icon} Chapter {idx+1}</div>
    <div class="chapter-title">{title}</div>
  </div>
</div>
""")
        parts.append(md_to_html(md_path))

    body = "\n".join(parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Engineering Manager - iOS: Complete Roadmap</title>
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""


def main():
    output_pdf = BASE_DIR / "Engineering-Manager-iOS-Complete-Roadmap.pdf"
    output_html = BASE_DIR / "_combined.html"

    print("Building combined HTML...", file=sys.stderr)
    html = build_combined_html()
    output_html.write_text(html, encoding="utf-8")
    print(f"HTML written: {output_html}", file=sys.stderr)

    print("Generating PDF with WeasyPrint...", file=sys.stderr)
    try:
        from weasyprint import HTML, CSS as WeasyCss
        HTML(filename=str(output_html)).write_pdf(str(output_pdf))
        print(f"PDF written: {output_pdf}", file=sys.stderr)
    except Exception as e:
        print(f"WeasyPrint error: {e}", file=sys.stderr)
        sys.exit(1)

    # Clean up temp HTML
    output_html.unlink()
    print(f"Done! PDF size: {output_pdf.stat().st_size // 1024} KB", file=sys.stderr)


if __name__ == "__main__":
    main()
