from __future__ import annotations

from pathlib import Path

from .ast import AppSpec, PlannedFile

GENERATED_FILES = [
    ("README.md", "app, model, workflow blocks", "generated app run instructions"),
    ("pyproject.toml", "stack file", "generated app package metadata"),
    ("app/__init__.py", "stack file", "python package marker"),
    ("app/main.py", "app, model, workflow blocks", "FastAPI application entry point"),
    ("app/database.py", "model blocks", "SQLite schema and connection helpers"),
    ("app/models.py", "model blocks", "model metadata"),
    ("app/schemas.py", "model blocks", "Pydantic schemas"),
    ("app/crud.py", "model blocks", "CRUD persistence functions"),
    ("app/routes.py", "model blocks", "CRUD API routes"),
    ("app/workflows.py", "workflow blocks", "workflow service stubs"),
    ("app/custom/__init__.py", "stack file", "custom extension package marker"),
    ("app/custom/hooks.py", "workflow blocks", "user-owned extension hooks"),
    ("tests/test_app.py", "app block", "FastAPI smoke tests"),
    ("tests/test_crud.py", "model blocks", "CRUD tests"),
    ("tests/test_workflows.py", "workflow blocks", "workflow stub tests"),
]


def plan_files(spec: AppSpec, out: str | Path = "generated") -> list[PlannedFile]:
    base = Path(out).as_posix().rstrip("/")
    planned: list[PlannedFile] = []
    for rel, source, reason in GENERATED_FILES:
        path = f"{base}/{rel}" if base else rel
        action = "update" if Path(path).exists() else "create"
        planned.append(PlannedFile(path=path, action=action, source=source, reason=reason))
    return sorted(planned, key=lambda item: item.path)


def format_plan(planned: list[PlannedFile]) -> str:
    lines: list[str] = []
    for item in planned:
        lines.append(f"{item.action.upper()} {item.path}")
        lines.append(f"Reason: {item.reason}")
        lines.append(f"Source: {item.source}")
    return "\n".join(lines)
