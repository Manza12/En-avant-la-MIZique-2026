# musictree

Dependency-graph tool for scripts written with the `musictensors` library.

Given a Python script that builds a musical piece through a sequence of
single-assignment definitions, `musictree` can:

1. **Export** the script to a JSON document describing every variable as an
   expression tree, with runtime type annotations and a dependency DAG.
2. **Interpret** the JSON back into live `musictensors` objects.
3. **Verify** that the round-trip (script → JSON → objects) produces the same
   result as running the script directly.
4. **Graph** the dependencies as a Graphviz DOT file (and optionally render to
   SVG/PNG), or print the dependency tree as indented text.

## Quickstart

Run from the **project root** (the directory containing `musictensors/`):

```bash
# Export a script to JSON
python -m tools.musictree export scripts/pathetique_1.py -o pathetique.json

# Without runtime types (pure AST, no execution)
python -m tools.musictree export scripts/pathetique_1.py -o pathetique.json --no-types

# Generate a dependency graph
python -m tools.musictree graph pathetique.json -o pathetique.svg
python -m tools.musictree graph pathetique.json -o pathetique.svg --mode full

# Show only the subgraph for a specific variable
python -m tools.musictree graph pathetique.json -o sub.svg --root m11_12

# Print the dependency tree as text
python -m tools.musictree tree pathetique.json
python -m tools.musictree tree pathetique.json --root m11_12 --max-depth 5

# Verify round-trip correctness
python -m tools.musictree verify scripts/pathetique_1.py pathetique.json
```

## JSON format

```json
{
  "format_version": 1,
  "source": "my_script.py",
  "imports": [
    {"from": "musictensors.model", "names": ["Hit", "Rhythm", "Texture"]}
  ],
  "definitions": [
    {
      "name": "t_quarter",
      "type": "Texture",
      "line": 12,
      "expr": {
        "call": "Texture", "type": "Texture",
        "args": [{"call": "Rhythm", "type": "Rhythm", "args": [
          {"call": "Hit", "type": "Hit", "args": [{"lit": "0"}, {"lit": "1/4"}]}
        ], "kwargs": {}}],
        "kwargs": {}
      }
    }
  ],
  "root": "piece"
}
```

### Expression node types

| Key | Example | Meaning |
|-----|---------|---------|
| `ref` | `{"ref": "t_quarter"}` | Reference to a previously defined variable |
| `lit` | `{"lit": "1/4"}` | Literal value (str, int, float, bool, None) |
| `call` | `{"call": "Hit", "args": [...], "kwargs": {...}}` | Constructor or classmethod call |
| `op` | `{"op": "+", "args": [left, right]}` | Binary operator (`+ - * ** @ \|`) |
| `op` (unary) | `{"op": "neg", "args": [operand]}` | Unary negation |
| `set` | `{"set": [...]}` | Set literal |
| `list` | `{"list": [...]}` | List literal |
| `tuple` | `{"tuple": [...]}` | Tuple literal |

`type` and `sig` fields are informational (added when the script is executed).

## Limitations

- Only supports scripts with **simple single-assignment** at the top level
  (`name = expr`). No reassignment, augmented assignment, tuple unpacking,
  control flow, comprehensions, lambdas, or f-strings.
- Attribute access as call target is limited to `Name.attr` (e.g.
  `Harmony.from_chord(...)`). Chained attribute access is not supported.
- The `--no-types` mode skips script execution, so `type` and `sig` fields
  are omitted from the JSON.
- Graphviz `dot` binary must be in PATH for SVG/PNG rendering; otherwise only
  `.dot` files are produced.

## Tests

```bash
pytest tools/musictree/tests/ -v
```
