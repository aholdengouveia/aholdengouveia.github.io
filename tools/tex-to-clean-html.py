#!/usr/bin/env python3
"""
Convert LaTeX .tex files to clean, accessible HTML
Similar to the simplified whatisdata.html format
"""

import sys
import re
from pathlib import Path

def extract_title(tex_content):
    """Extract title from \title{} command"""
    match = re.search(r'\\title\{([^}]+)\}', tex_content)
    return match.group(1) if match else "Lab Assignment"

def extract_author_info(tex_content):
    """Extract author information"""
    info = {}

    # Extract name - look for full name with hyphen
    name_match = re.search(r'\\author\{[^}]*?([A-Z][a-z]+\s+[A-Z][a-z]+-[A-Z][a-z]+)', tex_content, re.DOTALL)
    if not name_match:
        # Try without hyphen
        name_match = re.search(r'\\author\{[^}]*?([A-Z][a-z]+\s+[A-Z][a-z]+)', tex_content, re.DOTALL)
    info['name'] = name_match.group(1) if name_match else "Adrianna Holden-Gouveia"

    # Extract website
    website_match = re.search(r'\\url\{(https://[^}]+)\}', tex_content)
    info['website'] = website_match.group(1) if website_match else "https://aholdengouveia.name"

    # Extract GitHub
    github_match = re.search(r'\\faGithub.*?\{:\s*([^}]+)\}', tex_content)
    info['github'] = github_match.group(1).strip() if github_match else "aholdengouveia"

    return info

def convert_section(section_text, section_level='h2'):
    """Convert a section to HTML"""
    # Extract section title
    title_match = re.search(r'\\(?:sub)?section\*?\{([^}]+)\}', section_text)
    if not title_match:
        return ""

    title = title_match.group(1)
    section_id = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

    html = f'<section aria-labelledby="{section_id}">\n'
    html += f'<{section_level} id="{section_id}">{title}</{section_level}>\n'

    # Get content after section title
    content = section_text[title_match.end():]

    # Convert content
    html += convert_content(content)
    html += '</section>\n\n'

    return html

def extract_sections(body):
    """Extract all section titles and IDs for TOC generation"""
    sections = []

    # Find all section headers
    for match in re.finditer(r'\\((?:sub)?section)\*?\{([^}]+)\}', body):
        section_type = match.group(1)
        title = match.group(2)
        section_id = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

        # Determine if it's a subsection
        is_subsection = section_type == 'subsection'

        sections.append({
            'title': title,
            'id': section_id,
            'is_subsection': is_subsection
        })

    return sections

def generate_toc(sections):
    """Generate HTML for table of contents"""
    if not sections:
        return ""

    html = '''        <nav aria-label="Table of Contents" class="toc">
            <h2>On this page:</h2>
            <ul>
'''

    for section in sections:
        if section['is_subsection']:
            # Skip subsections in TOC to keep it concise
            continue
        html += f'                <li><a href="#{section["id"]}">{section["title"]}</a></li>\n'

    html += '''            </ul>
        </nav>

'''

    return html

