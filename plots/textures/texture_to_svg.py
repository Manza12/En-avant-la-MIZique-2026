import os
import subprocess
import shutil


def texture_to_latex(T, resolution, resolution_pos=None, x=0.5, add_rhythms=True):
    rows = len(T)
    cols = max(len(row) for row in T)
    lines = []
    lines.append(r"\begin{center}")
    lines.append(r"        \color{mycolor}")
    lines.append(r"        \begin{tikzpicture}[baseline=(current bounding box.center)]")
    lines.append(r"        % Commands")
    lines.append(f"        \\newcommand\\x{{{x}}}")
    lines.append(r"        \newcommand{\Cross}{$\mathbin{\tikz [x=3*\x ex,y=3*\x ex,line width=0.5*\x ex] \draw (0,0) -- (1,1) (0,1) -- (1,0);}$}")
    lines.append(r"        \newcommand{\Cdot}{\tikz\draw[mycolor,fill=mycolor] (0,0) circle (0.5*\x ex);}")
    lines.append(r"        % Grid")
    lines.append(f"        \\draw[step=\\x cm,color=mycolor] (0,0) grid ({cols}*\\x,{rows}*\\x);")
    lines.append(f"        \\foreach \\i in {{1, 2, ..., {rows}}}{{")
    lines.append(f"            \\dxcolorraw[thick] (0,\\i*\\x-\\x) rectangle ({cols}*\\x, \\i*\\x);")
    lines.append(r"        }")
    lines.append(r"        % Values")
    for row_idx, row in enumerate(T):
        row_num = row_idx + 1
        for col_idx, val in enumerate(row):
            if val == 0:
                continue
            col_num = col_idx + 1
            symbol = r"\Cross" if val == 2 else r"\Cdot"
            x_pos = f"{col_num}*\\x - \\x/2"
            y_pos = f"{row_num}*\\x - \\x/2"
            lines.append(f"        \\node at ({x_pos},{y_pos}) {{{symbol}}};")
    lines.append(r"        % Ticks")
    lines.append(f"        \\node at (0*\\x, -\\x/2) {{$0$}};")
    pos = resolution_pos if resolution_pos is not None else cols
    lines.append(f"        \\node at ({pos}*\\x, -\\x/2) {{$\\{resolution}$}};")
    for row_idx in range(rows):
        row_num = row_idx + 1
        if add_rhythms:
            lines.append(f"        \\node at (-\\x, {row_num}*\\x - \\x/2) {{$R_{{{row_num}}}$}};")
    lines.append(r"    \end{tikzpicture}")
    lines.append(r"\end{center}")
    return "\n".join(lines)


def texture_to_svg(T, resolution, output_svg, resolution_pos=None, x=0.5, add_rhythms=True,
                   inkscape_path=r"C:\Program Files\Inkscape\bin\inkscape.exe"):
    # Usamos C:\Tmp como directorio de trabajo para evitar rutas con caracteres especiales
    safe_dir = r"C:\Tmp\texture_latex"
    os.makedirs(safe_dir, exist_ok=True)

    tex_path = os.path.join(safe_dir, "texture.tex")
    pdf_path = os.path.join(safe_dir, "texture.pdf")
    svg_path = os.path.join(safe_dir, "texture.svg")

    tikz_body = texture_to_latex(T, resolution=resolution, resolution_pos=resolution_pos, x=x, add_rhythms=add_rhythms)

    full_tex = (
        "\\documentclass{standalone}\n"
        "\\usepackage{amsmath}\n"
        "\\usepackage{amssymb}\n"
        "\\usepackage{tikz}\n"
        "\\usepackage{harmony}\n"
        "\\usepackage{xcolor}\n"
        "\\definecolor{mycolor}{RGB}{0,60,102}\n"
        "\\pagestyle{empty}\n"
        "\\begin{document}\n"
        + tikz_body + "\n"
        + "\\end{document}\n"
    )

    # 1. Escribir el .tex en ruta segura
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(full_tex)

    # 2. Compilar con pdflatex
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", safe_dir, tex_path],
        capture_output=True, text=True
    )
    if not os.path.exists(pdf_path):
        print("ERROR: pdflatex fallo. Log:")
        print(result.stdout[-3000:])
        return False

    # 3. Convertir PDF -> SVG con Inkscape
    result = subprocess.run(
        [inkscape_path,
         "--pdf-poppler",
         pdf_path,
         "--export-type=svg",
         f"--export-filename={svg_path}"],
        capture_output=True, text=True
    )
    if not os.path.exists(svg_path):
        print("ERROR: Inkscape fallo.")
        print(result.stderr)
        return False

    # 4. Copiar SVG al destino final
    shutil.copy(svg_path, output_svg)
    print(f"SVG generado: {output_svg}")
    return True


# ── Ejemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    T = [
        [2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1],
        [2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
    ]

    texture_to_svg(
        T,
        resolution="Vier",
        output_svg="texture.svg",
    )