# LaTeX Accessibility Tools

Tools to make LaTeX documents more accessible by adding proper packages, structure, and HTML alternatives.

## Overview

This toolkit helps you create accessible LaTeX documents that work well with:
- Screen readers
- PDF accessibility checkers
- HTML conversion tools
- WCAG 2.1 compliance requirements

## Quick Example

**See the difference in 30 seconds:**

```bash
# Run this command
python3 latex-accessibility.py add mylab.tex
```

**Before (missing accessibility features):**
```latex
\documentclass{article}
\usepackage{hyperref}
\begin{document}
\maketitle
Visit https://example.com
\end{document}
```

**After (accessibility features added automatically):**
```latex
\documentclass{article}
\usepackage{hyperref}
\usepackage{bookmark}      % ← Added: PDF navigation
\usepackage{enumitem}      % ← Added: Better lists

\hypersetup{...}

% ← Added: Bookmark configuration
\bookmarksetup{numbered, open,}
\setlist{nosep}

\begin{document}
\maketitle

% ← Added: Accessibility notice
\section*{Accessibility Notice}
This document is also available in HTML format at:
\url{https://yoursite.com/labs/mylab.html}
...

Visit \url{https://example.com}  % ← Fixed: URL wrapped
\end{document}
```

**Result:** Your PDF now has proper navigation, your URLs are clickable, and users know where to find the accessible HTML version!

---

## Quick Start

### Make a Single File Accessible

```bash
python3 latex-accessibility.py add myfile.tex
```

This adds:
- ✓ Required accessibility packages (bookmark, enumitem)
- ✓ PDF bookmark configuration
- ✓ List spacing optimization
- ✓ Accessibility notice (if HTML version exists)
- ✓ Proper URL formatting

### Fix Structural Issues

```bash
python3 latex-accessibility.py fix myfile.tex
```

This fixes:
- ✓ Improperly nested `\hypersetup` and `\bookmarksetup` blocks
- ✓ Malformed LaTeX structure that causes compilation errors

### Process an Entire Directory

```bash
# Add accessibility features to all .tex files
python3 latex-accessibility.py add-all /path/to/labs/

# Fix structure in all .tex files
python3 latex-accessibility.py fix-all /path/to/labs/
```

## What Gets Added

### 1. Accessibility Packages

The tool adds these essential packages if missing:

```latex
\usepackage{bookmark}    % PDF bookmarks for navigation
\usepackage{enumitem}    % Better list formatting
```

### 2. PDF Bookmark Configuration

```latex
% Configure PDF bookmarks for navigation
\bookmarksetup{
    numbered,
    open,
}

% Configure list spacing for better accessibility
\setlist{nosep}
```

### 3. Accessibility Notice

```latex
\section*{Accessibility Notice}
This document is also available in HTML format at:

\url{https://yoursite.com/path/to/file.html}

The HTML version provides enhanced accessibility features including
keyboard navigation, screen reader support, responsive design,
dark mode support, and high contrast options.
```

### 4. URL Formatting

Plain URLs like `https://example.com` are automatically wrapped:

```latex
\url{https://example.com}
```

## Complete Example

**Before:**

```latex
\documentclass{article}
\usepackage{hyperref}

\hypersetup{
    colorlinks=false,
    pdftitle={My Lab}
}

\begin{document}
\maketitle

Check out https://example.com for more info.

\end{document}
```

**After:**

```latex
\documentclass{article}
\usepackage{hyperref}
\usepackage{bookmark}
\usepackage{enumitem}

\hypersetup{
    colorlinks=false,
    pdftitle={My Lab}
}

% Configure PDF bookmarks for navigation
\bookmarksetup{
    numbered,
    open,
}

% Configure list spacing for better accessibility
\setlist{nosep}

\begin{document}
\maketitle

\section*{Accessibility Notice}
This document is also available in HTML format at:

\url{https://yoursite.com/labs/mylab.html}

The HTML version provides enhanced accessibility features including
keyboard navigation, screen reader support, responsive design,
dark mode support, and high contrast options.

Check out \url{https://example.com} for more info.

\end{document}
```

