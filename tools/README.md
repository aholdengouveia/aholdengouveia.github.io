# TEX to HTML Conversion Tools

Convert .tex files to clean, accessible HTML.

## Quick Start

### Convert a Single File

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
- ✓ Links to whatisdata.css
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
    <link href="whatisdata.css" rel="stylesheet" type="text/css">
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

- `tex-to-clean-html.py` - Main converter (recommended)
- `Makefile` - Simple make interface
- `clean-html.py` - Post-processor for htlatex output
- `tex-to-accessible-html.sh` - Alternative using htlatex
- `watch-tex.sh` - Watch script

## Requirements

- Python 3 (usually pre-installed)
- Optional: `entr` for watch mode (`sudo apt-get install entr`)

No pandoc or other tools required!

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
