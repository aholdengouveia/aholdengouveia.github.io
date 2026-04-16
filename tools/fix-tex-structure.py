#!/usr/bin/env python3
"""
Fix LaTeX file structure to properly close hypersetup before bookmarksetup and setlist
"""

import sys
import re
from pathlib import Path

def fix_hypersetup_structure(content):
    """
    Fix the structure where bookmarksetup and setlist are incorrectly nested inside hypersetup
    """
    # Pattern to match the broken structure
    # hypersetup{ ... \n\n% Configure PDF bookmarks ... \bookmarksetup{...}\n\n% Configure list... \setlist{nosep}\n\n, pdftitle=...}

    pattern = r'(\\hypersetup\{[^}]*pdfborder=\{0 0 0\})\s*\n\n(% Configure PDF bookmarks.*?\\bookmarksetup\{[^}]*\})\s*\n\n(% Configure list spacing.*?\\setlist\{nosep\})\s*\n\n,\s*\n\s*(pdftitle=.*?\})\s*\n'

    match = re.search(pattern, content, re.DOTALL)

    if match:
        # Reconstruct properly
        hypersetup_start = match.group(1)
        bookmark_section = match.group(2)
        setlist_section = match.group(3)
        hypersetup_end = match.group(4)

        # Proper structure: close hypersetup, then bookmarksetup, then setlist
        fixed = f"{hypersetup_start},\n    {hypersetup_end}\n\n{bookmark_section}\n\n{setlist_section}\n"

        content = content[:match.start()] + fixed + content[match.end():]
        return content, True

    return content, False

def process_tex_file(tex_file):
    """Process a single .tex file"""
    print(f"Processing: {tex_file}")

    # Read file
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix structure
    content, modified = fix_hypersetup_structure(content)

    if modified:
        # Write back
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed structure")
        return True
    else:
        print(f"  Structure looks OK")
        return False

def main():
    # Find all .tex files in lab directories
    base_path = Path('/home/aholdengouveia/aholdengouveia.github.io')

    tex_files = []
    for pattern in ['IntroData/labs/*.tex', 'AdvData/labs/*.tex', 'LinuxAdmin/labexcercises/*.tex']:
        tex_files.extend(base_path.glob(pattern))

    print(f"Found {len(tex_files)} .tex files to check\n")

    fixed = 0
    for tex_file in sorted(tex_files):
        if process_tex_file(tex_file):
            fixed += 1
        print()

    print(f"\nSummary: Fixed {fixed} of {len(tex_files)} files")

if __name__ == '__main__':
    main()
