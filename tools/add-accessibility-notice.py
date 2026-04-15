#!/usr/bin/env python3
"""
Add accessibility notice and PDF bookmarks to all .tex lab files
"""

import sys
import re
from pathlib import Path

def get_html_url(tex_file_path):
    """Generate the HTML URL for a given .tex file"""
    # Convert absolute path to relative from github.io root
    parts = Path(tex_file_path).parts

    # Find the index of 'aholdengouveia.github.io'
    try:
        idx = parts.index('aholdengouveia.github.io')
        # Get parts after github.io root
        rel_parts = parts[idx + 1:]
        # Replace .tex with .html
        html_parts = list(rel_parts[:-1]) + [rel_parts[-1].replace('.tex', '.html')]
        # Build URL
        url = 'https://aholdengouveia.name/' + '/'.join(html_parts)
        return url
    except ValueError:
        return None

def has_bookmark_package(content):
    """Check if file already has bookmark package"""
    return r'\usepackage{bookmark}' in content

def has_bookmarksetup(content):
    """Check if file already has bookmarksetup"""
    return r'\bookmarksetup{' in content

def has_accessibility_notice(content):
    """Check if file already has accessibility notice section"""
    return r'\section*{Accessibility Notice}' in content

def add_bookmark_package(content):
    """Add bookmark package after accessibility package"""
    if r'\usepackage[tagged, highstructure]{accessibility}' in content:
        return content.replace(
            r'\usepackage[tagged, highstructure]{accessibility}',
            r'\usepackage[tagged, highstructure]{accessibility}' + '\n' + r'\usepackage{bookmark}'
        )
    # Fallback: add after hyperref
    elif r'\usepackage{hyperref}' in content:
        return content.replace(
            r'\usepackage{hyperref}',
            r'\usepackage{hyperref}' + '\n' + r'\usepackage{bookmark}'
        )
    else:
        print("Warning: Could not find place to add bookmark package", file=sys.stderr)
        return content

def add_bookmarksetup(content):
    """Add bookmarksetup after hypersetup"""
    hypersetup_end = re.search(r'\\hypersetup\{[^}]*\}', content, re.DOTALL)
    if hypersetup_end:
        insert_pos = hypersetup_end.end()
        bookmark_config = '\n\n% Configure PDF bookmarks for navigation\n\\bookmarksetup{\n    numbered,\n    open,\n}\n'
        return content[:insert_pos] + bookmark_config + content[insert_pos:]
    else:
        print("Warning: Could not find hypersetup block", file=sys.stderr)
        return content

def add_accessibility_notice(content, html_url):
    """Add accessibility notice after \\maketitle"""
    notice = f'''
\\section*{{Accessibility Notice}}
This document is also available in HTML format at:

\\url{{{html_url}}}

The HTML version provides enhanced accessibility features including keyboard navigation, screen reader support, responsive design, dark mode support, and high contrast options.
'''

    # Find maketitle and insert after it
    maketitle_match = re.search(r'\\maketitle', content)
    if maketitle_match:
        # Find the next line after maketitle
        insert_pos = maketitle_match.end()
        # Skip to next section or content
        next_section = re.search(r'\\section', content[insert_pos:])
        if next_section:
            # Insert before the next section
            actual_pos = insert_pos + next_section.start()
            return content[:actual_pos] + notice + '\n' + content[actual_pos:]
        else:
            # Insert right after maketitle
            return content[:insert_pos] + '\n' + notice + content[insert_pos:]
    else:
        print("Warning: Could not find \\maketitle", file=sys.stderr)
        return content

def process_tex_file(tex_file):
    """Process a single .tex file"""
    print(f"Processing: {tex_file}")

    # Read file
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get HTML URL
    html_url = get_html_url(str(tex_file))
    if not html_url:
        print(f"  Skipping: Could not determine HTML URL")
        return False

    modified = False

    # Add bookmark package if needed
    if not has_bookmark_package(content):
        print(f"  Adding bookmark package")
        content = add_bookmark_package(content)
        modified = True

    # Add bookmarksetup if needed
    if not has_bookmarksetup(content):
        print(f"  Adding bookmarksetup")
        content = add_bookmarksetup(content)
        modified = True

    # Add accessibility notice if needed
    if not has_accessibility_notice(content):
        print(f"  Adding accessibility notice: {html_url}")
        content = add_accessibility_notice(content, html_url)
        modified = True

    if modified:
        # Write back
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated")
        return True
    else:
        print(f"  Already up to date")
        return False

def main():
    # Find all .tex files in lab directories (exclude _site)
    base_path = Path('/home/aholdengouveia/aholdengouveia.github.io')

    tex_files = []
    for pattern in ['IntroData/labs/*.tex', 'AdvData/labs/*.tex', 'LinuxAdmin/labexcercises/*.tex']:
        tex_files.extend(base_path.glob(pattern))

    print(f"Found {len(tex_files)} .tex files to process\n")

    updated = 0
    for tex_file in sorted(tex_files):
        if process_tex_file(tex_file):
            updated += 1
        print()

    print(f"\nSummary: Updated {updated} of {len(tex_files)} files")

if __name__ == '__main__':
    main()
