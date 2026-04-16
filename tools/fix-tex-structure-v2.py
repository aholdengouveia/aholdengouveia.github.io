#!/usr/bin/env python3
"""
Fix LaTeX file structure - move bookmarksetup and setlist outside of hypersetup
"""

import sys
import re
from pathlib import Path

def fix_hypersetup_structure(content):
    """
    Move bookmarksetup and setlist blocks outside of hypersetup
    """
    # Find hypersetup block that contains bookmarksetup and setlist
    pattern = r'(\\hypersetup\{.*?)(% Configure PDF bookmarks.*?\\bookmarksetup\{[^}]*\}\s*\n\s*% Configure list spacing.*?\\setlist\{nosep\}\s*\n)(\})'

    match = re.search(pattern, content, re.DOTALL)

    if match:
        hypersetup_content = match.group(1)
        bookmark_and_setlist = match.group(2)
        closing_brace = match.group(3)

        # Close hypersetup properly, then add bookmark and setlist outside
        fixed = hypersetup_content + closing_brace + '\n\n' + bookmark_and_setlist

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

    print(f"\nSummary: Fixed {fixed} of {len(tex_files)} files")

if __name__ == '__main__':
    main()
