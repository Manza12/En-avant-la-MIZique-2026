"""Verify that a musictree JSON round-trips to the same object as the script."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from .interpret import build


def verify(
    script_path: str,
    json_path: str,
    *,
    project_root: str = ".",
) -> bool:
    """Return ``True`` if ``build(json)`` equals the script's root object."""
    proj = str(Path(project_root).resolve())
    if proj not in sys.path:
        sys.path.insert(0, proj)

    # Execute the script to get the reference object
    source = Path(script_path).resolve()
    code_text = source.read_text(encoding="utf-8")
    ns: Dict[str, Any] = {"__name__": "__musictree_verify__", "__file__": str(source)}
    exec(compile(code_text, str(source), "exec"), ns)  # noqa: S102

    doc = json.loads(Path(json_path).read_text(encoding="utf-8"))
    root_name = doc.get("root", doc["definitions"][-1]["name"])

    ref_obj = ns[root_name]
    built_obj = build(doc, project_root=project_root)

    return ref_obj == built_obj


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Verify musictree JSON round-trip")
    parser.add_argument("script", help="Original Python script")
    parser.add_argument("json_file", help="Exported JSON document")
    parser.add_argument("--project-root", default=".", help="Project root for imports")
    args = parser.parse_args(argv)

    ok = verify(args.script, args.json_file, project_root=args.project_root)
    if ok:
        print("OK: round-trip verified.")
        sys.exit(0)
    else:
        print("FAIL: built object differs from script result.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()