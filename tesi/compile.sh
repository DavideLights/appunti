#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
export PATH="$HOME/.local/bin:$HOME/.gemini/antigravity-ide/bin:$PATH"

echo "[1/4] Converting Markdown files to LaTeX in latex/ directory..."
python3 convert_thesis.py

echo "[2/4] Compiling LaTeX (first pass)..."
(cd latex && pdflatex -interaction=nonstopmode main.tex > /dev/null) || {
    echo "ERROR: LaTeX compilation failed in first pass! Showing last 35 lines of latex/main.log:" >&2
    tail -n 35 latex/main.log >&2
    exit 1
}

echo "[3/4] Generating Bibliography with BibTeX..."
(cd latex && bibtex main)

echo "[4/4] Finalizing PDF (two LaTeX passes for cross-references)..."
(cd latex && pdflatex -interaction=nonstopmode main.tex > /dev/null)
(cd latex && pdflatex -interaction=nonstopmode main.tex)

cp latex/main.pdf ./main.pdf
echo "Done! Generated main.pdf successfully at root."
