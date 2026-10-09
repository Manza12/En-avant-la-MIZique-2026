"""Export a musictensors script to a JSON dependency-graph document."""
from __future__ import annotations

import ast
import copy
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# ---------------------------------------------------------------------------
# AST operator maps
# ---------------------------------------------------------------------------

_BINOP_MAP = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.Pow: "**",
    ast.MatMult: "@",
    ast.BitOr: "|",
}

_UNARYOP_MAP = {
    ast.USub: "neg",
}

# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class ExportError(Exception):
    """Raised when the script contains unsupported constructs."""


def _fail(source: str, lineno: int, msg: str) -> None:
    raise ExportError(f"{source}:{lineno}: {msg}")


# ---------------------------------------------------------------------------
# AST -> expr-node  (without types by default)
# ---------------------------------------------------------------------------

def _expr_node(
    node: ast.expr,
    source: str,
    defined: Set[str],
    imported_names: Set[str],
    ns: Optional[Dict[str, Any]] = None,
) -> dict:
    """Convert an AST expression into a JSON-serialisable expression node.

    If *ns* is not ``None`` the node is also evaluated at runtime so that
    ``type`` (and ``sig`` for operators) can be filled in.
    """

    def _typeof(ast_node: ast.expr) -> Optional[str]:
        if ns is None:
            return None
        try:
            wrapper = ast.Expression(body=copy.deepcopy(ast_node))
            ast.fix_missing_locations(wrapper)
            val = eval(compile(wrapper, source, "eval"), ns)  # noqa: S307
            return type(val).__name__
        except Exception:
            return None

    # --- Constant -----------------------------------------------------------
    if isinstance(node, ast.Constant):
        v = node.value
        if isinstance(v, (str, int, float, bool)) or v is None:
            return {"lit": v}
        _fail(source, node.lineno, f"Unsupported constant type: {type(v).__name__}")

    # --- Name (reference) ---------------------------------------------------
    if isinstance(node, ast.Name):
        name = node.id
        if name in defined or name in imported_names:
            return {"ref": name}
        _fail(source, node.lineno, f"Undefined name: {name!r}")

    # --- Binary operator ----------------------------------------------------
    if isinstance(node, ast.BinOp):
        op_cls = type(node.op)
        if op_cls not in _BINOP_MAP:
            _fail(source, node.lineno, f"Unsupported binary operator: {op_cls.__name__}")
        left = _expr_node(node.left, source, defined, imported_names, ns)
        right = _expr_node(node.right, source, defined, imported_names, ns)
        result: dict = {"op": _BINOP_MAP[op_cls], "args": [left, right]}
        if ns is not None:
            sig_l = left.get("type") or _typeof(node.left)
            sig_r = right.get("type") or _typeof(node.right)
            if sig_l and sig_r:
                result["sig"] = [sig_l, sig_r]
            t = _typeof(node)
            if t:
                result["type"] = t
        return result

    # --- Unary operator -----------------------------------------------------
    if isinstance(node, ast.UnaryOp):
        op_cls = type(node.op)
        if op_cls not in _UNARYOP_MAP:
            _fail(source, node.lineno, f"Unsupported unary operator: {op_cls.__name__}")
        operand = _expr_node(node.operand, source, defined, imported_names, ns)
        result = {"op": _UNARYOP_MAP[op_cls], "args": [operand]}
        if ns is not None:
            sig = operand.get("type") or _typeof(node.operand)
            if sig:
                result["sig"] = [sig]
            t = _typeof(node)
            if t:
                result["type"] = t
        return result

    # --- Call ---------------------------------------------------------------
    if isinstance(node, ast.Call):
        # Determine call name
        if isinstance(node.func, ast.Name):
            call_name = node.func.id
        elif (isinstance(node.func, ast.Attribute)
              and isinstance(node.func.value, ast.Name)):
            call_name = f"{node.func.value.id}.{node.func.attr}"
        else:
            _fail(source, node.lineno, "Unsupported call target (only Name and Name.attr)")

        # Positional args
        args: List[dict] = []
        for arg in node.args:
            if isinstance(arg, ast.Starred):
                _fail(source, node.lineno, "Star expressions (*args) not supported")
            args.append(_expr_node(arg, source, defined, imported_names, ns))

        # Keyword args
        kwargs: Dict[str, dict] = {}
        for kw in node.keywords:
            if kw.arg is None:
                _fail(source, node.lineno, "**kwargs not supported")
            kwargs[kw.arg] = _expr_node(kw.value, source, defined, imported_names, ns)

        result = {"call": call_name, "args": args, "kwargs": kwargs}
        if ns is not None:
            t = _typeof(node)
            if t:
                result["type"] = t
        return result

    # --- Containers ---------------------------------------------------------
    if isinstance(node, ast.Set):
        elts = [_expr_node(e, source, defined, imported_names, ns) for e in node.elts]
        return {"set": elts}

    if isinstance(node, ast.List):
        elts = [_expr_node(e, source, defined, imported_names, ns) for e in node.elts]
        return {"list": elts}

    if isinstance(node, ast.Tuple):
        elts = [_expr_node(e, source, defined, imported_names, ns) for e in node.elts]
        return {"tuple": elts}

    # --- Unsupported constructs (clear errors) ------------------------------
    unsupported = {
        ast.JoinedStr: "f-strings",
        ast.ListComp: "list comprehensions",
        ast.SetComp: "set comprehensions",
        ast.DictComp: "dict comprehensions",
        ast.GeneratorExp: "generator expressions",
        ast.Lambda: "lambda expressions",
        ast.IfExp: "conditional expressions",
        ast.Dict: "dict literals",
        ast.Subscript: "subscript expressions",
        ast.Starred: "star expressions",
    }
    for cls, label in unsupported.items():
        if isinstance(node, cls):
            _fail(source, node.lineno, f"{label} not supported")

    _fail(source, getattr(node, "lineno", 0),
          f"Unsupported expression node: {type(node).__name__}")


