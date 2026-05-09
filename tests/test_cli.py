from pathlib import Path

from specforge.cli import main


ROOT = Path(__file__).resolve().parents[1]


def test_cli_init_validate_plan_apply_doctor_explain(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["init"]) == 0
    assert Path(".specforge/app.appspec").exists()
    assert main(["validate"]) == 0
    assert main(["plan", "--out", "generated"]) == 0
    assert main(["apply", "--out", "generated"]) == 0
    assert Path("generated/app/main.py").exists()
    assert main(["doctor"]) == 0
    assert main(["explain"]) == 0
    out = capsys.readouterr().out
    assert "model Task" in out


def test_cli_validate_explicit_example(capsys):
    spec = ROOT / "examples/software-spend-approval/.specforge/app.appspec"
    assert main(["validate", str(spec)]) == 0
    assert "Valid:" in capsys.readouterr().out


def test_cli_init_refuses_overwrite(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["init"]) == 0
    assert main(["init"]) == 1
