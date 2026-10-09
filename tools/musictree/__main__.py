"""CLI entry point: python -m tools.musictree <subcommand> ..."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def cmd_export(args: argparse.Namespace) -> None:
    from .export import export_to_file
    doc = export_to_file(
        args.script,
        args.output,
        project_root=args.project_root,
        no_types=args.no_types,
        root_name=args.root,
    )
    n = len(doc["definitions"])
    print(f"Exported {n} definitions to {args.output} (root={doc['root']!r})")


def cmd_graph(args: argparse.Namespace) -> None:
    from .graph import generate_dot_deps, generate_dot_full, render_dot
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


def cmd_tree(args: argparse.Namespace) -> None:
    from .graph import print_tree, generate_dot_tree, render_dot
    doc = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    root = args.root or doc.get("root")
    if args.output:
        dot = generate_dot_tree(doc, root=root, max_depth=args.max_depth)
        written = render_dot(dot, args.output)
        print(f"Written: {written}")
    else:
        print_tree(doc, root=root, max_depth=args.max_depth)


def cmd_structure(args: argparse.Namespace) -> None:
    from .graph import print_structure
    doc = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
    root = args.root or doc.get("root")
    print_structure(doc, root=root, max_depth=args.max_depth)


def cmd_verify(args: argparse.Namespace) -> None:
    from .verify import verify
    ok = verify(args.script, args.json_file, project_root=args.project_root)
    if ok:
        print("OK: round-trip verified.")
    else:
        print("FAIL: built object differs from script result.", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m tools.musictree",
        description="musictree - dependency graph tool for musictensors scripts",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- export --------------------------------------------------------------
    p_export = sub.add_parser("export", help="Export script to JSON")
    p_export.add_argument("script", help="Python script path")
    p_export.add_argument("-o", "--output", required=True, help="Output JSON path")
    p_export.add_argument("--no-types", action="store_true",
                          help="Pure AST mode, skip execution")
    p_export.add_argument("--project-root", default=".",
                          help="Project root for resolving imports (default: .)")
    p_export.add_argument("--root", default=None,
                          help="Override the root variable name")

    # -- graph ---------------------------------------------------------------
    p_graph = sub.add_parser("graph", help="Generate dependency graph")
    p_graph.add_argument("json_file", help="JSON document path")
    p_graph.add_argument("-o", "--output", default=None,
                         help="Output path (.dot, .svg, .png)")
    p_graph.add_argument("--mode", choices=["deps", "full"], default="deps")
    p_graph.add_argument("--root", default=None,
                         help="Only show subgraph for this variable")

    # -- tree ----------------------------------------------------------------
    p_tree = sub.add_parser("tree", help="Print dependency tree as text or render to SVG")
    p_tree.add_argument("json_file", help="JSON document path")
    p_tree.add_argument("-o", "--output", default=None,
                        help="Output path (.dot, .svg, .png); omit for text output")
    p_tree.add_argument("--root", default=None,
                        help="Root variable to expand")
    p_tree.add_argument("--max-depth", type=int, default=20,
                        help="Maximum recursion depth (default: 20)")

    # -- structure -----------------------------------------------------------
    p_struct = sub.add_parser("structure",
                              help="Print basic definitions + HarmonicTexture tree")
    p_struct.add_argument("json_file", help="JSON document path")
    p_struct.add_argument("--root", default=None,
                          help="Root variable to expand")
    p_struct.add_argument("--max-depth", type=int, default=40,
                          help="Maximum recursion depth (default: 40)")

    # -- verify --------------------------------------------------------------
    p_verify = sub.add_parser("verify", help="Verify JSON round-trip")
    p_verify.add_argument("script", help="Original Python script")
    p_verify.add_argument("json_file", help="Exported JSON document")
    p_verify.add_argument("--project-root", default=".",
                          help="Project root for resolving imports (default: .)")

    args = parser.parse_args()
    {
        "export": cmd_export,
        "graph": cmd_graph,
        "tree": cmd_tree,
        "structure": cmd_structure,
        "verify": cmd_verify,
    }[args.command](args)


if __name__ == "__main__":
    main()