# ---------------------------------------------------------------------------
# Collect imports from the AST
# ---------------------------------------------------------------------------

def _collect_imports(tree: ast.Module) -> List[dict]:
    """Return the ``imports`` section for the JSON document."""
    imports: List[dict] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names = [alias.name for alias in node.names]
            imports.append({"from": node.module, "names": names})
    return imports


def _imported_name_set(imports: List[dict]) -> Set[str]:
    """Flat set of every name brought into scope by the imports."""
    result: Set[str] = set()
    for imp in imports:
        result.update(imp["names"])
    return result


# ---------------------------------------------------------------------------
# Main export logic
# ---------------------------------------------------------------------------

def export(
    script_path: str,
    *,
    project_root: str = ".",
    no_types: bool = False,
    root_name: Optional[str] = None,
) -> dict:
    """Parse and (optionally) execute *script_path*, returning a JSON-ready dict."""
    source = Path(script_path).resolve()
    code_text = source.read_text(encoding="utf-8")
    tree = ast.parse(code_text, filename=str(source))

    imports = _collect_imports(tree)
    imported_names = _imported_name_set(imports)

    # --- optionally execute the script to learn runtime types ---------------
    ns: Optional[Dict[str, Any]] = None
    if not no_types:
        proj = Path(project_root).resolve()
        if str(proj) not in sys.path:
            sys.path.insert(0, str(proj))
        ns = {"__name__": "__musictree_export__", "__file__": str(source)}
        exec(compile(code_text, str(source), "exec"), ns)  # noqa: S102

    # --- walk top-level statements ------------------------------------------
    defined: Set[str] = set()
    definitions: List[dict] = []
    last_name: Optional[str] = None

    for node in ast.iter_child_nodes(tree):
        # Skip imports (already collected) and expression-statements
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Expr)):
            continue

        # Unsupported assignment forms
        if isinstance(node, ast.AugAssign):
            _fail(str(source), node.lineno, "Augmented assignment (+=, etc.) not supported")
        if isinstance(node, ast.AnnAssign):
            _fail(str(source), node.lineno, "Annotated assignment not supported")

        # We only care about simple assignments
        if not isinstance(node, ast.Assign):
            # Other statements (if, for, with, function/class defs, …) are ignored
            continue

        # Must be a single Name target
        if len(node.targets) != 1:
            _fail(str(source), node.lineno, "Multiple assignment targets not supported")
        target = node.targets[0]
        if isinstance(target, (ast.Tuple, ast.List)):
            _fail(str(source), node.lineno, "Tuple/list unpacking not supported")
        if not isinstance(target, ast.Name):
            _fail(str(source), node.lineno,
                  f"Unsupported assignment target: {type(target).__name__}")

        name = target.id
        if name in defined:
            _fail(str(source), node.lineno,
                  f"Reassignment of variable {name!r} not allowed (single-assignment only)")

        expr_tree = _expr_node(node.value, str(source), defined, imported_names, ns)

        defn: dict = {"name": name, "line": node.lineno, "expr": expr_tree}
        if ns is not None and name in ns:
            defn["type"] = type(ns[name]).__name__

        definitions.append(defn)
        defined.add(name)
        last_name = name

    if not definitions:
        raise ExportError("No definitions found in script.")

    if root_name is not None:
        if root_name not in defined:
            raise ExportError(f"--root name {root_name!r} not found in definitions")
    else:
        root_name = last_name

    return {
        "format_version": 1,
        "source": Path(script_path).name,
        "imports": imports,
        "definitions": definitions,
        "root": root_name,
    }


def export_to_file(
    script_path: str,
    output_path: str,
    **kwargs: Any,
) -> dict:
    """Export and write the JSON to *output_path*. Returns the document."""
    doc = export(script_path, **kwargs)
    Path(output_path).write_text(
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return doc