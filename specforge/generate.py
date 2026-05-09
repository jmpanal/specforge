from __future__ import annotations

import json
from pathlib import Path

from .ast import AppSpec
from .adapters.fastapi_sqlite_basic.adapter import render_files
from .planner import plan_files


def write_generated_project(spec: AppSpec, out: str | Path = "generated") -> list[Path]:
    out_path = Path(out)
    plan_out = out_path.name if out_path.is_absolute() else out_path
    files = render_files(spec)
    written: list[Path] = []
    for rel_path, content in sorted(files.items()):
        target = out_path / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written.append(target)

    specmap_path = _specmap_path(spec)
    specmap_path.parent.mkdir(parents=True, exist_ok=True)
    specmap = {
        "source": spec.source_label,
        "adapter": "fastapi-sqlite-basic",
        "generated": [
            {"path": item.path, "action": item.action, "source": item.source, "reason": item.reason}
            for item in plan_files(spec, plan_out)
        ],
    }
    specmap_path.write_text(json.dumps(specmap, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written.append(specmap_path)
    return written


def _specmap_path(spec: AppSpec) -> Path:
    if spec.path and spec.path.parent.name == ".specforge":
        return spec.path.parent / "specmap.json"
    return Path(".specforge/specmap.json")
