#!/usr/bin/env python3
import os
import re
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path("/home/davidel/appunti/tesi").resolve()
LATEX_DIR = BASE_DIR / "latex"
PANDOC_BIN = BASE_DIR / "pandoc-3.1.11.1" / "bin" / "pandoc"
if not PANDOC_BIN.exists():
    PANDOC_BIN = "pandoc"

# Directories to strictly ignore as thesis chapters
IGNORED_DIRS = {"bozza", "context", "latex", ".git", ".vscode", ".obsidian", "src"}

def section_sort_key(p: Path):
    """
    Extract leading section numbers as a tuple of ints:
    e.g. 1.1 -> (0, (1, 1), name)
         1.3 -> (0, (1, 3), name)
         1.3.1 -> (0, (1, 3, 1), name)
    """
    m = re.match(r'^(\d+(?:[\._]\d+)*)', p.name)
    if m:
        num_str = m.group(1).replace('_', '.')
        try:
            return (0, tuple(int(x) for x in num_str.split('.') if x.isdigit()), p.name.lower())
        except ValueError:
            pass
    return (1, (), p.name.lower())

def preprocess_markdown(text: str) -> str:
    # 1. Clean box-drawing characters for LaTeX listings compatibility
    box_map = {
        '├': '+', '└': '+', '┌': '+', '┐': '+', '┘': '+', '┴': '+', '┬': '+', '┼': '+',
        '─': '-', '│': '|', '═': '=', '║': '|', '▶': '>', '◀': '<', '▲': '^', '▼': 'v',
        '→': '->', '←': '<-'
    }
    for char, replacement in box_map.items():
        text = text.replace(char, replacement)

    # 2. Transform Obsidian image embeds: ![[src/images/pic.png]] or ![[pic.png|400]] -> ![](...)
    def replace_image(match):
        img_target = match.group(1).strip()
        if "|" in img_target:
            img_target = img_target.split("|")[0].strip()
        if not img_target.startswith("src/") and (BASE_DIR / "src" / "images" / img_target).exists():
            img_target = f"src/images/{img_target}"
        return f"![]({img_target})"

    text = re.sub(r'!\[\[(.*?)\]\]', replace_image, text)

    # 3. Transform Obsidian wikilinks: [[target|alias]] -> alias, [[target]] -> target
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)

    # 4. Clean and map section headers:
    lines = []
    for line in text.splitlines():
        header_match = re.match(r'^(#+)\s*(\d+(?:\.\d+)+)\s*(.*)$', line)
        if header_match:
            hashes, num_str, title = header_match.groups()
            dots = num_str.count('.')
            new_level = max(1, min(dots, 4))
            new_hashes = "#" * new_level
            title = title.strip()
            if not title:
                title = num_str
            lines.append(f"{new_hashes} {title}")
        else:
            lines.append(line)
    return "\n".join(lines)

def deduplicate_footnotes(tex: str, global_fn_map: dict) -> str:
    """
    Finds all \\footnote{...} in the generated LaTeX.
    If the exact footnote content was already defined, replaces duplicate
    occurrences with \\footref{label}.
    The first occurrence gets \\footnote{\\label{label}...}.
    """
    idx = 0
    pieces = []
    last_end = 0

    while True:
        pos = tex.find(r'\footnote{', idx)
        if pos == -1:
            pieces.append(tex[last_end:])
            break

        pieces.append(tex[last_end:pos])

        depth = 1
        i = pos + len(r'\footnote{')
        while i < len(tex) and depth > 0:
            if tex[i] == '{' and tex[i-1] != '\\':
                depth += 1
            elif tex[i] == '}' and tex[i-1] != '\\':
                depth -= 1
            i += 1

        fn_body = tex[pos + len(r'\footnote{') : i - 1]
        norm_key = re.sub(r'\s+', ' ', fn_body.strip())

        if norm_key in global_fn_map:
            label = global_fn_map[norm_key]
            pieces.append(f"\\footref{{{label}}}")
        else:
            label = f"fn:ref_{len(global_fn_map) + 1}"
            global_fn_map[norm_key] = label
            pieces.append(f"\\footnote{{\\label{{{label}}}{fn_body}}}")

        last_end = i
        idx = i

    return "".join(pieces)

def format_images(tex: str) -> str:
    """
    Wraps standalone \\includegraphics in a properly centered figure environment
    with max width bounded to \\linewidth to prevent overflowing A4 pages.
    """
    def repl_img(m):
        path = m.group(1).strip()
        base_name = os.path.splitext(os.path.basename(path))[0]
        clean_title = base_name.replace('-', ' ').replace('_', ' ').title()
        return (
            "\n\\begin{figure}[htbp]\n"
            "  \\centering\n"
            f"  \\includegraphics[width=0.85\\linewidth,height=0.65\\textheight,keepaspectratio]{{{path}}}\n"
            f"  \\caption{{{clean_title}}}\n"
            f"  \\label{{fig:{base_name}}}\n"
            "\\end{figure}\n"
        )

    pattern = r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}'
    return re.sub(pattern, repl_img, tex)

