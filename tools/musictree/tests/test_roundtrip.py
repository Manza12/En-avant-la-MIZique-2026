"""Tests for musictree: export -> interpret round-trip and error handling."""
from __future__ import annotations

import json
import textwrap
import tempfile
from pathlib import Path

import pytest

# We run tests from the project root so musictensors is importable.
PROJECT_ROOT = str(Path(__file__).resolve().parents[3])

SAMPLE_SCRIPT = textwrap.dedent("""\
    from musictensors.model import (
        Hit, Rhythm, Texture, Pitch, Chord, Harmony,
        Instrument, Section, Orchestration, HarmonicTexture, ScoreTensor,
    )
    from musictensors import frac

    # --- Time ---
    h1 = Hit('0', '1/4')
    r1 = Rhythm(h1)
    t_quarter = Texture(r1)
    t_double = t_quarter ** 2

    # --- Frequency ---
    ton = Chord({0})
    dom = Chord({7})
    h_ton = Harmony.from_chord(ton)
    h_pair = Harmony(ton | dom)

    # --- Combine ---
    ht = t_double @ h_pair
    transposed = ht - 12

    # --- Orchestration ---
    piano = Instrument('Piano')
    sec = Section(piano)

    # --- Negation ---
    p = Pitch(60)
    p_neg = Pitch(-60)

    # --- kwargs ---
    c_vel = Chord({0, 7}, velocity=64)

    piece = transposed
""")


@pytest.fixture
def sample_script_path(tmp_path: Path) -> Path:
    p = tmp_path / "sample.py"
    p.write_text(SAMPLE_SCRIPT, encoding="utf-8")
    return p


@pytest.fixture
def sample_json_path(sample_script_path: Path, tmp_path: Path) -> Path:
    from tools.musictree.export import export_to_file
    out = tmp_path / "sample.json"
    export_to_file(
        str(sample_script_path),
        str(out),
        project_root=PROJECT_ROOT,
    )
    return out


# ---------------------------------------------------------------------------
# Round-trip tests
# ---------------------------------------------------------------------------

class TestExport:
    def test_export_produces_valid_json(self, sample_json_path: Path):
        doc = json.loads(sample_json_path.read_text(encoding="utf-8"))
        assert doc["format_version"] == 1
        assert "definitions" in doc
        assert "imports" in doc
        assert doc["root"] == "piece"

    def test_definitions_have_types(self, sample_json_path: Path):
        doc = json.loads(sample_json_path.read_text(encoding="utf-8"))
        by_name = {d["name"]: d for d in doc["definitions"]}
        assert by_name["h1"]["type"] == "Hit"
        assert by_name["r1"]["type"] == "Rhythm"
        assert by_name["t_quarter"]["type"] == "Texture"
        assert by_name["t_double"]["type"] == "Texture"
        assert by_name["h_ton"]["type"] == "Harmony"
        assert by_name["ht"]["type"] == "HarmonicTexture"

    def test_expr_structures(self, sample_json_path: Path):
        doc = json.loads(sample_json_path.read_text(encoding="utf-8"))
        by_name = {d["name"]: d for d in doc["definitions"]}

        # h1 = Hit('0', '1/4') -> call
        assert by_name["h1"]["expr"]["call"] == "Hit"
        assert by_name["h1"]["expr"]["args"] == [{"lit": "0"}, {"lit": "1/4"}]

        # t_double = t_quarter ** 2 -> op
        expr = by_name["t_double"]["expr"]
        assert expr["op"] == "**"
        assert expr["args"][0] == {"ref": "t_quarter"}
        assert expr["args"][1] == {"lit": 2}

        # ton = Chord({0}) -> call with set arg
        expr = by_name["ton"]["expr"]
        assert expr["call"] == "Chord"
        assert expr["args"] == [{"set": [{"lit": 0}]}]

        # h_ton = Harmony.from_chord(ton) -> classmethod call
        expr = by_name["h_ton"]["expr"]
        assert expr["call"] == "Harmony.from_chord"
        assert expr["args"] == [{"ref": "ton"}]

        # h_pair = Harmony(ton | dom) -> call with binop arg
        expr = by_name["h_pair"]["expr"]
        assert expr["call"] == "Harmony"
        inner = expr["args"][0]
        assert inner["op"] == "|"
        assert inner["args"] == [{"ref": "ton"}, {"ref": "dom"}]

        # ht = t_double @ h_pair -> matmul
        expr = by_name["ht"]["expr"]
        assert expr["op"] == "@"

        # c_vel = Chord({0, 7}, velocity=64) -> kwargs
        expr = by_name["c_vel"]["expr"]
        assert expr["kwargs"]["velocity"] == {"lit": 64}

    def test_no_types_mode(self, sample_script_path: Path, tmp_path: Path):
        from tools.musictree.export import export_to_file
        out = tmp_path / "notypes.json"
        export_to_file(
            str(sample_script_path), str(out),
            project_root=PROJECT_ROOT, no_types=True,
        )
        doc = json.loads(out.read_text(encoding="utf-8"))
        for defn in doc["definitions"]:
            assert "type" not in defn


