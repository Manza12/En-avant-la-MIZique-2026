"""
score_tree.py
=============
Extracts and visualizes the structural tree of a musictensors composition
by parsing its source file with Python's standard `ast` module.

Usage:
    python score_tree.py score.py [root_variable] [--html]

    - score.py        : source file of the composition
    - root_variable   : variable to analyze (defaults to the last composite
                        assignment found in the file)
    - --html          : open an interactive visualization in the browser

Examples:
    python score_tree.py sonata.py piece
    python score_tree.py sonata.py piece --html
    python score_tree.py sonata.py --html
"""

import ast
import json
import sys
import tempfile
import webbrowser
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Tree structure
# ---------------------------------------------------------------------------

OPERATOR_SYMBOLS = {
    "Mult":    "*",
    "Add":     "+",
    "MatMult": "@",
    "Pow":     "**",
}


@dataclass
class TreeNode:
    label: str                       # variable name or operator label
    op: Optional[str] = None         # None if this is a leaf node
    children: list = field(default_factory=list)

    def is_leaf(self) -> bool:
        return self.op is None

    def pprint(self, indent: int = 0, last: bool = True, prefix: str = "") -> str:
        connector = "└── " if last else "├── "
        line = prefix + (connector if indent > 0 else "") + self._label_str()
        child_prefix = prefix + ("    " if last else "│   ")
        lines = [line]
        for i, child in enumerate(self.children):
            is_last = (i == len(self.children) - 1)
            lines.append(child.pprint(indent + 1, is_last, child_prefix))
        return "\n".join(lines)

    def _label_str(self) -> str:
        if self.op:
            return f"[{self.op}]  {self.label}" if self.label else f"[{self.op}]"
        return self.label

    def to_dict(self) -> dict:
        d = {"label": self.label, "op": self.op}
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d


# ---------------------------------------------------------------------------
# Assignment collection
# ---------------------------------------------------------------------------

def collect_assignments(tree: ast.Module) -> dict[str, ast.expr]:
    """
    Walk the module and return a {name: expression} dict for every simple
    assignment (Name = expr). If a variable is reassigned, the last value wins.
    """
    assignments = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments[target.id] = node.value
        elif isinstance(node, ast.AugAssign):
            if isinstance(node.target, ast.Name):
                assignments[node.target.id] = node.value
    return assignments


# ---------------------------------------------------------------------------
# Recursive tree construction
# ---------------------------------------------------------------------------

def build_tree(
    expr: ast.expr,
    assignments: dict[str, ast.expr],
    visited: set[str],
    label: str = "",
) -> TreeNode:
    """
    Recursively build a TreeNode from an AST expression.

    - If it is a Name with a known assignment, descend into its definition.
    - If it is a BinOp, create an operator node with two children.
    - Calls, literals, or anything else become leaf nodes.
    """

    # --- Variable name ---
    if isinstance(expr, ast.Name):
        name = expr.id
        if name in assignments and name not in visited:
            visited = visited | {name}       # copy, do not mutate
            child = build_tree(assignments[name], assignments, visited, label=name)
            if child.is_leaf() and not child.label:
                child.label = name
            elif child.label != name:
                child.label = name
            return child
        else:
            # Leaf: variable not defined in this file (primitive or imported)
            return TreeNode(label=name or expr.id)

    # --- Binary operation ---
    if isinstance(expr, ast.BinOp):
        op_name = type(expr.op).__name__
        symbol = OPERATOR_SYMBOLS.get(op_name, op_name)
        left  = build_tree(expr.left,  assignments, visited)
        right = build_tree(expr.right, assignments, visited)
        return TreeNode(label=label, op=symbol, children=[left, right])

    # --- Function / method call ---
    if isinstance(expr, ast.Call):
        func = expr.func
        if isinstance(func, ast.Attribute):
            call_label = f"{_unparse_simple(func.value)}.{func.attr}()"
        elif isinstance(func, ast.Name):
            call_label = f"{func.id}()"
        else:
            call_label = "call()"
        return TreeNode(label=call_label)

    # --- Anything else: constant, tuple, unary op, etc. ---
    return TreeNode(label=label or ast.unparse(expr))


def _unparse_simple(node: ast.expr) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        return "?"


# ---------------------------------------------------------------------------
# Automatic root detection
# ---------------------------------------------------------------------------