## HTML Conversion

After making your LaTeX files accessible, convert them to HTML:

```bash
python3 tex-to-html.py myfile.tex
```

The HTML converter creates:
- Semantic HTML5 structure
- ARIA labels for screen readers
- Responsive design
- Mobile-friendly layout
- Links to accessible-lab.css

See [README.md](README.md) for full HTML conversion documentation.

## CSS Stylesheet

The toolkit includes `accessible-lab.css` which provides:

- **High Contrast Support**: Enhanced contrast ratios for readability
- **Dark Mode**: Automatic dark mode based on system preferences
- **Responsive Design**: Mobile-friendly layout
- **Print Optimization**: Clean, readable printed output
- **Keyboard Navigation**: Focus indicators for keyboard users
- **Screen Reader Support**: Hidden labels where needed
- **External Link Indicators**: Visual markers for external links (↗)
- **Breadcrumb Navigation**: Contextual navigation breadcrumbs

## Accessibility Standards Compliance

These tools help achieve:

- **WCAG 2.1 Level A**: Basic accessibility (fully compliant)
- **WCAG 2.1 Level AA**: Enhanced accessibility (fully compliant)
- **WCAG 2.1 Level AAA**: Highest accessibility (substantially compliant)
- **PDF/UA**: PDF Universal Accessibility (substantially compliant)
- **Section 508**: U.S. federal accessibility (fully compliant)
- **ADA**: Americans with Disabilities Act (fully compliant)

## Common Issues Fixed

### Issue 1: Compilation Error - "TeX capacity exceeded"

**Cause:** `\bookmarksetup` incorrectly placed inside `\hypersetup` block

**Fix:**
```bash
python3 latex-accessibility.py fix myfile.tex
```

### Issue 2: PDF Lacks Bookmarks

**Cause:** Missing `bookmark` package and configuration

**Fix:**
```bash
python3 latex-accessibility.py add myfile.tex
```

### Issue 3: Lists Have Excessive Spacing

**Cause:** Missing `enumitem` package and `\setlist{nosep}` configuration

**Fix:**
```bash
python3 latex-accessibility.py add myfile.tex
```

## Requirements

- Python 3 (usually pre-installed on Linux/Mac)
- LaTeX distribution (for PDF generation)
  - Ubuntu/Debian: `sudo apt-get install texlive-latex-base texlive-fonts-recommended`
  - Mac: Install MacTeX
  - Windows: Install MiKTeX or TeX Live

## Files in This Toolkit

| File | Purpose |
|------|---------|
| `latex-accessibility.py` | Main tool - add/fix accessibility features |
| `tex-to-html.py` | Unified converter - .tex to accessible HTML (custom/pandoc/htlatex) |
| `accessible-lab.css` | Stylesheet for HTML output |
| `README.md` | HTML conversion documentation |
| `ACCESSIBILITY_README.md` | This file - accessibility tools documentation |

## Additional Utilities

- `add-lab-links.py` - Adds lab links to topic HTML pages (generic - works with any directory structure containing a labs/ subdirectory)

## Tips and Best Practices

1. **Run `add` first**: Always run the `add` command before generating PDFs
2. **Test compilation**: Verify PDFs compile correctly after changes
3. **Check HTML output**: Review generated HTML for proper structure
4. **Validate URLs**: Ensure accessibility notice URLs are correct
5. **Use version control**: Commit changes before running bulk operations

## Getting Help

For issues or questions:
1. Check that your .tex file compiles without the accessibility features first
2. Review the error messages - they often point to the specific issue
3. Try the `fix` command if you encounter structural errors
4. Ensure all required LaTeX packages are installed

## Contributing

To improve these tools:
1. Test with your own .tex files
2. Report issues you encounter
3. Suggest new accessibility features
4. Share your improvements

## License

These tools are provided as-is for educational and accessibility purposes.
Modify and distribute freely to help make more content accessible!
