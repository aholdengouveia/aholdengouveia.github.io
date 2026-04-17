# Tools Improvement TODO List

Tracking improvements and enhancements for the LaTeX accessibility toolkit.

## Legend
- **Status:** ⏳ Not Started | 🔄 In Progress | ✅ Completed | ❌ Won't Fix
- **Effort:** 🟢 Low (<30 min) | 🟡 Medium (1-3 hours) | 🔴 High (>3 hours)
- **Priority:** ⭐ Quick Win | 🔥 High | 📌 Medium | 💡 Nice-to-Have

---

## ⭐ Quick Wins (Easy, High Impact)
_These can be done quickly and provide immediate value_

### QW1. Add Version Number to Scripts ⏳
**Effort:** 🟢 Low (5 min) | **Impact:** Helps users know if they have latest version

Add `__version__ = "1.0.0"` to latex-accessibility.py and tex-to-html.py. Show version with `--version` flag.

**How to test:**
```bash
python3 latex-accessibility.py --version
# Should output: LaTeX Accessibility Tool v1.0.0
```

---

### QW2. Add Example Section to README ✅
**Effort:** 🟢 Low (15 min) | **Impact:** Helps new users get started faster

Add "Quick Example" section at top of ACCESSIBILITY_README.md showing before/after .tex file.

**How to test:** Read through README, verify example is clear and accurate.

**Status:** ✅ COMPLETED - Added concise before/after example showing key changes (packages, bookmarks, URL wrapping) with visual annotations.

---

### QW3. Add Summary Statistics to Batch Operations ⏳
**Effort:** 🟢 Low (20 min) | **Impact:** Better feedback for users

At end of `add-all` or `fix-all`, show:
- Total files processed
- Files modified vs. already compliant
- Any errors encountered

**How to test:**
```bash
python3 latex-accessibility.py add-all IntroLinux/labs/

# Should show summary like:
# ✓ Processed 14 files
#   - Modified: 12 files
#   - Already compliant: 2 files
#   - Errors: 0 files
```

---

### QW4. Add --help Text with Examples ⏳
**Effort:** 🟢 Low (15 min) | **Impact:** Better discoverability

Enhance `--help` output to include common examples for each command.

**How to test:**
```bash
python3 latex-accessibility.py --help
# Should show usage, commands, and examples
```

---

### QW5. Add Troubleshooting Section to README ⏳
**Effort:** 🟢 Low (20 min) | **Impact:** Reduces support questions

Add common issues and solutions:
- "TeX capacity exceeded" error
- "Package not found" errors
- Permission denied errors
- UTF-8 encoding issues

**How to test:** Review section for completeness and clarity.

---

### QW6. Color-Coded Output ⏳
**Effort:** 🟢 Low (30 min) | **Impact:** Easier to scan output

Add color to terminal output:
- ✅ Green for success
- ❌ Red for errors
- ⚠️  Yellow for warnings
- ℹ️  Blue for info

Use colorama library with fallback for Windows compatibility.

**How to test:** Run on Linux/Mac/Windows, verify colors display correctly or fall back gracefully.

---

## 🔥 High Priority Improvements
_Important features that significantly improve the toolkit_

### HP1. LaTeX Package Detection and Installation ✅
**Effort:** 🟡 Medium (2-3 hours) | **Priority:** 🔥 High

**What it does:**
Automatically detect if required LaTeX packages are installed and show OS-specific installation commands.

**Why it matters:**
New users often get confused by "package not found" errors. This would make setup much easier.

**How to implement:**
1. Check for packages: bookmark, enumitem, hyperref, accessibility
2. Detect OS (Linux, Mac, Windows)
3. Show appropriate installation command for that OS
4. Could check by trying to compile a minimal .tex file

**How to test:**
```bash
python3 latex-accessibility.py check-packages

# On Ubuntu without packages:
# ❌ Missing LaTeX packages: bookmark, enumitem
#
# To install on Ubuntu/Debian:
#   sudo apt-get install texlive-latex-extra
#
# On Mac:
#   brew install --cask mactex
```

**Status:** ✅ COMPLETED - Added check-packages command that:
- Detects if LaTeX is installed (checks for kpsewhich)
- Checks for required packages (hyperref, bookmark, enumitem)
- Checks for optional packages (accessibility)
- Detects OS (Ubuntu/Debian, Fedora/RHEL, Mac, Windows, generic Linux)
- Provides OS-specific installation instructions
- Returns exit code 0 for success, 1 for missing packages

