from __future__ import annotations

from pathlib import Path

from .parser import parse_file
from .planner import format_plan, plan_files

MESSAGE = "Agent edited 1 spec file instead of 12 source files."
DEMO_SPEC = Path("examples/software-spend-approval/.specforge/app.appspec")

NORMAL_FILES = [
    "database model",
    "schema",
    "route",
    "service",
    "frontend table",
    "frontend form",
    "permission check",
    "test fixtures",
    "test assertions",
    "docs",
    "API client",
    "status enum usage",
]

WORKFLOW_BLOCK = """workflow ApproveSoftwareRequest
  when Manager approves SoftwareRequest
  require SoftwareRequest.status = submitted
  if SoftwareRequest.monthly_cost > 500
    set SoftwareRequest.status pending_finance
    notify Finance
  else
    set SoftwareRequest.status approved"""


def demo_output() -> str:
    spec = parse_file(DEMO_SPEC)
    lines = [
        "SpecForge demo: software spend approval",
        MESSAGE,
        "",
        "Before SpecForge:",
        "A coding agent adds finance approval by editing many scattered files:",
    ]
    lines.extend(f"- {item}" for item in NORMAL_FILES)
    lines.extend([
        "",
        "After SpecForge:",
        "The agent edits one spec block:",
        "",
        WORKFLOW_BLOCK,
        "",
        "Generated file plan:",
        format_plan(plan_files(spec, "generated/software-spend-approval")),
    ])
    return "\n".join(lines)
