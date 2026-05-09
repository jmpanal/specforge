from pathlib import Path

from specforge.adapters.fastapi_sqlite_basic.adapter import render_files
from specforge.generate import write_generated_project
from specforge.parser import parse_file, parse_text


ROOT = Path(__file__).resolve().parents[1]


def test_generator_writes_expected_files(tmp_path):
    text = (ROOT / "examples/task-manager/.specforge/app.appspec").read_text(encoding="utf-8")
    spec_dir = tmp_path / ".specforge"
    spec_dir.mkdir()
    spec_path = spec_dir / "app.appspec"
    spec_path.write_text(text, encoding="utf-8")
    spec = parse_text(text, spec_path)
    written = write_generated_project(spec, tmp_path / "generated")
    assert tmp_path.joinpath("generated/app/main.py").exists()
    assert tmp_path.joinpath("generated/tests/test_crud.py").exists()
    assert any(path.name == "specmap.json" for path in written)


def test_generator_output_is_deterministic():
    spec = parse_file(ROOT / "examples/task-manager/.specforge/app.appspec")
    assert render_files(spec) == render_files(spec)
