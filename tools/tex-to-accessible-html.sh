#!/bin/bash
# Convert .tex to accessible HTML
# Works around accessibility package issues with make4ht

TARGET_DIR="${1:-.}"

# Check if directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory $TARGET_DIR does not exist"
    exit 1
fi

cd "$TARGET_DIR" || exit 1

echo "Converting .tex files in $(pwd) to accessible HTML"
echo ""

# Function to convert one file
convert_file() {
    local tex_file="$1"
    local base="${tex_file%.tex}"
    local html_file="${base}.html"
    local temp_tex="${base}_temp.tex"

    echo "Converting $tex_file..."

    # Create temporary tex file without accessibility package
    sed '/\\usepackage\[tagged, highstructure\]{accessibility}/d' "$tex_file" > "$temp_tex"

    # Convert using htlatex with clean options
    htlatex "$temp_tex" "xhtml,charset=utf-8,fn-in" " -cunihtf -utf8" > /dev/null 2>&1

    # Move the generated HTML to correct name
    if [ -f "${base}_temp.html" ]; then
        mv "${base}_temp.html" "$html_file"

        # Post-process HTML to make it more accessible
        # Find the tools directory
        SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" 2>/dev/null && pwd )"
        if [ -z "$SCRIPT_DIR" ]; then
            SCRIPT_DIR="$(dirname "$(dirname "$(pwd)")")/tools"
        fi

        if python3 "$SCRIPT_DIR/clean-html.py" "$html_file" 2>&1; then
            echo "✓ Created $html_file"
        else
            echo "⚠ Warning: HTML cleaning failed, but file created"
        fi

        # Clean up temporary files
        rm -f "${base}_temp."* "${base}.aux" "${base}.log" "${base}.4ct" "${base}.4tc" \
              "${base}.dvi" "${base}.idv" "${base}.lg" "${base}.tmp" "${base}.xref" \
              "${base}.css" 2>/dev/null
    else
        echo "✗ Failed to convert $tex_file"
    fi

    # Remove temporary tex file
    rm -f "$temp_tex"
}

# Convert all .tex files
count=0
for tex_file in *.tex; do
    if [ -f "$tex_file" ]; then
        convert_file "$tex_file"
        ((count++))
    fi
done

if [ $count -eq 0 ]; then
    echo "No .tex files found"
else
    echo ""
    echo "✓ Converted $count file(s)"
fi