def convert_md_file(md_path: Path, target_dir: Path, global_fn_map: dict) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    tex_path = target_dir / (md_path.stem + ".tex")
    print(f"Converting: {md_path.relative_to(BASE_DIR)} -> {tex_path.relative_to(BASE_DIR)}")

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write("% Sezione vuota\n")
        return tex_path

    processed_content = preprocess_markdown(content)

    cmd = [
        str(PANDOC_BIN),
        "-f", "gfm+footnotes",
        "-t", "latex",
        "--listings"
    ]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(processed_content)
    if p.returncode != 0:
        print(f"Error converting {md_path}: {err}", file=sys.stderr)
        raise RuntimeError(err)

    out = deduplicate_footnotes(out, global_fn_map)
    out = format_images(out)

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(out)

    return tex_path

def format_chapter_title(dir_name: str) -> str:
    cleaned = re.sub(r'^\d+[\._\s]*', '', dir_name).replace('_', ' ').strip()
    return cleaned if cleaned else dir_name

def main():
    print("=== Starting Thesis Markdown to LaTeX Conversion ===")
    LATEX_DIR.mkdir(parents=True, exist_ok=True)
    
    chapter_dirs = []
    for item in sorted(BASE_DIR.iterdir()):
        if item.is_dir() and item.name not in IGNORED_DIRS and not item.name.startswith("pandoc-"):
            md_files = list(item.glob("*.md"))
            if md_files:
                chapter_dirs.append(item)

    print(f"Found active chapter directories: {[d.name for d in chapter_dirs]}")

    global_fn_map = {}
    includes_code = []

    for c_dir in chapter_dirs:
        md_files = sorted(c_dir.glob("*.md"), key=section_sort_key)
        tex_files = []
        target_sub_dir = LATEX_DIR / c_dir.name
        for md in md_files:
            tex_file = convert_md_file(md, target_sub_dir, global_fn_map)
            tex_files.append(tex_file)

        chapter_title = format_chapter_title(c_dir.name)
        wrapper_name = f"{chapter_title.replace(' ', '_')}.tex"
        wrapper_path = LATEX_DIR / wrapper_name
        print(f"Generating wrapper: {wrapper_name}")

        with open(wrapper_path, "w", encoding="utf-8") as f:
            f.write(f"% Capitolo: {chapter_title}\n")
            f.write(f"\\chapter{{{chapter_title}}}\n\n")
            for tf in tex_files:
                rel = tf.relative_to(LATEX_DIR).as_posix()
                rel_no_ext = os.path.splitext(rel)[0]
                f.write(f"\\input{{{rel_no_ext}}}\n")

        wrapper_no_ext = os.path.splitext(wrapper_name)[0]
        includes_code.append(
            f"\\fancyhead[R]{{{chapter_title}}} \\fancyfoot[L]{{{chapter_title}}}\n"
            f"\\include{{{wrapper_no_ext}}}\n"
        )

    # Ensure Bibliography.bib exists in LATEX_DIR
    bib_file = LATEX_DIR / "Bibliography.bib"
    if not bib_file.exists():
        with open(bib_file, "w", encoding="utf-8") as f:
            f.write("% Bibliografia della tesi\n")

    # Generate main.tex from template.tex inside LATEX_DIR
    template_file = LATEX_DIR / "template.tex"
    if not template_file.exists() and (BASE_DIR / "template.tex").exists():
        template_file = BASE_DIR / "template.tex"

    main_file = LATEX_DIR / "main.tex"
    print(f"Generating unified LaTeX master file: {main_file.relative_to(BASE_DIR)}")
    
    with open(template_file, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Apply fixes
    content = template_content.replace(r"\usepackage[italian]{babel}", r"\usepackage[italian,provide=*]{babel}")
    content = re.sub(r'\\baselineskip\s*=\s*\d+pt', r'\\linespread{1.15}\\selectfont', content)

    pre_begin_doc = r"""
% Support for pandoc-generated LaTeX & listings styling
\usepackage[plainpages=false,pdfpagelabels]{hyperref}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{calc}
\usepackage{textcomp}
\setlength{\headheight}{15pt}
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\newcommand{\passthrough}[1]{#1}

% Search images in parent root as well
\graphicspath{{../}{./}}

% Global image constraints: never exceed text width or height
\makeatletter
\def\maxwidth{\ifdim\Gin@nat@width>\linewidth\linewidth\else\Gin@nat@width\fi}
\def\maxheight{\ifdim\Gin@nat@height>\textheight\textheight\else\Gin@nat@height\fi}
\makeatother
\setkeys{Gin}{width=\maxwidth,height=\maxheight,keepaspectratio}

\lstset{
    basicstyle=\ttfamily\footnotesize,
    breaklines=true,
    numbers=left,
    numberstyle=\tiny\color{gray},
    keywordstyle=\color{blue}\bfseries,
    commentstyle=\color{olive}\itshape,
    stringstyle=\color{teal},
    showstringspaces=false,
    frame=lines
}

\begin{document}
"""
    content = content.replace(r"\begin{document}", pre_begin_doc)

    pattern = r"(\\fancyhead\[R\]\{Introduzione\}.*?\\include\{Dataset\})"
    replacement_includes = "\n".join(includes_code)
    
    content = re.sub(pattern, lambda m: replacement_includes, content, flags=re.DOTALL)

    with open(main_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"=== Conversion Completed Successfully! Total unique footnotes: {len(global_fn_map)} ===")

if __name__ == "__main__":
    main()
