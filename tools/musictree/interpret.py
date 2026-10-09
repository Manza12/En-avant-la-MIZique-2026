"""Reconstruct musictensors objects from a musictree JSON document."""
from __future__ import annotations

import importlib
import json
import operator
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Operator dispatch
# ---------------------------------------------------------------------------

_OP_MAP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "**": operator.pow,
    "@": operator.matmul,
    "|": operator.or_,
    "neg": operator.neg,
}

# ---------------------------------------------------------------------------
# Core builder
# ---------------------------------------------------------------------------

def _resolve_callable(name: str, ns: Dict[str, Any]) -> Any:
    """Resolve ``'Foo'`` or ``'Foo.bar'`` to a callable using *ns*."""
    parts = name.split(".", 1)
    obj = ns[parts[0]]
    if len(parts) == 2:
        obj = getattr(obj, parts[1])
    return obj


def _eval_expr(expr: dict, ns: Dict[str, Any]) -> Any:
    """Recursively evaluate an expression node in *ns*."""
    if "ref" in expr:
        return ns[expr["ref"]]

    if "lit" in expr:
        return expr["lit"]

    if "op" in expr:
        fn = _OP_MAP[expr["op"]]
        args = [_eval_expr(a, ns) for a in expr["args"]]
        return fn(*args)

    if "call" in expr:
        fn = _resolve_callable(expr["call"], ns)
        args = [_eval_expr(a, ns) for a in expr.get("args", [])]
        kwargs = {k: _eval_expr(v, ns) for k, v in expr.get("kwargs", {}).items()}
        return fn(*args, **kwargs)

    if "set" in expr:
        return {_eval_expr(e, ns) for e in expr["set"]}

    if "list" in expr:
        return [_eval_expr(e, ns) for e in expr["list"]]

    if "tuple" in expr:
        return tuple(_eval_expr(e, ns) for e in expr["tuple"])

    raise ValueError(f"Unknown expression node: {expr!r}")


def build(
    doc: dict,
    *,
    project_root: Optional[str] = None,
) -> Any:
    """Evaluate all definitions in *doc* and return the root object.

    *project_root*, if given, is prepended to ``sys.path`` so that the
    modules listed in ``imports`` can be resolved.
    """
    if project_root is not None:
        proj = str(Path(project_root).resolve())
        if proj not in sys.path:
            sys.path.insert(0, proj)

    # Build namespace from imports
    ns: Dict[str, Any] = {}
    for imp in doc["imports"]:
        mod = importlib.import_module(imp["from"])
        for name in imp["names"]:
            ns[name] = getattr(mod, name)

    # Evaluate definitions in order
    for defn in doc["definitions"]:
        ns[defn["name"]] = _eval_expr(defn["expr"], ns)

    root_name = doc.get("root")
    if root_name is None:
        root_name = doc["definitions"][-1]["name"]
    return ns[root_name]


def build_all(
    doc: dict,
    *,
    project_root: Optional[str] = None,
) -> Dict[str, Any]:
    """Like :func:`build` but returns the full namespace (all definitions)."""
    if project_root is not None:
        proj = str(Path(project_root).resolve())
        if proj not in sys.path:
            sys.path.insert(0, proj)

    ns: Dict[str, Any] = {}
    for imp in doc["imports"]:
        mod = importlib.import_module(imp["from"])
        for name in imp["names"]:
            ns[name] = getattr(mod, name)

    for defn in doc["definitions"]:
        ns[defn["name"]] = _eval_expr(defn["expr"], ns)

    return ns


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Build objects from musictree JSON")
    parser.add_argument("json_file", help="Path to the JSON document")
    parser.add_argument("--project-root", default=".", help="Project root for imports")
    args = parser.parse_args(argv)

    doc = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    root = build(doc, project_root=args.project_root)
    print(f"root ({doc.get('root')}): {root!r}")


if __name__ == "__main__":
    main()