def convert_content(content):
    """Convert LaTeX content to HTML"""
    html = ""

    # Split into blocks
    blocks = re.split(r'\n\n+', content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Skip blocks that are just environment endings
        if re.match(r'^\\end\{(itemize|enumerate|figure|table|verbatim|quote)\}$', block):
            continue

        # Handle itemize (bullet lists)
        if '\\begin{itemize}' in block:
            html += convert_itemize(block)
        # Handle enumerate (numbered lists)
        elif '\\begin{enumerate}' in block:
            html += convert_enumerate(block)
        # Handle figures
        elif '\\begin{figure}' in block or '\\includegraphics' in block:
            html += convert_figure(block)
        # Regular paragraph
        else:
            # Clean up LaTeX commands
            para = clean_latex(block)
            if para:
                html += f'<p>{para}</p>\n\n'

    return html

def convert_itemize(block):
    """Convert itemize environment to HTML ul"""
    # Extract items - capture everything between \item and next \item or \end{itemize}
    items = re.findall(r'\\item\s+((?:(?!\\item|\\end\{itemize\}).)+)', block, re.DOTALL)
    if not items:
        return ""

    html = "<ul>\n"
    for item in items:
        item = clean_latex(item.strip())
        html += f"<li>{item}</li>\n"
    html += "</ul>\n\n"
    return html

def convert_enumerate(block):
    """Convert enumerate environment to HTML ol"""
    # Extract items - capture everything between \item and next \item or \end{enumerate}
    items = re.findall(r'\\item\s+((?:(?!\\item|\\end\{enumerate\}).)+)', block, re.DOTALL)
    if not items:
        return ""

    html = "<ol>\n"
    for item in items:
        item = clean_latex(item.strip())
        html += f"<li>{item}</li>\n"
    html += "</ol>\n\n"
    return html

def convert_figure(block):
    """Convert figure to HTML"""
    # Extract image filename
    img_match = re.search(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', block)
    if not img_match:
        return ""

    img_src = img_match.group(1)

    # Extract caption
    caption_match = re.search(r'\\caption\{([^}]+)\}', block)
    caption = caption_match.group(1) if caption_match else ""

    # Extract alt text
    alt_match = re.search(r'\\alt\{([^}]+)\}', block)
    alt_text = alt_match.group(1) if alt_match else caption

    html = "<figure>\n"
    html += f'<img src="{img_src}" alt="{clean_latex(alt_text)}">\n'
    if caption:
        html += f"<figcaption>{clean_latex(caption)}</figcaption>\n"
    html += "</figure>\n\n"

    return html

def clean_latex(text):
    """Remove/convert LaTeX commands to plain text/HTML"""
    # Remove comments
    text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)

    # Convert URLs (allow optional whitespace between \url and {)
    text = re.sub(r'\\url\s*\{([^}]+)\}', r'<a href="\1">\1</a>', text)
    text = re.sub(r'\\href\s*\{([^}]+)\}\s*\{([^}]+)\}', r'<a href="\1">\2</a>', text)

    # Convert text formatting
    text = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', text)
    text = re.sub(r'\\textit\{([^}]+)\}', r'<em>\1</em>', text)
    text = re.sub(r'\\emph\{([^}]+)\}', r'<em>\1</em>', text)

    # Remove other LaTeX commands
    text = re.sub(r'\\[a-zA-Z]+\*?\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+\*?', '', text)

    # Clean up spacing
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text

def convert_tex_to_html(tex_file, css_file="../../tools/accessible-lab.css"):
    """Main conversion function"""
    # Read .tex file
    with open(tex_file, 'r', encoding='utf-8') as f:
        tex_content = f.read()

    # Extract metadata
    title = extract_title(tex_content)
    author_info = extract_author_info(tex_content)

    # Get PDF filename for accessibility notice
    pdf_file = Path(tex_file).with_suffix('.pdf').name

    # Extract document body
    body_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', tex_content, re.DOTALL)
    if not body_match:
        print(f"Error: No document environment found in {tex_file}", file=sys.stderr)
        return False

    body = body_match.group(1)

    # Extract sections for TOC
    sections = extract_sections(body)
    toc_html = generate_toc(sections)

    # Start HTML
    html = f'''<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link href="{css_file}" rel="stylesheet" type="text/css">
</head>
<body>
    <a href="#main-content" class="skip-link">Skip to main content</a>
    <header>
        <h1>{title}</h1>
        <div class="author">
            <p>{author_info['name']}</p>
            <p>Website: <a href="{author_info['website']}">{author_info['website']}</a></p>
            <p>GitHub: <a href="https://github.com/{author_info['github']}" aria-label="GitHub profile">{author_info['github']}</a></p>
        </div>
    </header>

    <main id="main-content">
        <section aria-labelledby="pdf-version-notice" class="accessibility-notice">
            <h2 id="pdf-version-notice">PDF Version Available</h2>
            <p>This document is also available in PDF format: <a href="{pdf_file}">{pdf_file}</a></p>
            <p>The PDF version includes bookmarks for easy navigation and is optimized for printing.</p>
        </section>

{toc_html}'''

    # Split into sections
    sections = re.split(r'(\\(?:sub)?section\*?\{[^}]+\})', body)

    current_section = ""
    for i, part in enumerate(sections):
        if re.match(r'\\(?:sub)?section\*?\{', part):
            # This is a section header
            if current_section:
                html += convert_section(current_section)
            current_section = part
        else:
            current_section += part

    # Process last section
    if current_section:
        html += convert_section(current_section)

    # Close HTML
    html += '''    </main>
</body>
</html>
'''

    # Write HTML file
    html_file = Path(tex_file).with_suffix('.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Created {html_file}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: tex-to-clean-html.py <tex_file>", file=sys.stderr)
        sys.exit(1)

    tex_file = sys.argv[1]
    if not Path(tex_file).exists():
        print(f"Error: File {tex_file} not found", file=sys.stderr)
        sys.exit(1)

    if convert_tex_to_html(tex_file):
        sys.exit(0)
    else:
        sys.exit(1)
