#!/usr/bin/env python3
"""Clean and improve HTML generated from LaTeX"""

import sys
import re

def clean_html(html_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove XML declaration
        content = re.sub(r'<\?xml[^>]*\?>\s*', '', content)

        # Ensure proper HTML5 doctype
        content = re.sub(r'<!DOCTYPE[^>]*>', '<!DOCTYPE html>', content)

        # Add lang attribute
        content = re.sub(r'<html[^>]*>', '<html lang="en-US">', content)

        # Add/update meta viewport
        if 'viewport' not in content:
            content = re.sub(
                r'(<head[^>]*>)',
                r'\1\n<meta name="viewport" content="width=device-width, initial-scale=1">',
                content
            )

        # Link to simplified CSS
        content = re.sub(
            r'<link[^>]*rel=["\']stylesheet["\'][^>]*>',
            '<link href="whatisdata.css" rel="stylesheet" type="text/css">',
            content
        )

        # Improve semantic structure
        content = re.sub(r'<h3 class="likesectionHead"', '<h2', content)
        content = re.sub(r'class="likesectionHead"', '', content)
        content = re.sub(r'class="likesubsectionHead"', '', content)

        # Clean up excessive classes
        content = re.sub(r' class="noindent"', '', content)
        content = re.sub(r' class="indent"', '', content)
        content = re.sub(r' class="enumerate1"', '', content)

        # Wrap sections with semantic HTML
        # Add section wrappers for headings with IDs
        lines = content.split('\n')
        new_lines = []
        section_open = False

        for line in lines:
            # Close previous section if new h2 starts
            if '<h2' in line and 'id=' in line and section_open:
                new_lines.append('</section>')
                section_open = False

            # Open new section
            if '<h2' in line and 'id=' in line:
                id_match = re.search(r'id=["\']([^"\']+)["\']', line)
                if id_match:
                    section_id = id_match.group(1)
                    new_lines.append(f'<section aria-labelledby="{section_id}">')
                    section_open = True

            new_lines.append(line)

        # Close last section if open
        if section_open:
            # Insert before </body>
            for i in range(len(new_lines) - 1, -1, -1):
                if '</body>' in new_lines[i]:
                    new_lines.insert(i, '</section>')
                    break

        content = '\n'.join(new_lines)

        # Write back
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"Error processing {html_file}: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: clean-html.py <html_file>", file=sys.stderr)
        sys.exit(1)

    html_file = sys.argv[1]
    if clean_html(html_file):
        print(f"✓ Cleaned {html_file}")
    else:
        print(f"✗ Failed to clean {html_file}", file=sys.stderr)
        sys.exit(1)