class TestInterpret:
    def test_build_returns_root(self, sample_json_path: Path):
        from tools.musictree.interpret import build
        doc = json.loads(sample_json_path.read_text(encoding="utf-8"))
        root = build(doc, project_root=PROJECT_ROOT)
        assert type(root).__name__ == "HarmonicTexture"

    def test_build_all_has_all_names(self, sample_json_path: Path):
        from tools.musictree.interpret import build_all
        doc = json.loads(sample_json_path.read_text(encoding="utf-8"))
        ns = build_all(doc, project_root=PROJECT_ROOT)
        expected = {d["name"] for d in doc["definitions"]}
        assert expected.issubset(set(ns.keys()))


class TestVerify:
    def test_roundtrip_matches(self, sample_script_path: Path, sample_json_path: Path):
        from tools.musictree.verify import verify
        assert verify(
            str(sample_script_path),
            str(sample_json_path),
            project_root=PROJECT_ROOT,
        )


class TestGraph:
    def test_deps_dot_output(self, sample_json_path: Path):
        from tools.musictree.graph import generate_dot_deps
        doc = json.loads(sample_json_path.read_text(encoding="utf-8"))
        dot = generate_dot_deps(doc)
        assert "digraph" in dot
        assert "t_quarter" in dot
        assert "piece" in dot

    def test_full_dot_output(self, sample_json_path: Path):
        from tools.musictree.graph import generate_dot_full
        doc = json.loads(sample_json_path.read_text(encoding="utf-8"))
        dot = generate_dot_full(doc)
        assert "digraph" in dot
        assert "ellipse" in dot

    def test_tree_output(self, sample_json_path: Path, capsys):
        from tools.musictree.graph import print_tree
        doc = json.loads(sample_json_path.read_text(encoding="utf-8"))
        print_tree(doc, root="t_double")
        captured = capsys.readouterr()
        assert "t_double" in captured.out
        assert "t_quarter" in captured.out

    def test_root_filter(self, sample_json_path: Path):
        from tools.musictree.graph import generate_dot_deps
        doc = json.loads(sample_json_path.read_text(encoding="utf-8"))
        dot = generate_dot_deps(doc, root="t_double")
        # Should include t_quarter (dependency) but not ht (unrelated)
        assert "t_quarter" in dot
        assert "ht" not in dot


# ---------------------------------------------------------------------------
# Error handling tests
# ---------------------------------------------------------------------------

class TestErrors:
    def _write_and_export(self, tmp_path: Path, code: str):
        from tools.musictree.export import export
        p = tmp_path / "bad.py"
        p.write_text(code, encoding="utf-8")
        return export(str(p), project_root=PROJECT_ROOT, no_types=True)

    def test_reassignment_error(self, tmp_path: Path):
        from tools.musictree.export import ExportError
        with pytest.raises(ExportError, match="Reassignment"):
            self._write_and_export(tmp_path, "x = 1\nx = 2\n")

    def test_augassign_error(self, tmp_path: Path):
        from tools.musictree.export import ExportError
        with pytest.raises(ExportError, match="Augmented"):
            self._write_and_export(tmp_path, "x = 1\nx += 2\n")

    def test_tuple_unpack_error(self, tmp_path: Path):
        from tools.musictree.export import ExportError
        with pytest.raises(ExportError, match="unpack"):
            self._write_and_export(tmp_path, "a, b = 1, 2\n")

    def test_fstring_error(self, tmp_path: Path):
        from tools.musictree.export import ExportError
        with pytest.raises(ExportError, match="f-string"):
            self._write_and_export(tmp_path, "x = 1\ny = f'{x}'\n")

    def test_lambda_error(self, tmp_path: Path):
        from tools.musictree.export import ExportError
        with pytest.raises(ExportError, match="lambda"):
            self._write_and_export(tmp_path, "f = lambda x: x\n")

    def test_listcomp_error(self, tmp_path: Path):
        from tools.musictree.export import ExportError
        with pytest.raises(ExportError, match="comprehension"):
            self._write_and_export(tmp_path, "xs = [x for x in range(3)]\n")