---

### HP2. Backup/Restore Functionality ⏳
**Effort:** 🟡 Medium (1-2 hours) | **Priority:** 🔥 High

**What it does:**
Automatically create backups before modifying files, with ability to restore if something goes wrong.

**Why it matters:**
Users are nervous about tools modifying their .tex files. Backups provide peace of mind.

**How to implement:**
1. Add `--backup` flag (or make it default?)
2. Copy file to `.bak` before making changes
3. Add `restore` command to revert changes
4. Maybe keep a log of what was backed up when

**How to test:**
```bash
# Modify with backup
python3 latex-accessibility.py add --backup myfile.tex
# Should create myfile.tex.bak

# Restore if needed
python3 latex-accessibility.py restore myfile.tex
# Restores from myfile.tex.bak

# List all backups
python3 latex-accessibility.py list-backups
```

---

### HP3. Batch Processing with Progress ⏳
**Effort:** 🟢 Low (30 min) | **Priority:** 🔥 High

**What it does:**
Show progress when processing multiple files: "Processing 5 of 14..."

**Why it matters:**
Users don't know if the tool is working or frozen when processing many files.

**How to implement:**
1. Count total .tex files first
2. Show "Processing file X of Y: filename.tex"
3. Optional: use tqdm library for fancy progress bar (with fallback)
4. Show summary at end (files modified, skipped, errors)

**How to test:**
```bash
python3 latex-accessibility.py add-all IntroLinux/labs/

# Should show:
# Processing file 1 of 14: shellbasics.tex
# ✓ Added features to shellbasics.tex
# Processing file 2 of 14: shellcond.tex
# ○ shellcond.tex already compliant
# ...
# ✓ Processed 14 files (12 modified, 2 already compliant)
```

---

## 📌 Medium Priority Improvements
_Useful features that enhance usability_

### MP1. Dry Run Mode (Preview Changes) ⏳
**Effort:** 🟢 Low (30 min) | **Priority:** 📌 Medium

**What it does:**
See what would change WITHOUT actually modifying files.

**Why it matters:**
Users want to preview before committing to changes, especially on important files.

**How to implement:**
1. Add `--dry-run` or `--preview` flag
2. Show what changes would be made
3. Don't write any files
4. Could show a diff-style output

**How to test:**
```bash
python3 latex-accessibility.py add --dry-run myfile.tex

# Should show what would change but NOT modify file:
# Would add packages: bookmark, enumitem
# Would add bookmarksetup configuration
# Would add accessibility notice
# File NOT modified (dry run)
```

---

### MP2. Validation and Verification ⏳
**Effort:** 🟡 Medium (1-2 hours) | **Priority:** 📌 Medium

**What it does:**
Test that .tex files still compile correctly after modifications.

**Why it matters:**
Catch errors immediately instead of finding out later when trying to compile.

**How to implement:**
1. Add `validate` command that runs pdflatex
2. Use `--interaction=nonstopmode` to catch errors
3. Parse output for errors
4. Report success or show errors
5. Clean up auxiliary files (.aux, .log, etc.)

**How to test:**
```bash
python3 latex-accessibility.py validate myfile.tex

# If compiles successfully:
# ✓ myfile.tex compiles successfully
# ✓ PDF generated: myfile.pdf
# ✓ Accessibility features detected

# If errors:
# ❌ myfile.tex failed to compile
# Error on line 42: Undefined control sequence
```

---

### MP3. Configuration File Support ⏳
**Effort:** 🟡 Medium (2 hours) | **Priority:** 📌 Medium

**What it does:**
Let users customize settings via config file instead of command-line flags.

**Why it matters:**
Easier to maintain consistent settings across a project.

**How to implement:**
1. Support `.latex-accessibility.yaml` or `.latex-accessibility.ini`
2. Look for config in current directory, then home directory
3. Allow customizing:
   - HTML URL pattern
   - Which packages to add
   - Custom accessibility notice text
   - Default backup behavior

**Example config:**
```yaml
# .latex-accessibility.yaml
html_url_pattern: "https://mysite.edu/{parent}/{section}/{filename}.html"
packages:
  - bookmark
  - enumitem
  - accessibility
backup_by_default: true
custom_notice: |
  This document is available in accessible formats at {html_url}
```

**How to test:**
Create config file, run tool, verify settings are used.

---

### MP4. Template System for Notices ⏳
**Effort:** 🟢 Low (45 min) | **Priority:** 📌 Medium

