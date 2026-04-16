#!/usr/bin/env python3
"""
Add enumitem package and list spacing configuration to all .tex lab files
for improved PDF accessibility with screen readers
"""

import sys
import re
from pathlib import Path

def has_enumitem_package(content):
    """Check if file already has enumitem package"""
    return r'\usepackage{enumitem}' in content

def has_setlist(content):
    """Check if file already has setlist configuration"""
    return r'\setlist{nosep}' in content or r'\setlist{' in content

def add_enumitem_package(content):
    """Add enumitem package after bookmark package"""
    if r'\usepackage{bookmark}' in content:
        return content.replace(
            r'\usepackage{bookmark}',
            r'\usepackage{bookmark}' + '\n' + r'\usepackage{enumitem}'
        )
    # Fallback: add after accessibility package
    elif r'\usepackage[tagged, highstructure]{accessibility}' in content:
        return content.replace(
            r'\usepackage[tagged, highstructure]{accessibility}',
            r'\usepackage[tagged, highstructure]{accessibility}' + '\n' + r'\usepackage{enumitem}'
        )
    else:
        print("Warning: Could not find place to add enumitem package", file=sys.stderr)
        return content

def add_setlist(content):
    """Add setlist configuration after bookmarksetup"""
    # Find the bookmarksetup block
    bookmarksetup_end = re.search(r'\\bookmarksetup\{[^}]*\}', content, re.DOTALL)
    if bookmarksetup_end:
        insert_pos = bookmarksetup_end.end()
        setlist_config = '\n\n% Configure list spacing for better accessibility\n\\setlist{nosep}\n'
        return content[:insert_pos] + setlist_config + content[insert_pos:]
    else:
        print("Warning: Could not find bookmarksetup block", file=sys.stderr)
        return content

def process_tex_file(tex_file):
    """Process a single .tex file"""
    print(f"Processing: {tex_file}")

    # Read file
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Add enumitem package if needed
    if not has_enumitem_package(content):
        print(f"  Adding enumitem package")
        content = add_enumitem_package(content)
        modified = True
    else:
        print(f"  Already has enumitem package")

    # Add setlist if needed
    if not has_setlist(content):
        print(f"  Adding setlist configuration")
        content = add_setlist(content)
        modified = True
    else:
        print(f"  Already has setlist configuration")

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
