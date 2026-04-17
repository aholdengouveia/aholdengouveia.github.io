#!/usr/bin/env python3
r"""
LaTeX Accessibility Tool - Add and fix accessibility features in .tex files

This tool helps make LaTeX documents more accessible by:
- Adding required accessibility packages (accessibility, bookmark, enumitem)
- Adding accessibility notices for HTML versions
- Fixing common LaTeX structure issues (hypersetup, bookmarksetup)
- Converting plain URLs to proper \url{} commands

Usage:
    # Check if LaTeX and required packages are installed
    python3 latex-accessibility.py check-packages

    # Add all accessibility features to a file
    python3 latex-accessibility.py add <file.tex>

    # Fix structural issues in a file
    python3 latex-accessibility.py fix <file.tex>

    # Add accessibility features to all .tex files in a directory
    python3 latex-accessibility.py add-all <directory>

    # Fix all .tex files in a directory
    python3 latex-accessibility.py fix-all <directory>
"""

import sys
import re
import platform
import subprocess
from pathlib import Path


def check_package_installed(package_name):
    """Check if a LaTeX package is installed using kpsewhich"""
    try:
        # kpsewhich is a standard tool that comes with TeX distributions
        # It searches for files in the TeX directory structure
        result = subprocess.run(
            ['kpsewhich', f'{package_name}.sty'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except FileNotFoundError:
        # kpsewhich not found - LaTeX probably not installed
        return None
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None


def detect_os():
    """Detect the operating system"""
    system = platform.system().lower()
    if system == 'linux':
        # Try to detect Linux distribution
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
                if 'ubuntu' in os_info or 'debian' in os_info:
                    return 'debian'
                elif 'fedora' in os_info or 'rhel' in os_info or 'centos' in os_info:
                    return 'fedora'
                else:
                    return 'linux'
        except:
            return 'linux'
    elif system == 'darwin':
        return 'mac'
    elif system == 'windows':
        return 'windows'
    else:
        return 'unknown'


def get_installation_command(os_type):
    """Get OS-specific installation commands for LaTeX packages"""
    commands = {
        'debian': {
            'full': 'sudo apt-get install texlive-latex-extra texlive-fonts-recommended',
            'description': 'Ubuntu/Debian'
        },
        'fedora': {
            'full': 'sudo dnf install texlive-scheme-medium',
            'description': 'Fedora/RHEL/CentOS'
        },
        'mac': {
            'full': 'brew install --cask mactex',
            'alt': 'Or download from: https://www.tug.org/mactex/',
            'description': 'macOS'
        },
        'windows': {
            'full': 'Download and install MiKTeX from: https://miktex.org/download',
            'alt': 'Or install TeX Live from: https://www.tug.org/texlive/windows.html',
            'description': 'Windows'
        },
        'linux': {
            'full': 'Install texlive-latex-extra using your package manager',
            'description': 'Linux'
        }
    }
    return commands.get(os_type, commands['linux'])


def check_latex_packages():
    """Check if required LaTeX packages are installed and provide installation instructions"""
    required_packages = ['hyperref', 'bookmark', 'enumitem']
    optional_packages = ['accessibility']

    print("Checking LaTeX installation and packages...\n")

    # Check if kpsewhich exists (indicates LaTeX is installed)
    try:
        subprocess.run(['kpsewhich', '--version'], capture_output=True, timeout=5)
        latex_installed = True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        latex_installed = False

    if not latex_installed:
        print("❌ LaTeX does not appear to be installed (kpsewhich not found)")
        print("\nLaTeX is required to generate PDFs from .tex files.")
        os_type = detect_os()
        install_info = get_installation_command(os_type)
        print(f"\nTo install LaTeX on {install_info['description']}:")
        print(f"  {install_info['full']}")
        if 'alt' in install_info:
            print(f"  {install_info['alt']}")
        return False

    print("✓ LaTeX is installed (kpsewhich found)\n")

    # Check required packages
    missing_packages = []
    installed_packages = []

    print("Required packages:")
    for package in required_packages:
        status = check_package_installed(package)
        if status:
            print(f"  ✓ {package}")
            installed_packages.append(package)
        else:
            print(f"  ❌ {package} (missing)")
            missing_packages.append(package)

    # Check optional packages
    print("\nOptional packages:")
    for package in optional_packages:
        status = check_package_installed(package)
        if status:
            print(f"  ✓ {package}")
            installed_packages.append(package)
        else:
            print(f"  ○ {package} (not installed, but optional)")

    # Provide installation instructions if packages are missing
    if missing_packages:
        print(f"\n❌ Missing {len(missing_packages)} required package(s): {', '.join(missing_packages)}")
        print("\nThese packages are needed for the accessibility features to work.")

        os_type = detect_os()
        install_info = get_installation_command(os_type)

        print(f"\nTo install missing packages on {install_info['description']}:")
        print(f"  {install_info['full']}")
        if 'alt' in install_info:
            print(f"  {install_info['alt']}")

        print("\nAfter installation, run this command again to verify.")
        return False
    else:
        print("\n✅ All required packages are installed!")
        print("\nYou're ready to use the LaTeX accessibility tools.")
        return True


def add_accessibility_packages(content):
    """Add accessibility-related packages if missing"""
    modified = False

    # Check for and add bookmark package
    if r'\usepackage{bookmark}' not in content:
        # Find hyperref package and add bookmark after it
        pattern = r'(\\usepackage(?:\[.*?\])?\{hyperref\})'
        if re.search(pattern, content):
            content = re.sub(pattern, r'\1\n\\usepackage{bookmark}', content)
            modified = True

    # Check for and add enumitem package
    if r'\usepackage{enumitem}' not in content:
        # Add after bookmark or hyperref
        if r'\usepackage{bookmark}' in content:
            pattern = r'(\\usepackage\{bookmark\})'
            content = re.sub(pattern, r'\1\n\\usepackage{enumitem}', content)
            modified = True
        elif r'\usepackage{hyperref}' in content:
            pattern = r'(\\usepackage(?:\[.*?\])?\{hyperref\})'
            content = re.sub(pattern, r'\1\n\\usepackage{enumitem}', content)
            modified = True

    return content, modified


def add_bookmark_configuration(content):
    """Add bookmarksetup and setlist configuration after hypersetup"""
    modified = False

    # Check if already has bookmarksetup
    if r'\bookmarksetup{' in content:
        return content, False

    # Find the end of hypersetup block
    pattern = r'(\\hypersetup\{[^}]*\})'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        bookmark_config = r'''

% Configure PDF bookmarks for navigation
\bookmarksetup{
    numbered,
    open,
}

% Configure list spacing for better accessibility
\setlist{nosep}
'''
        insert_pos = match.end()
        content = content[:insert_pos] + bookmark_config + content[insert_pos:]
        modified = True

    return content, modified


def add_accessibility_notice(content, html_url):
    """Add accessibility notice section after \maketitle"""
    modified = False

    # Check if notice already exists
    if 'Accessibility Notice' in content:
        return content, False

    # Find \maketitle and add notice after it
    pattern = r'(\\maketitle\s*\n)'

    if re.search(pattern, content):
        notice = f'''
\\section*{{Accessibility Notice}}
This document is also available in HTML format at:

\\url{{{html_url}}}

The HTML version provides enhanced accessibility features including keyboard navigation, screen reader support, responsive design, dark mode support, and high contrast options.

'''
        content = re.sub(pattern, r'\1\n' + notice, content)
        modified = True

    return content, modified


def fix_hypersetup_structure(content):
    """Fix hypersetup block that has bookmarksetup incorrectly inside it"""

    # Pattern to find malformed hypersetup blocks where bookmarksetup is inside
    pattern = r'\\hypersetup\{(.*?)\n\n(% Configure PDF bookmarks for navigation.*?\\setlist\{nosep\})\s*\n\s*\n(,\s*\n.*?)\}'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        hypersetup_params_before = match.group(1)  # colorlinks, pdfborder, etc.
        bookmark_section = match.group(2)  # The bookmarksetup and setlist blocks
        hypersetup_params_after = match.group(3)  # Comma + pdftitle, etc.

        # Remove the leading comma from params_after
        hypersetup_params_after = hypersetup_params_after.lstrip(',\n ')

        # Reconstruct hypersetup properly
        fixed_hypersetup = '\\hypersetup{\n' + hypersetup_params_before

        # Add comma if needed between before and after params
        if hypersetup_params_before.strip() and hypersetup_params_after.strip():
            if not hypersetup_params_before.rstrip().endswith(','):
                fixed_hypersetup += ','
            fixed_hypersetup += '\n    ' + hypersetup_params_after
        else:
            fixed_hypersetup += '\n    ' + hypersetup_params_after

        fixed_hypersetup += '\n}'

        # Reconstruct the full content with bookmark section after hypersetup
        new_content = content[:match.start()] + fixed_hypersetup + '\n\n' + bookmark_section + '\n' + content[match.end():]
        return new_content, True

    return content, False


def fix_plain_urls(content):
    r"""Wrap plain http(s) URLs in \url{} commands"""
    lines = content.split('\n')
    fixed_lines = []
    modified = False

    for line in lines:
        # Skip lines that already have \url or \href
        if '\\url' in line or '\\href' in line:
            fixed_lines.append(line)
            continue

        # Find standalone URLs (not already wrapped)
        url_pattern = r'(?<!\\url\{)(?<!\\href\{)(https?://[^\s\)]+)'
        if re.search(url_pattern, line):
            # Wrap URL in \url{}
            new_line = re.sub(url_pattern, r'\\url{\1}', line)
            if new_line != line:
                fixed_lines.append(new_line)
                modified = True
                continue

        fixed_lines.append(line)

    return '\n'.join(fixed_lines), modified


def add_all_features(tex_file, html_url=None):
    """Add all accessibility features to a .tex file"""
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"❌ Error: File {tex_file} is not valid UTF-8 text")
        print("   Suggestion: Check if this is a binary file or has encoding issues")
        return False
    except Exception as e:
        print(f"❌ Error reading {tex_file}: {e}")
        return False

    original_content = content

    # Auto-generate HTML URL if not provided
    if not html_url:
        # Try to extract from existing URLs or create default
        file_path = Path(tex_file)
        # Assuming structure like /path/to/Section/labs/filename.tex
        # Create URL like https://aholdengouveia.name/Section/labs/filename.html
        parts = file_path.parts
        if len(parts) >= 2:
            section = parts[-2]  # e.g., "labs"
            parent = parts[-3] if len(parts) >= 3 else "unknown"  # e.g., "IntroLinux"
            filename = file_path.stem  # filename without extension
            html_url = f"https://aholdengouveia.name/{parent}/{section}/{filename}.html"

    # Add packages
    content, pkg_modified = add_accessibility_packages(content)

    # Fix URLs
    content, url_modified = fix_plain_urls(content)

    # Add bookmark configuration
    content, bookmark_modified = add_bookmark_configuration(content)

    # Add accessibility notice
    if html_url:
        content, notice_modified = add_accessibility_notice(content, html_url)
    else:
        notice_modified = False

    modified = pkg_modified or url_modified or bookmark_modified or notice_modified

    if modified:
        try:
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except PermissionError:
            print(f"❌ Error: Permission denied writing to {tex_file}")
            print("   Suggestion: Check file permissions or run with appropriate privileges")
            return False
        except Exception as e:
            print(f"❌ Error writing to {tex_file}: {e}")
            return False

    return False


def fix_structure(tex_file):
    """Fix structural issues in a .tex file"""
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {tex_file}: {e}")
        return False

    # Fix hypersetup structure
    content, modified = fix_hypersetup_structure(content)

    if modified:
        try:
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"❌ Error writing to {tex_file}: {e}")
            return False

    return False