**What it does:**
Let users customize the accessibility notice with templates.

**Why it matters:**
Different institutions may have different wording requirements.

**How to implement:**
1. Create `templates/` directory with default template
2. Support variables: `{html_url}`, `{title}`, `{date}`, `{author}`
3. Look for custom template in project directory
4. Fall back to default if not found

**Template example:**
```latex
\section*{Accessibility}
Accessible version: \url{{html_url}}
Last updated: {date}
```

**How to test:**
Create custom template, run tool, verify custom text is used.

---

## 💡 Low Priority / Nice-to-Have
_Would be nice but not essential_

### LP1. Git Integration ⏳
**Effort:** 🟢 Low (30 min) | **Priority:** 💡 Nice-to-Have

**What it does:**
Automatically commit changes with descriptive message.

**Why it matters:**
Saves time for users who want changes tracked in git.

**How to implement:**
1. Add `--commit` flag
2. Check if directory is a git repo
3. Create commit with message listing modified files
4. Warn if there are uncommitted changes first

**How to test:**
```bash
python3 latex-accessibility.py add-all --commit labs/

# Creates git commit:
# "Add accessibility features to 14 lab files
#
# Modified: shellbasics.tex, shellcond.tex, ..."
```

---

### LP2. Interactive Mode / Wizard ⏳
**Effort:** 🟡 Medium (2 hours) | **Priority:** 💡 Nice-to-Have

**What it does:**
Step-by-step wizard for users who prefer interactive prompts.

**Why it matters:**
Some users prefer guided experience over command-line flags.

**How to implement:**
1. Add `interactive` command
2. Prompt for: file/directory, HTML URL, which features to add
3. Show preview of changes
4. Confirm before applying
5. Use arrow keys for navigation (library: `questionary` or `inquirer`)

**How to test:**
```bash
python3 latex-accessibility.py interactive

# Wizard prompts:
# 1. Select file or directory: [browse]
# 2. HTML URL pattern: [input]
# 3. Features to add: [✓] Packages [✓] Bookmarks [✓] Notice
# 4. Preview changes? [Yes/No]
# 5. Apply changes? [Yes/No]
```

---

### LP3. HTML Conversion Enhancements ⏳
**Effort:** 🔴 High (4+ hours) | **Priority:** 💡 Nice-to-Have

**What it does:**
Improve tex-to-html.py with better math, tables, and figure support.

**Why it matters:**
Current HTML converter handles basic content well, but struggles with complex LaTeX.

**Areas to improve:**
- Better math conversion (MathJax rendering)
- Improved table formatting and responsiveness
- Figure/image handling with alt text
- Code block syntax highlighting
- Better list handling
- Citation and bibliography support

**How to test:**
Create test .tex files with complex content and verify HTML output.

---

### LP4. Accessibility Compliance Report ⏳
**Effort:** 🟡 Medium (2-3 hours) | **Priority:** 💡 Nice-to-Have

**What it does:**
Generate detailed report on accessibility compliance for a file or directory.

**Why it matters:**
Helps track progress and identify which files need work.

**Report should include:**
- Which files are compliant vs. need work
- What's missing from each file
- WCAG compliance level (A, AA, AAA)
- PDF/UA compliance
- Suggestions for improvement
- Export to HTML, PDF, or JSON

**How to test:**
```bash
python3 latex-accessibility.py report labs/ --output report.html

# Generates HTML report showing:
# - 12 of 14 files compliant
# - shellbasics.tex: Missing accessibility notice
# - networking.tex: Missing bookmark configuration
```

---

### LP5. Extended LaTeX Environment Support ⏳
**Effort:** 🔴 High (5+ hours) | **Priority:** 💡 Nice-to-Have

**What it does:**
Handle more LaTeX environments and commands for better accessibility.

**Environments to support:**
- Figures with alt text: `\caption{text}` → add alt text hints
- Tables: accessibility improvements (header rows, captions)
- Code listings: proper semantic markup
- Equations: ensure numbered for reference
- Theorems/proofs: proper semantic structure
- Bibliography: accessible citations
- Index: accessible index generation

**How to test:**
Create comprehensive test .tex with all environments, verify proper handling.

---

## 📚 Documentation Improvements
_Making the tools easier to learn and use_

### DOC1. Quick Start Video Tutorial ⏳
**Effort:** 🔴 High (3+ hours) | **Priority:** 💡 Nice-to-Have

