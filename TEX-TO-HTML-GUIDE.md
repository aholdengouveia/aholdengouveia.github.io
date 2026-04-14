# TEX to HTML Conversion Guide

Quick reference for converting .tex files to HTML across all lab directories.

## Setup (One Time)

```bash
sudo apt-get install pandoc inotify-tools
```

## Usage

### Method 1: From Any Lab Directory (Easiest)

```bash
cd IntroData/labs    # or AdvData/labs, InfoSec/labs, etc.
make                 # Convert all .tex files
make watch           # Auto-convert on file save
make clean           # Remove generated HTML
```

### Method 2: From Repository Root

```bash
# Convert specific directory
./tools/convert-tex-to-html.sh IntroData/labs

# Watch specific directory
./tools/watch-tex.sh AdvData/labs
```

### Method 3: Convert All Labs at Once

```bash
# One-time conversion of all directories
for dir in IntroData/labs AdvData/labs InfoSec/labs LinuxAdmin/labexcercises; do
    ./tools/convert-tex-to-html.sh "$dir"
done
```

## What Gets Created

Each .tex file generates a corresponding .html file:
- `whatisdata.tex` → `whatisdata.html`
- `bigdata.tex` → `bigdata.html`
- etc.

The HTML files:
- ✓ Use clean, accessible HTML5
- ✓ Link to whatisdata.css for styling
- ✓ Include proper metadata
- ✓ Preserve document structure

## Typical Workflow

1. **Edit your .tex file** in your preferred editor
2. **In a terminal, run:** `cd IntroData/labs && make watch`
3. **Save your .tex file**
4. **HTML auto-generates!**
5. **Refresh browser** to see changes

## Directory Structure

```
aholdengouveia.github.io/
├── tools/                          # Conversion tools (universal)
│   ├── README.md                   # Detailed documentation
│   ├── Makefile                    # Universal Makefile
│   ├── convert-tex-to-html.sh      # Convert script
│   ├── watch-tex.sh                # Watch script
│   └── watch-and-convert.sh        # Legacy script
│
├── IntroData/labs/
│   ├── Makefile                    # Links to tools/Makefile
│   ├── whatisdata.css              # Styling
│   ├── whatisdata.tex              # Source
│   └── whatisdata.html             # Generated
│
├── AdvData/labs/
│   └── Makefile                    # Links to tools/Makefile
│
├── InfoSec/labs/
│   └── Makefile                    # Links to tools/Makefile
│
└── LinuxAdmin/labexcercises/
    └── Makefile                    # Links to tools/Makefile
```

## Full Documentation

See [tools/README.md](tools/README.md) for complete documentation, troubleshooting, and advanced usage.

## Quick Commands Reference

| Command | Description |
|---------|-------------|
| `make` | Convert all .tex files in current directory |
| `make watch` | Watch and auto-convert on changes |
| `make clean` | Remove generated HTML files |
| `make help` | Show help message |

## Need Help?

Check the detailed documentation:
```bash
cat tools/README.md
```

Or see the Makefile help:
```bash
make help
```