def process_directory(directory, command):
    """Process all .tex files in a directory"""
    directory = Path(directory)
    tex_files = list(directory.glob('*.tex'))

    if not tex_files:
        print(f"No .tex files found in {directory}")
        return

    modified_count = 0
    for tex_file in sorted(tex_files):
        if command == 'add-all':
            if add_all_features(tex_file):
                print(f"✓ Added accessibility features to {tex_file.name}")
                modified_count += 1
            else:
                print(f"○ {tex_file.name} already has accessibility features")
        elif command == 'fix-all':
            if fix_structure(tex_file):
                print(f"✓ Fixed structure in {tex_file.name}")
                modified_count += 1
            else:
                print(f"○ {tex_file.name} structure OK")

    print(f"\n✓ Modified {modified_count} files")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command in ['add', 'fix']:
        if len(sys.argv) < 3:
            print(f"❌ Error: Missing file argument")
            print(f"\nUsage: {sys.argv[0]} {command} <file.tex>")
            print(f"\nExample: {sys.argv[0]} {command} mylab.tex")
            sys.exit(1)

        tex_file = sys.argv[2]

        if not Path(tex_file).exists():
            print(f"❌ Error: File not found: {tex_file}")
            print(f"\nSuggestions:")
            print(f"  • Check the file path is correct")
            print(f"  • Make sure you're in the right directory")
            print(f"  • Use 'ls' to see available .tex files")

            # Suggest similar files
            directory = Path(tex_file).parent if Path(tex_file).parent.exists() else Path('.')
            tex_files = list(directory.glob('*.tex'))
            if tex_files:
                print(f"\n  Available .tex files in {directory}:")
                for f in sorted(tex_files)[:5]:
                    print(f"    • {f.name}")
                if len(tex_files) > 5:
                    print(f"    ... and {len(tex_files) - 5} more")
            sys.exit(1)

        if not str(tex_file).endswith('.tex'):
            print(f"⚠️  Warning: {tex_file} doesn't have .tex extension")
            print(f"   This tool is designed for LaTeX files (.tex)")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(0)

        if command == 'add':
            if add_all_features(tex_file):
                print(f"✓ Added accessibility features to {tex_file}")
            else:
                print(f"○ {tex_file} already has accessibility features")
        elif command == 'fix':
            if fix_structure(tex_file):
                print(f"✓ Fixed structure in {tex_file}")
            else:
                print(f"○ {tex_file} structure OK")

    elif command in ['add-all', 'fix-all']:
        if len(sys.argv) < 3:
            print(f"❌ Error: Missing directory argument")
            print(f"\nUsage: {sys.argv[0]} {command} <directory>")
            print(f"\nExample: {sys.argv[0]} {command} IntroLinux/labs")
            sys.exit(1)

        directory = sys.argv[2]

        if not Path(directory).exists():
            print(f"❌ Error: Directory not found: {directory}")
            print(f"\nSuggestions:")
            print(f"  • Check the directory path is correct")
            print(f"  • Use 'ls' to see available directories")
            sys.exit(1)

        if not Path(directory).is_dir():
            print(f"❌ Error: {directory} is not a directory")
            print(f"   Use '{command.replace('-all', '')}' for single files")
            sys.exit(1)

        process_directory(directory, command)

    elif command == 'check-packages':
        # Check LaTeX package installation
        success = check_latex_packages()
        sys.exit(0 if success else 1)

    else:
        print(f"❌ Error: Unknown command: {command}")
        print(f"\nValid commands: add, fix, add-all, fix-all, check-packages")
        print(f"\nFor help, run: {sys.argv[0]} --help")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
