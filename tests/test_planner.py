from pathlib import Path

from specforge.parser import parse_file
from specforge.planner import plan_files


ROOT = Path(__file__).resolve().parents[1]


def test_planner_produces_expected_file_list():
    spec = parse_file(ROOT / "examples/task-manager/.specforge/app.appspec")
    paths = [item.path for item in plan_files(spec, "generated/task-manager")]
    assert "generated/task-manager/app/main.py" in paths
    assert "generated/task-manager/tests/test_crud.py" in paths


def test_planner_output_is_deterministic():
    spec = parse_file(ROOT / "examples/task-manager/.specforge/app.appspec")
    assert plan_files(spec, "generated/task-manager") == plan_files(spec, "generated/task-manager")
