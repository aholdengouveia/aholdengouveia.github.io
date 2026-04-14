#!/bin/bash
# Universal TEX to HTML converter
# Usage:
#   ./convert-tex-to-html.sh <directory>
#   ./convert-tex-to-html.sh                    (uses current directory)

# Set target directory
TARGET_DIR="${1:-.}"

# Check if directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory $TARGET_DIR does not exist"
    exit 1
fi

# Change to target directory
cd "$TARGET_DIR" || exit 1

echo "Converting .tex files in $(pwd)"
echo ""

# Check if pandoc is available
if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc is not installed"
    echo "Install with: sudo apt-get install pandoc"
    exit 1
fi

# Find CSS file (look in current dir, parent dir, or use default)
CSS_FILE=""
if [ -f "whatisdata.css" ]; then
    CSS_FILE="whatisdata.css"
elif [ -f "../whatisdata.css" ]; then
    CSS_FILE="../whatisdata.css"
elif [ -f "style.css" ]; then
    CSS_FILE="style.css"
else
    echo "Warning: No CSS file found. HTML will be generated without styling."
fi

# Function to convert .tex to .html
convert_tex_to_html() {
    local tex_file="$1"
    local html_file="${tex_file%.tex}.html"
    local title=$(grep '\\title{' "$tex_file" | sed 's/.*{\(.*\)}/\1/' | head -1)

    echo "Converting $tex_file..."

    local pandoc_cmd="pandoc \"$tex_file\" \
        --from latex \
        --to html5 \
        --standalone \
        --metadata lang=en-US \
        --output \"$html_file\""

    # Add CSS if found
    if [ -n "$CSS_FILE" ]; then
        pandoc_cmd="$pandoc_cmd --css=\"$CSS_FILE\""
    fi

    # Add title if found
    if [ -n "$title" ]; then
        pandoc_cmd="$pandoc_cmd --metadata title=\"$title\""
    fi

    eval $pandoc_cmd

    if [ $? -eq 0 ]; then
        echo "✓ Created $html_file"
    else
        echo "✗ Failed to convert $tex_file"
    fi
}

# Convert all .tex files
count=0
for tex_file in *.tex; do
    if [ -f "$tex_file" ]; then
        convert_tex_to_html "$tex_file"
        ((count++))
    fi
done

if [ $count -eq 0 ]; then
    echo "No .tex files found in $TARGET_DIR"
else
    echo ""
    echo "✓ Converted $count file(s)"
fi
