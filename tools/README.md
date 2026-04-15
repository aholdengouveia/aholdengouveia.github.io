# TEX to HTML Conversion Tools

Convert .tex files to clean, accessible HTML.

## Quick Start

### Interactive Converter (PDF + HTML)

The easiest way to convert a single .tex file to both PDF and HTML:

```bash
cd tools
./update-tex-outputs.sh
```

The script will:
- ✓ Prompt you for the .tex file path
- ✓ Validate the file exists
- ✓ Generate both PDF (via pdflatex) and HTML (via tex-to-clean-html.py)
- ✓ Show clear success/failure messages
- ✓ Clean up auxiliary files (.aux, .log, etc.)

### Convert a Single File to HTML Only

```bash
cd IntroData/labs
python3 ../../tools/tex-to-clean-html.py usesandabusesofdata.tex
```

### Convert All Files in a Directory

```bash
cd IntroData/labs
make
```

## The Clean HTML Converter

The `tex-to-clean-html.py` script generates accessible HTML similar to whatisdata.html:

**Features:**
- ✓ Clean, semantic HTML5
- ✓ Proper `<header>`, `<main>`, `<section>` structure
- ✓ ARIA labels (`aria-labelledby`) for accessibility
- ✓ Responsive design (viewport meta tag)
- ✓ Links to accessible-lab.css in tools folder
- ✓ Converts lists, figures, links automatically
- ✓ No complex LaTeX-generated classes

**Example Output:**
```html
<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Lab Title</title>
    <link href="../../tools/accessible-lab.css" rel="stylesheet" type="text/css">
</head>
<body>
    <header>
        <h1>Lab Title</h1>
        ...
    </header>
    <main>
        <section aria-labelledby="objectives">
            <h2 id="objectives">Objectives</h2>
            ...
        </section>
    </main>
</body>
</html>
```

## Usage from Makefile

Each labs directory has a Makefile. Just run:

```bash
cd IntroData/labs
make              # Convert all .tex files
make watch        # Auto-convert on changes (requires entr)
make clean        # Remove generated HTML
```

## Files

- `update-tex-outputs.sh` - **Interactive script to generate both PDF and HTML** (recommended for single files)
- `tex-to-clean-html.py` - Main HTML converter
- `Makefile` - Simple make interface for batch conversion
- `clean-html.py` - Post-processor for htlatex output
- `tex-to-accessible-html.sh` - Alternative using htlatex
- `watch-tex.sh` - Watch script for auto-conversion

## Requirements

### For HTML conversion only:
- Python 3 (usually pre-installed)
- Optional: `entr` for watch mode (`sudo apt-get install entr`)

### For PDF + HTML conversion (update-tex-outputs.sh):
- Python 3
- pdflatex (install with: `sudo apt-get install texlive-latex-base`)

No pandoc required!

## Test Results

Successfully converts:
- ✓ usesandabusesofdata.tex → Clean, accessible HTML
- ✓ bigdata.tex
- ✓ datasecurity.tex
- ✓ datavisualizations.tex
- ✓ finalproject.tex
- ✓ labtemplate.tex
- And more...

## Accessibility Features

The generated HTML includes:
- Semantic HTML5 elements
- ARIA labels for screen readers  
- Proper heading hierarchy (h1 → h2 → h3)
- Alt text for images (from \alt{} in .tex)
- Clean, readable structure
- Mobile-responsive viewport settings

Perfect for students using screen readers or other assistive technologies!
