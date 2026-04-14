#!/bin/bash
# Watch for changes to .tex files and automatically convert to HTML
# Usage: ./watch-and-convert.sh

echo "Watching for changes to .tex files in $(pwd)"
echo "Press Ctrl+C to stop"
echo ""

# Check if inotifywait is available
if ! command -v inotifywait &> /dev/null; then
    echo "Error: inotifywait is not installed"
    echo "Install with: sudo apt-get install inotify-tools"
    exit 1
fi

# Check if pandoc is available
if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc is not installed"
    echo "Install with: sudo apt-get install pandoc"
    exit 1
fi

# Function to convert .tex to .html
convert_tex_to_html() {
    local tex_file="$1"
    local html_file="${tex_file%.tex}.html"
    local title=$(grep '\\title{' "$tex_file" | sed 's/.*{\(.*\)}/\1/' | head -1)

    echo "Converting $tex_file..."

    pandoc "$tex_file" \
        --from latex \
        --to html5 \
        --standalone \
        --css=whatisdata.css \
        --metadata title="$title" \
        --metadata lang=en-US \
        --output "$html_file"

    if [ $? -eq 0 ]; then
        echo "✓ Created $html_file at $(date '+%H:%M:%S')"
    else
        echo "✗ Failed to convert $tex_file"
    fi
}

# Initial conversion of all .tex files
echo "Initial conversion of all .tex files..."
for tex_file in *.tex; do
    if [ -f "$tex_file" ]; then
        convert_tex_to_html "$tex_file"
    fi
done

echo ""
echo "Now watching for changes..."
echo ""

# Watch for changes and convert
inotifywait -m -e close_write,moved_to,create --format '%f' *.tex 2>/dev/null | while read file; do
    if [[ "$file" == *.tex ]]; then
        convert_tex_to_html "$file"
    fi
done
