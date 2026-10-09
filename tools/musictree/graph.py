"""Generate dependency graphs and text trees from a musictree JSON document."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Colour palette keyed by type name (Graphviz colour names).
_TYPE_COLOURS: Dict[str, str] = {
    "Texture": "#4a90d9",
    "Rhythm": "#6ab04c",
    "Hit": "#27ae60",
    "Pitch": "#e67e22",
    "Chord": "#e74c3c",
    "Harmony": "#9b59b6",
    "HarmonicTexture": "#2980b9",
    "Instrument": "#1abc9c",
    "Section": "#16a085",
    "Orchestration": "#8e44ad",
    "OrchestredTexture": "#2c3e50",
    "HarmonicOrchestration": "#34495e",
    "ScoreTensor": "#c0392b",
}

_DEFAULT_COLOUR = "#95a5a6"


def _colour_for(type_name: Optional[str]) -> str:
    return _TYPE_COLOURS.get(type_name or "", _DEFAULT_COLOUR)


def _summarise_expr(expr: dict, max_len: int = 48) -> str:
    """One-line summary of an expression tree."""
    if "ref" in expr:
        return expr["ref"]
    if "lit" in expr:
        v = expr["lit"]
        return repr(v) if isinstance(v, str) else str(v)
    if "op" in expr:
        op = expr["op"]
        if op == "neg":
            return f"-{_summarise_expr(expr['args'][0], max_len)}"
        left = _summarise_expr(expr["args"][0], max_len)
        right = _summarise_expr(expr["args"][1], max_len)
        s = f"{left} {op} {right}"
        if len(s) > max_len:
            s = s[:max_len - 1] + "\u2026"
        return s
    if "call" in expr:
        name = expr["call"]
        args_s = ", ".join(_summarise_expr(a, 20) for a in expr.get("args", []))
        kw_s = ", ".join(f"{k}={_summarise_expr(v, 16)}"
                         for k, v in expr.get("kwargs", {}).items())
        parts = [p for p in (args_s, kw_s) if p]
        s = f"{name}({', '.join(parts)})"
        if len(s) > max_len:
            s = s[:max_len - 1] + "\u2026"
        return s
    if "set" in expr:
        inner = ", ".join(_summarise_expr(e, 12) for e in expr["set"])
        return "{" + inner + "}"
    if "list" in expr:
        inner = ", ".join(_summarise_expr(e, 12) for e in expr["list"])
        return "[" + inner + "]"
    if "tuple" in expr:
        inner = ", ".join(_summarise_expr(e, 12) for e in expr["tuple"])
        return "(" + inner + ")"
    return "?"


# ---------------------------------------------------------------------------
# Dependency extraction
# ---------------------------------------------------------------------------

def _collect_refs(expr: dict) -> Set[str]:
    """Return all variable names referenced (transitively) in *expr*."""
    refs: Set[str] = set()
    _walk_refs(expr, refs)
    return refs


def _walk_refs(expr: dict, out: Set[str]) -> None:
    if "ref" in expr:
        out.add(expr["ref"])
        return
    for key in ("args", "set", "list", "tuple"):
        if key in expr:
            for child in expr[key]:
                _walk_refs(child, out)
    if "kwargs" in expr:
        for child in expr["kwargs"].values():
            _walk_refs(child, out)


def _defined_set(doc: dict) -> Set[str]:
    return {d["name"] for d in doc["definitions"]}


def _deps_of(defn: dict, defined: Set[str]) -> Set[str]:
    """Direct variable dependencies (only names that are definitions, not imports)."""
    return _collect_refs(defn["expr"]) & defined


# ---------------------------------------------------------------------------
# Subgraph filtering
# ---------------------------------------------------------------------------

def _reachable_from(name: str, doc: dict) -> Set[str]:
    """All definitions transitively needed by *name*, including itself."""
    by_name = {d["name"]: d for d in doc["definitions"]}
    defined = set(by_name)
    visited: Set[str] = set()
    stack = [name]
    while stack:
        n = stack.pop()
        if n in visited or n not in by_name:
            continue
        visited.add(n)
        for dep in _deps_of(by_name[n], defined):
            stack.append(dep)
    return visited


# ---------------------------------------------------------------------------
# DOT generation - deps mode
# ---------------------------------------------------------------------------

def _escape_dot(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _edge_label(defn: dict, defined: Set[str]) -> Optional[str]:
    """If the expression is exactly ``ref OP ref``, return the operator."""
    expr = defn["expr"]
    if "op" not in expr:
        return None
    if expr["op"] == "neg":
        return None
    args = expr["args"]
    if len(args) == 2 and "ref" in args[0] and "ref" in args[1]:
        if args[0]["ref"] in defined and args[1]["ref"] in defined:
            return expr["op"]
    return None


def generate_dot_deps(doc: dict, root: Optional[str] = None) -> str:
    """Generate a DOT graph in *deps* mode."""
    defined = _defined_set(doc)
    keep = _reachable_from(root, doc) if root else defined

    lines = [
        "digraph musictree {",
        '  rankdir=BT;',
        '  node [shape=box, style=filled, fontname="Helvetica", fontsize=10];',
        '  edge [fontname="Helvetica", fontsize=9];',
    ]

    for defn in doc["definitions"]:
        name = defn["name"]
        if name not in keep:
            continue
        typ = defn.get("type", "")
        colour = _colour_for(typ)
        label = f"{name} : {typ}" if typ else name
        summary = _summarise_expr(defn["expr"], 40)
        label += f"\\n{_escape_dot(summary)}"
        lines.append(f'  "{name}" [label="{_escape_dot(label)}", '
                     f'fillcolor="{colour}", fontcolor="white"];')

    for defn in doc["definitions"]:
        name = defn["name"]
        if name not in keep:
            continue
        deps = _deps_of(defn, defined) & keep
        elabel = _edge_label(defn, defined)
        for dep in sorted(deps):
            edge_attrs = ""
            if elabel and len(deps) == 2:
                edge_attrs = f' [label="{elabel}"]'
            lines.append(f'  "{dep}" -> "{name}"{edge_attrs};')

    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# DOT generation - full mode
# ---------------------------------------------------------------------------

_full_counter = 0


def _full_node_id() -> str:
    global _full_counter
    _full_counter += 1
    return f"anon_{_full_counter}"


def _emit_full(
    expr: dict,
    parent_id: str,
    defined: Set[str],
    keep: Set[str],
    lines: List[str],
    edge_label: str = "",
) -> None:
    """Recursively emit sub-expression ellipse nodes for *full* mode."""
    if "ref" in expr:
        ref = expr["ref"]
        if ref in keep:
            attrs = f' [label="{edge_label}"]' if edge_label else ""
            lines.append(f'  "{ref}" -> "{parent_id}"{attrs};')
        return

    if "lit" in expr:
        return  # literals stay inline

    # Anonymous sub-expression → small ellipse
    nid = _full_node_id()
    sig = ""
    if "op" in expr:
        op = expr["op"]
        sig_parts = expr.get("sig", [])
        typ = expr.get("type", "")
        sig = f"{op}  {' '.join(sig_parts)} -> {typ}" if sig_parts else op
    elif "call" in expr:
        sig = expr["call"]
        typ = expr.get("type", "")
        if typ:
            sig += f" -> {typ}"
    else:
        sig = "?"

    lines.append(f'  "{nid}" [shape=ellipse, label="{_escape_dot(sig)}", '
                 f'style=filled, fillcolor="#ecf0f1", fontsize=8];')
    attrs = f' [label="{edge_label}"]' if edge_label else ""
    lines.append(f'  "{nid}" -> "{parent_id}"{attrs};')

    # Recurse into children
    for key in ("args", "set", "list", "tuple"):
        if key in expr:
            for child in expr[key]:
                _emit_full(child, nid, defined, keep, lines)
    if "kwargs" in expr:
        for k, child in expr["kwargs"].items():
            _emit_full(child, nid, defined, keep, lines, edge_label=k)


def generate_dot_full(doc: dict, root: Optional[str] = None) -> str:
    """Generate a DOT graph in *full* mode."""
    global _full_counter
    _full_counter = 0

    defined = _defined_set(doc)
    keep = _reachable_from(root, doc) if root else defined

    lines = [
        "digraph musictree {",
        '  rankdir=BT;',
        '  node [shape=box, style=filled, fontname="Helvetica", fontsize=10];',
        '  edge [fontname="Helvetica", fontsize=9];',
    ]

    for defn in doc["definitions"]:
        name = defn["name"]
        if name not in keep:
            continue
        typ = defn.get("type", "")
        colour = _colour_for(typ)
        label = f"{name} : {typ}" if typ else name
        lines.append(f'  "{name}" [label="{_escape_dot(label)}", '
                     f'fillcolor="{colour}", fontcolor="white"];')
        _emit_full(defn["expr"], name, defined, keep, lines)

    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Text tree
# ---------------------------------------------------------------------------

def print_tree(
    doc: dict,
    root: Optional[str] = None,
    max_depth: int = 20,
    file: Any = None,
) -> None:
    """Print the dependency tree as indented text."""
    if file is None:
        file = sys.stdout

    by_name = {d["name"]: d for d in doc["definitions"]}
    defined = set(by_name)

    if root is None:
        root = doc.get("root", doc["definitions"][-1]["name"])
    if root not in by_name:
        print(f"Error: {root!r} not found in definitions", file=sys.stderr)
        return

    seen: Set[str] = set()

    def _print(name: str, indent: int, depth: int) -> None:
        defn = by_name[name]
        typ = defn.get("type", "")
        prefix = "  " * indent
        summary = _summarise_expr(defn["expr"], 60)
        print(f"{prefix}{name} : {typ} = {summary}", file=file)
        if name in seen:
            print(f"{prefix}  -> {name} (already shown)", file=file)
            return
        seen.add(name)
        if depth >= max_depth:
            print(f"{prefix}  ... (max depth)", file=file)
            return
        deps = sorted(_deps_of(defn, defined))
        for dep in deps:
            _print(dep, indent + 1, depth + 1)

    _print(root, 0, 0)


# ---------------------------------------------------------------------------
# DOT tree (expanded tree layout, no dependency edges)
# ---------------------------------------------------------------------------

_tree_counter = 0


def _tree_node_id() -> str:
    global _tree_counter
    _tree_counter += 1
    return f"tn_{_tree_counter}"


def generate_dot_tree(
    doc: dict,
    root: Optional[str] = None,
    max_depth: int = 20,
) -> str:
    """Generate a DOT tree that expands definitions recursively.

    Each occurrence of a variable in the tree gets its own node (like the
    text ``tree`` output).  Leaves are the terminal definitions (no further
    deps) or back-references to already-expanded names.  No separate
    dependency edges — the tree structure *is* the dependency.
    """
    global _tree_counter
    _tree_counter = 0

    by_name = {d["name"]: d for d in doc["definitions"]}
    defined = set(by_name)

    if root is None:
        root = doc.get("root", doc["definitions"][-1]["name"])

    lines = [
        "digraph musictree_tree {",
        '  rankdir=TB;',
        '  node [fontname="Helvetica", fontsize=10];',
        '  edge [fontname="Helvetica", fontsize=9, arrowhead=none];',
    ]

    seen: Set[str] = set()

    def _emit(name: str, depth: int) -> str:
        """Emit nodes/edges for *name*, return this node's DOT id."""
        nid = _tree_node_id()
        defn = by_name[name]
        typ = defn.get("type", "")
        summary = _summarise_expr(defn["expr"], 50)
        colour = _colour_for(typ)
        label = f"{name} : {typ}\\n{_escape_dot(summary)}" if typ else f"{name}\\n{_escape_dot(summary)}"

        if name in seen:
            # Back-reference: dashed box, no children
            lines.append(
                f'  "{nid}" [shape=box, style="filled,dashed", '
                f'fillcolor="{colour}", fontcolor="white", '
                f'label="{_escape_dot(name)} (↑)"];'
            )
            return nid

        seen.add(name)

        if depth >= max_depth:
            lines.append(
                f'  "{nid}" [shape=box, style="filled,dashed", '
                f'fillcolor="{colour}", fontcolor="white", '
                f'label="{_escape_dot(name)} …"];'
            )
            return nid

        deps = sorted(_deps_of(defn, defined))
        if not deps:
            # Leaf node
            lines.append(
                f'  "{nid}" [shape=box, style="filled,rounded", '
                f'fillcolor="{colour}", fontcolor="white", '
                f'label="{_escape_dot(label)}"];'
            )
            return nid

        # Interior node
        lines.append(
            f'  "{nid}" [shape=box, style=filled, '
            f'fillcolor="{colour}", fontcolor="white", '
            f'label="{_escape_dot(label)}"];'
        )
        for dep in deps:
            child_id = _emit(dep, depth + 1)
            lines.append(f'  "{nid}" -> "{child_id}";')

        return nid

    _emit(root, 0)
    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Render DOT to file
