#!/usr/bin/env python3
"""
Fix plain text URLs in .tex files by wrapping them in url commands
"""

import sys
import re
from pathlib import Path

def fix_plain_urls(content):
    """
    Find standalone URLs and wrap them in url commands
    """
    # Pattern to match URLs that are NOT already in \url{} or \href{}
    # Match lines with http(s):// that don't have \url or \href before them

    lines = content.split('\n')
    fixed_lines = []
    modified = False

    for line in lines:
        # Skip if line already has \url or \href
        if r'\url' in line or r'\href' in line:
            fixed_lines.append(line)
            continue

        # Check if line has a standalone URL
        url_pattern = r'^(.*?)(https?://[^\s]+)(.*)$'
        match = re.match(url_pattern, line)

        if match:
            before = match.group(1)
            url = match.group(2)
            after = match.group(3)

            # Only wrap if it's truly standalone (not part of other LaTeX command)
            if not before.strip().endswith('\\'):
                fixed_line = before + r'\url{' + url + '}' + after
                fixed_lines.append(fixed_line)
                modified = True
                print(f"    Fixed: {url}")
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines), modified

def process_tex_file(tex_file):
    """Process a single .tex file"""
    print(f"Processing: {tex_file}")

    # Read file
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix URLs
    content, modified = fix_plain_urls(content)

    if modified:
        # Write back
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed plain text URLs")
        return True
    else:
        print(f"  No plain text URLs found")
        return False

def main():
    # Specific files that need fixing
    base_path = Path('/home/aholdengouveia/aholdengouveia.github.io/LinuxAdmin/labexcercises')

    files_to_fix = [
        'awklab.tex',
        'contSetup.tex',
        'greplab.tex',
        'iptables.tex',
        'networking.tex',
        'sedlab.tex',
        'serverhardening.tex',
        'ServerSetup.tex'
    ]

    print(f"Fixing {len(files_to_fix)} .tex files with plain text URLs\n")

    fixed = 0
    for filename in files_to_fix:
        tex_file = base_path / filename
        if tex_file.exists():
            if process_tex_file(tex_file):
                fixed += 1
            print()
        else:
            print(f"Warning: {tex_file} not found\n")

    print(f"\nSummary: Fixed {fixed} of {len(files_to_fix)} files")

if __name__ == '__main__':
    main()