**What to create:**
Short (5-10 min) video showing:
1. Installation and setup
2. Making a single file accessible
3. Batch processing a directory
4. Viewing results

**Where to host:**
YouTube or similar, link from README

---

### DOC2. FAQ Section ⏳
**Effort:** 🟢 Low (30 min) | **Priority:** 📌 Medium

**What to add:**
Add FAQ section to ACCESSIBILITY_README.md answering:

**Q: When do I use `add` vs `fix`?**
A: Use `add` for new files or adding missing features. Use `fix` when you have compilation errors from malformed structure.

**Q: The tool says "already has accessibility features" but my PDF lacks bookmarks. Why?**
A: The tool checks for packages and configuration, but PDF generation is separate. Run `pdflatex myfile.tex` to regenerate the PDF.

**Q: Can I customize the HTML URL pattern?**
A: Currently no, but config file support is planned (see TODO). For now, edit the HTML URL in your .tex file manually.

**Q: I got "TeX capacity exceeded" error. What now?**
A: Run `python3 latex-accessibility.py fix myfile.tex` to fix structural issues.

**Q: Does this work on Windows?**
A: Yes! Python 3 works on Windows. For LaTeX, install MiKTeX or TeX Live.

---

### DOC3. Expand Examples Section ⏳
**Effort:** 🟢 Low (20 min) | **Priority:** 📌 Medium

**What to add:**
Add more before/after examples in ACCESSIBILITY_README.md:
- File with malformed structure → fixed
- File missing packages → packages added
- Plain URLs → wrapped in \url{}
- Complete workflow: .tex → accessible .tex → PDF → HTML

---

### DOC4. Contributing Guide ⏳
**Effort:** 🟢 Low (30 min) | **Priority:** 💡 Nice-to-Have

**What to create:**
Add CONTRIBUTING.md with:
- How to report issues
- How to suggest improvements
- Code style guidelines
- Testing requirements
- Pull request process

---

### DOC5. Changelog ⏳
**Effort:** 🟢 Low (15 min initially) | **Priority:** 📌 Medium

**What to create:**
Add CHANGELOG.md to track:
- Version numbers
- New features
- Bug fixes
- Breaking changes

Keep it updated with each release.

---

## ♿ Accessibility of the Tools Themselves
_Making the tools accessible to all users_

### ACC1. Better Error Messages for Screen Reader Users ⏳
**Effort:** 🟢 Low (30 min) | **Priority:** 📌 Medium

**What to improve:**
Current messages use emojis (✓, ❌, ○) which may not read well on screen readers.

**How to fix:**
Add text equivalents:
- `✓` → `[SUCCESS]` or `✓ Success:`
- `❌` → `[ERROR]` or `❌ Error:`
- `○` → `[SKIP]` or `○ Skipped:`
- `⚠️` → `[WARNING]` or `⚠️ Warning:`

**How to test:**
Test with screen reader (NVDA, JAWS, VoiceOver) or just ensure text is always present.

---

### ACC2. Verbose Mode for Detailed Output ⏳
**Effort:** 🟢 Low (20 min) | **Priority:** 💡 Nice-to-Have

**What to add:**
Add `--verbose` flag for users who need more detailed output.

**Normal mode:**
```
✓ Added accessibility features to myfile.tex
```

**Verbose mode:**
```
✓ Added accessibility features to myfile.tex
  - Added package: bookmark
  - Added package: enumitem
  - Added bookmarksetup configuration
  - Added accessibility notice
  - Wrapped 3 plain URLs
```

---

### ACC3. Plain Text Output Mode ⏳
**Effort:** 🟢 Low (15 min) | **Priority:** 💡 Nice-to-Have

**What to add:**
Add `--plain` flag to disable all colors and emojis for accessibility or scripting.

**How to implement:**
Set flag that disables colorama colors and replaces emojis with text.

---

## 🧪 Testing Infrastructure
_Ensuring the tools work correctly_

### TEST1. Automated Test Suite ⏳
**Effort:** 🔴 High (4+ hours) | **Priority:** 📌 Medium

**What to create:**
Comprehensive test suite using pytest:

**Unit tests:**
- Test each function in isolation
- Test regex patterns
- Test file detection logic

**Integration tests:**
- Test full add workflow
- Test full fix workflow
- Test batch processing

**Test files:**
- Create sample .tex files with known issues
- Verify fixes are applied correctly
- Test edge cases (empty files, malformed LaTeX, etc.)