# ---------------------------------------------------------------------------

def render_dot(
    dot_text: str,
    output_path: str,
) -> str:
    """Write .dot and optionally render to .svg/.png. Returns path written."""
    out = Path(output_path)
    dot_path = out.with_suffix(".dot")
    dot_path.write_text(dot_text, encoding="utf-8")

    fmt = out.suffix.lstrip(".") if out.suffix in (".svg", ".png", ".pdf") else None
    if fmt is None:
        return str(dot_path)

    dot_bin = shutil.which("dot")
    if dot_bin is None:
        print(f"Warning: 'dot' (graphviz) not found in PATH. "
              f"Only .dot file written: {dot_path}", file=sys.stderr)
        return str(dot_path)

    try:
        subprocess.run(
            [dot_bin, f"-T{fmt}", str(dot_path), "-o", str(out)],
            check=True, capture_output=True,
        )
        return str(out)
    except subprocess.CalledProcessError as exc:
        print(f"Warning: graphviz failed: {exc.stderr.decode()}", file=sys.stderr)
        return str(dot_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Generate dependency graph")
    parser.add_argument("json_file", help="Path to the JSON document")
    parser.add_argument("-o", "--output", default=None,
                        help="Output path (.dot, .svg, .png)")
    parser.add_argument("--mode", choices=["deps", "full"], default="deps")
    parser.add_argument("--root", default=None,
                        help="Only show subgraph for this variable")
    args = parser.parse_args(argv)

    doc = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    root = args.root or doc.get("root")

    if args.mode == "full":
        dot = generate_dot_full(doc, root=root)
    else:
        dot = generate_dot_deps(doc, root=root)

    if args.output:
        written = render_dot(dot, args.output)
        print(f"Written: {written}")
    else:
        print(dot)


if __name__ == "__main__":
    main()