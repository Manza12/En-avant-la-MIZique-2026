def texture_to_latex(T, resolution, x=0.5):
    """
    Genera código LaTeX (tikzpicture) a partir de una lista de listas.

    Convención de valores:
        0  → celda vacía
        1  → punto negro (Cdot)
        2  → cruz (Cross)

    Parámetros
    ----------
    T : list[list[int]]
        Filas de la textura. El índice 0 es la fila inferior (R1).
    x : float
        Tamaño de celda en ex (por defecto 0.5).
    """
    rows = len(T)
    cols = max(len(row) for row in T)

    lines = []

    # Cabecera
    lines.append(r"\begin{center}")
    lines.append(r"    T = \begin{tikzpicture}[baseline=(current bounding box.center)]")

    # Comandos internos
    lines.append(r"        % Commands")
    lines.append(f"        \\newcommand\\x{{{x}}}")
    lines.append(r"        \newcommand{\Cross}{$\mathbin{\tikz [x=3*\x ex,y=3*\x ex,line width=0.5*\x ex] \draw (0,0) -- (1,1) (0,1) -- (1,0);}$}")
    lines.append(r"        \newcommand{\Cdot}{\tikz\draw[black,fill=black] (0,0) circle (0.5*\x ex);}")

    # Grid
    lines.append(r"        % Grid")
    lines.append(f"        \\draw[step=\\x cm,color=gray] (0,0) grid ({cols}*\\x,{rows}*\\x);")
    lines.append(f"        \\foreach \\i in {{1, 2, ..., {rows}}}{{")
    lines.append(f"            \\draw[thick] (0,\\i*\\x-\\x) rectangle ({cols}*\\x, \\i*\\x);")
    lines.append(r"        }")

    # Valores
    lines.append(r"        % Values")
    for row_idx, row in enumerate(T):
        row_num = row_idx + 1          # fila 1-indexed desde abajo
        for col_idx, val in enumerate(row):
            if val == 0:
                continue
            col_num = col_idx + 1      # columna 1-indexed
            symbol = r"\Cross" if val == 2 else r"\Cdot"
            x_pos = f"{col_num}*\\x - \\x/2"
            y_pos = f"{row_num}*\\x - \\x/2"
            lines.append(f"        \\node at ({x_pos},{y_pos}) {{{symbol}}};")

    # Ticks
    lines.append(r"        % Ticks")
    lines.append(f"        \\node at (0*\\x, -\\x/2) {{$0$}};")
    lines.append(f"        \\node at ({cols}*\\x, -\\x/2) {{$\\{resolution}$}};")
    for row_idx in range(rows):
        row_num = row_idx + 1
        lines.append(f"        \\node at (-\\x, {row_num}*\\x - \\x/2) {{$R_{{{row_num}}}$}};")

    # Cierre
    lines.append(r"    \end{tikzpicture} \, .")
    lines.append(r"\end{center}")

    return "\n".join(lines)


# ── Ejemplo de uso ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    T = [
        [2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1],
        [2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
    ]

    latex_code = texture_to_latex(T, resolution='Vier')
    print(latex_code)