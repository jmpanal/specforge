from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from . import __version__
from .demo import demo_output
from .generate import write_generated_project
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

- When changing app behavior, edit `.specforge/app.appspec` first.
- Run `specforge validate`.
- Run `specforge plan`.
- Run `specforge apply`.
- Do not manually edit generated files unless required.
- If custom code is needed, put it in generated custom extension folders.
- Keep generated output deterministic.
- Keep errors specific and actionable.
- Run tests before finalizing changes.
"""

CLAUDE = """# SpecForge Claude Code Guide

- Start behavior changes in `.specforge/app.appspec`.
- Run `specforge validate`, then `specforge plan`, then `specforge apply`.
- Avoid manual edits to generated files unless the spec cannot express the change.
- Put custom logic in generated custom extension folders.
- Keep changes small, deterministic, and covered by tests.
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
    print("Created .specforge app files.")
    print("Next: specforge validate && specforge plan && specforge apply")
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


def cmd_doctor() -> int:
    checks = [
        ("Python >= 3.11", sys.version_info >= (3, 11)),
        ("Package import", True),
        (".specforge exists", Path(".specforge").exists()),
        ("stack.appspec exists", Path(".specforge/stack.appspec").exists()),
        ("generated output exists", Path("generated").exists()),
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