def find_root(assignments: dict[str, ast.expr], all_names: list[str]) -> str:
    """
    Heuristic: find the last assigned variable that is not referenced by any
    other assignment — i.e. a root of the dependency graph.
    """
    referenced: set[str] = set()
    for expr in assignments.values():
        for node in ast.walk(expr):
            if isinstance(node, ast.Name):
                referenced.add(node.id)

    roots = [n for n in all_names if n not in referenced and n in assignments]
    if roots:
        return roots[-1]
    return all_names[-1]


# ---------------------------------------------------------------------------
# Associative flattening
# ---------------------------------------------------------------------------

def flatten_associative(node: TreeNode) -> TreeNode:
    """
    Collapse unbalanced chains of the same operator into n-ary nodes.
    E.g.  (a * (b * (c * d)))  ->  [*] with four children.
    """
    if node.is_leaf():
        return node
    node.children = [flatten_associative(c) for c in node.children]
    if node.op in ("*", "+"):
        merged = []
        for child in node.children:
            if not child.is_leaf() and child.op == node.op and not child.label:
                merged.extend(child.children)
            else:
                merged.append(child)
        node.children = merged
    return node


# ---------------------------------------------------------------------------
# Analysis entry point
# ---------------------------------------------------------------------------

def analyze(source_path: str, root_var: Optional[str] = None) -> TreeNode:
    with open(source_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    assignments = collect_assignments(tree)

    # Preserve source order for the root heuristic
    ordered_names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id not in ordered_names:
                    ordered_names.append(t.id)

    if root_var is None:
        root_var = find_root(assignments, ordered_names)
        print(f"[score_tree] Root variable auto-detected: '{root_var}'\n")

    if root_var not in assignments:
        print(f"Error: '{root_var}' not found in the file's assignments.")
        sys.exit(1)

    root_expr = assignments[root_var]
    root_node = build_tree(root_expr, assignments, visited={root_var}, label=root_var)
    root_node = flatten_associative(root_node)
    return root_node


# ---------------------------------------------------------------------------
# Interactive HTML visualization
# ---------------------------------------------------------------------------

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Score tree -- {title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: ui-monospace, 'Cascadia Code', monospace; font-size: 13px;
          background: #fafafa; color: #1a1a1a; }}
  h1 {{ font-size: 15px; font-weight: 600; padding: 14px 16px 0;
        color: #111; letter-spacing: -0.01em; }}
  .subtitle {{ font-size: 11px; color: #888; padding: 2px 16px 10px; }}

  .controls {{ display: flex; gap: 6px; padding: 8px 16px 10px;
               border-bottom: 1px solid #e8e8e8; flex-wrap: wrap; align-items: center; }}
  button {{ font-size: 11px; padding: 3px 10px; border-radius: 4px;
            border: 1px solid #d0d0d0; background: #fff; color: #333;
            cursor: pointer; transition: background 0.1s; }}
  button:hover {{ background: #f0f0f0; }}
  .sep {{ color: #ccc; font-size: 14px; }}

  .legend {{ display: flex; flex-wrap: wrap; gap: 10px; padding: 8px 16px;
             border-bottom: 1px solid #e8e8e8; }}
  .leg {{ display: flex; align-items: center; gap: 5px; font-size: 11px; color: #666; }}
  .badge {{ font-size: 10px; font-weight: 600; padding: 1px 6px;
            border-radius: 3px; letter-spacing: 0.03em; }}
  .b-seq  {{ background: #dbeafe; color: #1e40af; }}
  .b-par  {{ background: #dcfce7; color: #166534; }}
  .b-orch {{ background: #ffe4e6; color: #9f1239; }}
  .b-pow  {{ background: #fae8ff; color: #7e22ce; }}
  .b-sub  {{ background: #f1f5f9; color: #475569; }}

  .tree {{ padding: 10px 16px 24px; }}
  .row {{ display: flex; align-items: center; gap: 6px; padding: 2px 6px 2px 2px;
          border-radius: 4px; cursor: pointer; transition: background 0.1s;
          width: fit-content; min-width: 0; }}
  .row:hover {{ background: #f0f0f0; }}
  .toggle {{ width: 14px; height: 14px; display: flex; align-items: center;
             justify-content: center; color: #aaa; font-size: 10px; flex-shrink: 0; }}
  .name {{ font-weight: 600; color: #111; }}
  .leaf {{ color: #777; font-weight: 400; }}
  .children {{ margin-left: 14px; padding-left: 10px; border-left: 1px solid #e0e0e0; }}
  .hidden {{ display: none; }}
</style>
</head>
<body>
<h1>{title}</h1>
<div class="subtitle">{source}</div>

<div class="legend">
  <span class="leg"><span class="badge b-seq">*</span> sequence</span>
  <span class="leg"><span class="badge b-par">+</span> parallel layers</span>
  <span class="leg"><span class="badge b-orch">@</span> orchestration</span>
  <span class="leg"><span class="badge b-pow">**</span> repetition</span>
  <span class="leg"><span class="badge b-sub">Sub</span> transposition</span>
</div>

<div class="controls">
  <button onclick="setAll(true)">Expand all</button>
  <button onclick="setAll(false)">Collapse all</button>
  <span class="sep">|</span>
  <button onclick="setDepth(1)">Depth 1</button>
  <button onclick="setDepth(2)">Depth 2</button>
  <button onclick="setDepth(3)">Depth 3</button>
  <button onclick="setDepth(4)">Depth 4</button>
</div>

<div class="tree" id="root"></div>

<script>
const data = {data};

const OP_CLASS = {{ "*": "b-seq", "+": "b-par", "@": "b-orch", "**": "b-pow", "Sub": "b-sub" }};

function badge(op) {{
  const cls = OP_CLASS[op] || "b-sub";
  return `<span class="badge ${{cls}}">${{op}}</span>`;
}}

function buildNode(node, depth) {{
  const div = document.createElement("div");
  div.className = "node";

  const row = document.createElement("div");
  row.className = "row";

  const hasChildren = node.children && node.children.length > 0;

  const toggle = document.createElement("span");
  toggle.className = "toggle";
  toggle.textContent = hasChildren ? "\u25be" : " ";
  row.appendChild(toggle);

  if (node.op) row.innerHTML += badge(node.op) + " ";

  const lbl = document.createElement("span");
  lbl.className = node.op ? (node.label ? "name" : "") : "leaf";
  lbl.textContent = node.label || "";
  row.appendChild(lbl);

  div.appendChild(row);

  if (hasChildren) {{
    const ch = document.createElement("div");
    ch.className = "children";
    node.children.forEach(c => ch.appendChild(buildNode(c, depth + 1)));
    div.appendChild(ch);

    row.addEventListener("click", () => {{
      const hidden = ch.classList.toggle("hidden");
      toggle.textContent = hidden ? "\u25b8" : "\u25be";
    }});
  }}

  return div;
}}

function setAll(open) {{
  document.querySelectorAll(".children").forEach(el => {{
    el.classList.toggle("hidden", !open);
  }});
  document.querySelectorAll(".toggle").forEach(el => {{
    if (el.textContent.trim()) el.textContent = open ? "\u25be" : "\u25b8";
  }});
}}

function setDepth(maxDepth) {{
  function walk(node, depth) {{
    const children = node.querySelector(":scope > .children");
    const toggle   = node.querySelector(":scope > .row > .toggle");
    if (!children) return;
    const hide = depth >= maxDepth;
    children.classList.toggle("hidden", hide);
    if (toggle && toggle.textContent.trim()) toggle.textContent = hide ? "\u25b8" : "\u25be";
    children.querySelectorAll(":scope > .node").forEach(ch => walk(ch, depth + 1));
  }}
  document.querySelectorAll("#root > .node").forEach(n => walk(n, 0));
}}

const root = document.getElementById("root");
root.appendChild(buildNode(data, 0));
</script>
</body>
</html>
"""


def to_html(root_node: TreeNode, source_path: str, root_var: str) -> str:
    """Render the tree as a self-contained interactive HTML page."""
    return HTML_TEMPLATE.format(
        title=root_var,
        source=source_path,
        data=json.dumps(root_node.to_dict(), ensure_ascii=False),
    )


def open_in_browser(html: str) -> None:
    """Write the HTML to a temp file and open it in the default browser."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", encoding="utf-8", delete=False
    ) as f:
        f.write(html)
        path = f.name
    print(f"[score_tree] Opening visualization: {path}")
    webbrowser.open(f"file://{path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args  = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = [a for a in sys.argv[1:] if a.startswith("-")]

    if not args:
        print(__doc__)
        sys.exit(1)

    source_path = args[0]
    root_var    = args[1] if len(args) > 1 else None
    use_html    = "--html" in flags

    root_node   = analyze(source_path, root_var)
    actual_root = root_var or root_node.label or "piece"

    if use_html:
        html = to_html(root_node, source_path, actual_root)
        open_in_browser(html)
    else:
        print(root_node.pprint())


if __name__ == "__main__":
    main()