**How to run:**
```bash
# Install pytest
pip install pytest pytest-cov

# Run tests
pytest tests/

# With coverage report
pytest --cov=latex-accessibility tests/

# Should aim for >80% code coverage
```

---

### TEST2. Regression Test Suite ⏳
**Effort:** 🟡 Medium (1 hour) | **Priority:** 📌 Medium

**What to create:**
Tests for bugs that have been fixed to ensure they don't come back.

**Test cases:**
- Malformed hypersetup/bookmarksetup nesting (the big bug we fixed)
- UTF-8 encoding issues
- Files without \maketitle
- Files without hyperref package
- Empty files
- Binary files (should fail gracefully)

---

### TEST3. Cross-Platform Testing ⏳
**Effort:** 🟡 Medium (varies) | **Priority:** 📌 Medium

**What to test:**
Verify tools work on:
- Linux (Ubuntu, Debian, Fedora)
- macOS
- Windows (with Git Bash, PowerShell, WSL)

**What to verify:**
- Python script runs
- File paths work correctly (/ vs \)
- Encoding works (UTF-8)
- LaTeX packages can be detected
- Colors work or fallback gracefully

---

## 🔧 Additional LaTeX Features
_Specific LaTeX commands and environments to handle better_

### LAT1. Better \includegraphics Handling ⏳
**Effort:** 🟡 Medium (1-2 hours) | **Priority:** 💡 Nice-to-Have

**What to detect:**
Find `\includegraphics{image.png}` and suggest adding descriptions.

**What to suggest:**
```latex
% Before:
\includegraphics{diagram.png}

% After (suggestion):
\includegraphics{diagram.png}
% Alt text: [Add description here for accessibility]
```

---

### LAT2. Detect Missing Alt Text in Figures ⏳
**Effort:** 🟡 Medium (1 hour) | **Priority:** 💡 Nice-to-Have

**What to check:**
Ensure figures have \caption for accessibility.

**What to report:**
```
⚠️ Warning: Figure on line 42 has no \caption
  Suggestion: Add \caption{Description of figure}
```

---

### LAT3. Table Accessibility Checks ⏳
**Effort:** 🟡 Medium (1-2 hours) | **Priority:** 💡 Nice-to-Have

**What to check:**
- Tables should have \caption
- Consider suggesting header row markup
- Warn about complex tables that may not be accessible

---

### LAT4. Detect Color-Only Information ⏳
**Effort:** 🟡 Medium (1-2 hours) | **Priority:** 💡 Nice-to-Have

**What to detect:**
Use of `\textcolor` without additional cues (bold, italic, markers).

**What to suggest:**
```latex
% Potentially inaccessible:
\textcolor{red}{Important text}

% Better:
\textcolor{red}{\textbf{Important text}} % Also bold
```

---

## 🎯 Performance Improvements
_Making the tools faster_

### PERF1. Cache Compiled Regex Patterns ⏳
**Effort:** 🟢 Low (15 min) | **Priority:** 💡 Nice-to-Have

**What to do:**
Pre-compile regex patterns at module level instead of in functions.

**Why:**
Faster when processing many files.

---

### PERF2. Parallel Processing for Batch Operations ⏳
**Effort:** 🟡 Medium (1-2 hours) | **Priority:** 💡 Nice-to-Have

**What to do:**
Use multiprocessing to process multiple .tex files simultaneously.

**Why:**
Much faster for large directories (50+ files).

**How:**
Use `multiprocessing.Pool` to process files in parallel.

---

## 📋 Summary

**Quick Wins (Do First):** 6 items - 🟢 Low effort, high impact
**High Priority:** 3 items - Important features worth the effort
**Medium Priority:** 4 items - Nice improvements when you have time
**Low Priority:** 5 items - Would be nice eventually
**Documentation:** 5 items - Make tools easier to use
**Accessibility:** 3 items - Make tools themselves accessible
**Testing:** 3 items - Ensure quality and prevent bugs
**LaTeX Features:** 4 items - Handle more LaTeX edge cases
**Performance:** 2 items - Make tools faster

**Total:** 35 improvements tracked

---

## 🎬 Getting Started

**If you have 30 minutes:** Pick a Quick Win
**If you have 2-3 hours:** Tackle a High Priority item
**If you want to improve docs:** Work on Documentation section
**If you care about quality:** Add Testing infrastructure

Remember: **Done is better than perfect!** Start with Quick Wins to build momentum.
