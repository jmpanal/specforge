from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from . import __version__
from .demo import demo_output
from .generate import write_generated_project
from .guardrails import check_repo, format_check, format_inspection, inspect_repo, write_proposal
from .parser import parse_file
from .planner import format_plan, plan_files
from .privacy import scan
from .validate import validate_spec


DEFAULT_APP = """app TaskManager

role User
role Admin

model Task
  title text required
  description text optional
  status enum todo doing done
  owner text required
  created_at datetime

screen TaskList
  table Task
  filter status
  action create
  action edit
  allowed User

workflow CompleteTask
  when User completes Task
  require Task.status != done
  set Task.status done

policy TaskAccess
  allow User read Task
  allow User create Task
  allow Admin manage Task

job DailyTaskSummary
  every day
  notify Admin
"""

DEFAULT_STACK = """stack fastapi-sqlite-basic
"""

AGENTS = """# SpecForge Agent Guide

- Read `.specforge/change.md`.
- Run `specforge inspect`.
- Run `specforge propose`.
- Implement the checklist in `.specforge/plan.md`.
- Run `specforge check` before finalizing.
- Keep changes small, deterministic, and covered by tests.
"""

CLAUDE = """# SpecForge Claude Code Guide

- Read `.specforge/change.md`.
- Run `specforge inspect`.
- Run `specforge propose`.
- Implement the checklist in `.specforge/plan.md`.
- Run `specforge check` before finalizing.
- Keep changes small, deterministic, and covered by tests.
"""

DEFAULT_CHANGE = """Describe the change you want in plain English.

Example:
I want users to upload a photo. The app should analyze the photo and return a short sentence listing the objects in it, such as sofa, table, and TV.
"""

DEFAULT_PLAN = """# SpecForge Change Plan

Run `specforge propose` after writing `.specforge/change.md`.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="specforge")
    parser.add_argument("--version", action="version", version=f"specforge {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--force", action="store_true")

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("spec_path", nargs="?", default=".specforge/app.appspec")

    p_plan = sub.add_parser("plan")
    p_plan.add_argument("spec_path", nargs="?", default=".specforge/app.appspec")
    p_plan.add_argument("--out", default="generated")

    p_apply = sub.add_parser("apply")
    p_apply.add_argument("spec_path", nargs="?", default=".specforge/app.appspec")
    p_apply.add_argument("--out", default="generated")

    sub.add_parser("inspect")

    p_propose = sub.add_parser("propose")
    p_propose.add_argument("--change", default=".specforge/change.md")
    p_propose.add_argument("--plan", default=".specforge/plan.md")

    sub.add_parser("check")
    sub.add_parser("doctor")
    sub.add_parser("explain")
    sub.add_parser("demo")
    sub.add_parser("privacy-scan")

    args = parser.parse_args(argv)
    if args.command == "init":
        return cmd_init(args.force)
    if args.command == "validate":
        return cmd_validate(args.spec_path)
    if args.command == "plan":
        return cmd_plan(args.spec_path, args.out)
    if args.command == "apply":
        return cmd_apply(args.spec_path, args.out)
    if args.command == "inspect":
        return cmd_inspect()
    if args.command == "propose":
        return cmd_propose(args.change, args.plan)
    if args.command == "check":
        return cmd_check()
    if args.command == "doctor":
        return cmd_doctor()
    if args.command == "explain":
        return cmd_explain()
    if args.command == "demo":
        print(demo_output())
        return 0
    if args.command == "privacy-scan":
        return cmd_privacy_scan()
    return 2


def cmd_init(force: bool = False) -> int:
    files = {
        ".specforge/app.appspec": DEFAULT_APP,
        ".specforge/stack.appspec": DEFAULT_STACK,
        ".specforge/specmap.json": "{}\n",
        ".specforge/change.md": DEFAULT_CHANGE,
        ".specforge/plan.md": DEFAULT_PLAN,
        "AGENTS.md": AGENTS,
        "CLAUDE.md": CLAUDE,
    }
    existing = [path for path in files if Path(path).exists()]
    if existing and not force:
        print("Refusing to overwrite existing files:")
        for path in existing:
            print(f"- {path}")
        print("Use --force to overwrite.")
        return 1
    for path, content in files.items():
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    print("Created .specforge files.")
    print("Next: edit .specforge/change.md, then run specforge inspect && specforge propose")
    return 0


def cmd_validate(spec_path: str) -> int:
    spec = parse_file(spec_path)
    errors = validate_spec(spec)
    if errors:
        for error in errors:
            print(error.format())
        return 1
    print(f"Valid: {spec_path}")
    return 0


def cmd_plan(spec_path: str, out: str) -> int:
    spec = parse_file(spec_path)
    errors = validate_spec(spec)
    if errors:
        for error in errors:
            print(error.format())
        return 1
    print(format_plan(plan_files(spec, out)))
    return 0


def cmd_apply(spec_path: str, out: str) -> int:
    spec = parse_file(spec_path)
    errors = validate_spec(spec)
    if errors:
        for error in errors:
            print(error.format())
        return 1
    written = write_generated_project(spec, out)
    print("Wrote generated files:")
    for path in written:
        print(f"- {path.as_posix()}")
    return 0


def cmd_inspect() -> int:
    print(format_inspection(inspect_repo(".")))
    return 0


def cmd_propose(change: str, plan: str) -> int:
    try:
        output = write_proposal(".", change, plan)
    except FileNotFoundError:
        print(f"Missing change request: {change}")
        print("Create it with plain English describing what you want Codex to build.")
        return 1
    print(output)
    print(f"Wrote: {plan}")
    return 0


def cmd_check() -> int:
    result = check_repo(".")
    print(format_check(result))
    serious = [warning for warning in result.warnings if not warning.startswith("No obvious") and not warning.startswith("No changed")]
    return 1 if serious else 0


def cmd_doctor() -> int:
    checks = [
        ("Python >= 3.11", sys.version_info >= (3, 11)),
        ("Package import", True),
        (".specforge exists", Path(".specforge").exists()),
        ("change.md exists", Path(".specforge/change.md").exists()),
        ("plan.md exists", Path(".specforge/plan.md").exists()),
        ("git repo exists", Path(".git").exists()),
    ]
    exit_code = 0
    for name, ok in checks:
        print(f"{'OK' if ok else 'WARN'} {name}")
        if not ok and name in {"Python >= 3.11", "Package import"}:
            exit_code = 1
    if shutil.which("python") is None:
        print("WARN python executable not found on PATH")
    return exit_code


def cmd_explain() -> int:
    lines = [
        "model Task -> model metadata, schema, CRUD routes, CRUD tests",
        "screen TaskList -> route metadata in v0",
        "workflow CompleteTask -> service stub and test stub",
        "policy TaskAccess -> validation metadata in v0",
        "job DailyTaskSummary -> validation metadata in v0",
    ]
    print("\n".join(lines))
    return 0


def cmd_privacy_scan() -> int:
    matches = scan(".")
    if not matches:
        print("No suspicious private artifacts found.")
        return 0
    print("Suspicious matches:")
    for path, line_no, line in matches:
        print(f"{path.as_posix()}:{line_no}: {line}")
    return 1
