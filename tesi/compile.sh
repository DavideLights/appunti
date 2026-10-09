#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[1/3] Converting Markdown files to LaTeX in latex/ directory..."
python3 convert_thesis.py

echo "[2/3] Compiling LaTeX (first pass)..."
(cd latex && pdflatex -interaction=nonstopmode main.tex > /dev/null)

echo "[3/3] Compiling LaTeX (second pass)..."
(cd latex && pdflatex -interaction=nonstopmode main.tex)

cp latex/main.pdf ./main.pdf
echo "Done! Generated main.pdf successfully at root."
