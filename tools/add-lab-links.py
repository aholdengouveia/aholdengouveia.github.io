#!/usr/bin/env python3
"""
Add lab PDF and HTML links to IntroLinux topic HTML files
"""

import sys
import re
from pathlib import Path

def add_lab_links(content, lab_name):
    """Add links to matching lab HTML and PDF in the suggested activities section"""

    # First, remove old format links if they exist
    old_pattern1 = r'\s*<li><a href="labs/' + re.escape(lab_name) + r'\.html">Lab Assignment \(HTML\)</a> - Accessible web version</li>\s*\n'
    old_pattern2 = r'\s*<li><a href="labs/' + re.escape(lab_name) + r'\.pdf">Lab Assignment \(PDF\)</a> - Printable version</li>\s*\n'
    content = re.sub(old_pattern1, '', content)
    content = re.sub(old_pattern2, '', content)

    # Check if new format links already exist
    if f'Lab assignment: <a href="labs/{lab_name}.pdf">PDF version</a>' in content:
        return content, False

    # Pattern to find the suggested activities section
    # Look for the opening <ul> after "Suggested Activities and Discussion Topics:"
    pattern = r'(<p>Suggested Activities and Discussion Topics:\s*<ul>)'

    # Create the lab links to insert
    lab_links = f'''        <li>Lab assignment: <a href="labs/{lab_name}.pdf">PDF version</a> (<a href="labs/{lab_name}.html">accessible HTML version</a>)</li>
'''

    # Insert the links right after the opening <ul>
    replacement = r'\1\n' + lab_links
    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        return new_content, True

    return content, False

def main():
    # Get all IntroLinux HTML files (excluding resources.html)
    intro_linux_dir = Path('/home/aholdengouveia/aholdengouveia.github.io/IntroLinux')
    html_files = list(intro_linux_dir.glob('*.html'))

    modified_count = 0

    for html_file in sorted(html_files):
        # Skip resources.html
        if html_file.name == 'resources.html':
            continue

        lab_name = html_file.stem  # filename without extension

        # Check if matching lab exists
        lab_html = intro_linux_dir / 'labs' / f'{lab_name}.html'
        if not lab_html.exists():
            print(f"○ Skipping {html_file.name} - no matching lab found")
            continue

        # Read file
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add lab links
        new_content, modified = add_lab_links(content, lab_name)

        if modified:
            # Write back
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Added lab links to {html_file.name}")
            modified_count += 1
        else:
            print(f"○ {html_file.name} already has lab links")

    print(f"\n✓ Modified {modified_count} files")

if __name__ == '__main__':
    main()
