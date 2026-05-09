from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


CODE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".swift", ".kt", ".java"}
TEST_MARKERS = ("test", "spec", "__tests__")
DOC_MARKERS = ("readme", "docs/", ".md")
API_MARKERS = ("api", "route", "routes", "controller", "endpoint", "schema", "schemas", "main.py")
UPLOAD_WORDS = ("upload", "photo", "image", "file")
VALIDATION_WORDS = ("validate", "validation", "size", "mime", "content_type", "content-type", "extension", "allowed")
ENV_WORDS = ("os.environ", "getenv", "process.env", "api" + "_key", "sec" + "ret", "to" + "ken")


@dataclass(frozen=True)
class RepoInspection:
    root: Path
    app_type: str
    package_files: tuple[str, ...]
    source_folders: tuple[str, ...]
    test_commands: tuple[str, ...]
    framework_clues: tuple[str, ...]
    api_folders: tuple[str, ...]
    ui_folders: tuple[str, ...]
    warnings: tuple[str, ...]


@dataclass(frozen=True)
class CheckResult:
    changed_files: tuple[str, ...]
    warnings: tuple[str, ...]


def inspect_repo(root: str | Path = ".") -> RepoInspection:
    root_path = Path(root)
    package_files = tuple(_existing(root_path, ["pyproject.toml", "package.json", "requirements.txt", "Pipfile", "poetry.lock", "pnpm-lock.yaml", "package-lock.json", "yarn.lock", "pubspec.yaml"]))
    source_folders = tuple(_dirs(root_path, ["src", "app", "backend", "frontend", "mobile", "server", "client", "lib", "pages", "components", "tests"]))
    framework_clues = tuple(_framework_clues(root_path))
    api_folders = tuple(path for path in source_folders if path in {"api", "app", "backend", "server"} or _contains_name(root_path / path, API_MARKERS))
    ui_folders = tuple(path for path in source_folders if path in {"frontend", "mobile", "client", "pages", "components"} or _contains_name(root_path / path, ("screen", "view", "component", "page")))
    test_commands = tuple(_test_commands(package_files, framework_clues))
    warnings = tuple(_inspection_warnings(package_files, source_folders, test_commands))
    return RepoInspection(
        root=root_path,
        app_type=_app_type(framework_clues, package_files),
        package_files=package_files,
        source_folders=source_folders,
        test_commands=test_commands,
        framework_clues=framework_clues,
        api_folders=api_folders,
        ui_folders=ui_folders,
        warnings=warnings,
    )


def format_inspection(inspection: RepoInspection) -> str:
    lines = [
        f"App type: {inspection.app_type}",
        f"Package files: {_join(inspection.package_files)}",
        f"Source folders: {_join(inspection.source_folders)}",
        f"Framework clues: {_join(inspection.framework_clues)}",
        f"API folders: {_join(inspection.api_folders)}",
        f"UI folders: {_join(inspection.ui_folders)}",
        f"Likely test commands: {_join(inspection.test_commands)}",
    ]
    if inspection.warnings:
        lines.append("Warnings:")
        lines.extend(f"- {warning}" for warning in inspection.warnings)
    return "\n".join(lines)


def propose(change_text: str, inspection: RepoInspection) -> str:
    topic = _topic(change_text)
    actions = [
        f"Restate the requested change: {topic}",
        "Inspect the existing app flow before editing files.",
    ]
    if inspection.api_folders:
        actions.append(f"Update backend or API code in likely folders: {_join(inspection.api_folders)}.")
    else:
        actions.append("Find the backend or API entry point before adding server behavior.")
    if inspection.ui_folders:
        actions.append(f"Update UI code in likely folders: {_join(inspection.ui_folders)}.")
    if any(word in change_text.lower() for word in UPLOAD_WORDS):
        actions.append("Add upload validation for file type, file size, and empty file cases.")
        actions.append("Keep uploaded file handling away from hardcoded local paths.")
    if "photo" in change_text.lower() or "image" in change_text.lower():
        actions.append("Add a clear boundary for image analysis so the model or service can be replaced later.")
    if "api key" in change_text.lower() or "vision" in change_text.lower() or "openai" in change_text.lower():
        actions.append("Use environment variables for service credentials and document required placeholders.")
    actions.append("Add or update the narrowest useful tests for the changed behavior.")
    actions.append("Run the relevant test command and record the result.")
    return _format_plan(change_text, inspection, actions)


def write_proposal(root: str | Path = ".", change_path: str | Path = ".specforge/change.md", plan_path: str | Path = ".specforge/plan.md") -> str:
    root_path = Path(root)
    change_file = root_path / change_path
    if not change_file.exists():
        raise FileNotFoundError(change_file)
    inspection = inspect_repo(root_path)
    plan = propose(change_file.read_text(encoding="utf-8"), inspection)
    target = root_path / plan_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(plan, encoding="utf-8")
    return plan


def check_repo(root: str | Path = ".") -> CheckResult:
    root_path = Path(root)
    changed = _changed_files(root_path)
    warnings: list[str] = []
    if not changed:
        return CheckResult((), ("No changed files found. Run this after Codex edits the repo.",))

    code_changed = [path for path in changed if Path(path).suffix in CODE_SUFFIXES and not _is_test(path)]
    tests_changed = [path for path in changed if _is_test(path)]
    docs_changed = [path for path in changed if _is_doc(path)]
    api_changed = [path for path in changed if _has_marker(path, API_MARKERS)]
    generated_changed = [path for path in changed if path.startswith("generated/") or _has_generated_header(root_path / path)]
    changed_text = "\n".join(_safe_read(root_path / path) for path in changed)

    if code_changed and not tests_changed:
        warnings.append("Code changed but no test files changed.")
    if api_changed and not docs_changed:
        warnings.append("API-like files changed but docs or README did not change.")
    if any(word in changed_text.lower() for word in UPLOAD_WORDS) and not any(word in changed_text.lower() for word in VALIDATION_WORDS):
        warnings.append("Upload or image handling changed without obvious file validation.")
    if any(word in changed_text.lower() for word in ENV_WORDS) and not any(path.endswith(".env.example") or _is_doc(path) for path in changed):
        warnings.append("Environment variables or credential markers changed without docs or .env.example updates.")
    if generated_changed:
        warnings.append("Generated files changed directly. Prefer changing source specs or custom extension files.")
    if not warnings:
        warnings.append("No obvious consistency issues found. Still review the diff.")
    return CheckResult(tuple(changed), tuple(warnings))


def format_check(result: CheckResult) -> str:
    lines = ["Changed files:"]
    lines.extend(f"- {path}" for path in result.changed_files) if result.changed_files else lines.append("- none")
    lines.append("Checks:")
    lines.extend(f"- {warning}" for warning in result.warnings)
    return "\n".join(lines)


def _existing(root: Path, names: list[str]) -> list[str]:
    return [name for name in names if (root / name).exists()]


def _dirs(root: Path, names: list[str]) -> list[str]:
    return [name for name in names if (root / name).is_dir()]


def _framework_clues(root: Path) -> list[str]:
    clues: list[str] = []
    package_json = root / "package.json"
    pyproject = root / "pyproject.toml"
    requirements = root / "requirements.txt"
    pubspec = root / "pubspec.yaml"
    text = "\n".join(_safe_read(path).lower() for path in [package_json, pyproject, requirements, pubspec])
    for name, marker in [
        ("FastAPI", "fastapi"),
        ("Django", "django"),
        ("Flask", "flask"),
        ("React Native", "react-native"),
        ("Expo", "expo"),
        ("Next.js", "next"),
        ("React", "react"),
        ("Flutter", "flutter"),
        ("pytest", "pytest"),
        ("Jest", "jest"),
        ("Vitest", "vitest"),
    ]:
        if marker in text:
            clues.append(name)
    return clues


def _test_commands(package_files: tuple[str, ...], clues: tuple[str, ...]) -> list[str]:
    commands: list[str] = []
    if "pyproject.toml" in package_files or "requirements.txt" in package_files:
        commands.append("python -m pytest")
    if "package.json" in package_files:
        commands.append("npm test")
    if "pubspec.yaml" in package_files:
        commands.append("flutter test")
    return commands or ["No obvious test command found"]


def _inspection_warnings(package_files: tuple[str, ...], source_folders: tuple[str, ...], test_commands: tuple[str, ...]) -> list[str]:
    warnings: list[str] = []
    if not package_files:
        warnings.append("No package file found.")
    if not source_folders:
        warnings.append("No common source folders found.")
    if test_commands == ("No obvious test command found",):
        warnings.append("No obvious test command found.")
    return warnings


def _app_type(clues: tuple[str, ...], packages: tuple[str, ...]) -> str:
    if "React Native" in clues or "Expo" in clues:
        return "mobile app"
    if "Flutter" in clues:
        return "mobile app"
    if "Next.js" in clues or "React" in clues:
        return "web app"
    if "FastAPI" in clues or "Django" in clues or "Flask" in clues:
        return "backend app"
    if "package.json" in packages:
        return "JavaScript or TypeScript app"
    if "pyproject.toml" in packages or "requirements.txt" in packages:
        return "Python app"
    return "unknown"


def _contains_name(path: Path, markers: tuple[str, ...]) -> bool:
    if not path.exists():
        return False
    for child in path.rglob("*"):
        rel = child.as_posix().lower()
        if any(marker in rel for marker in markers):
            return True
    return False


def _format_plan(change_text: str, inspection: RepoInspection, actions: list[str]) -> str:
    lines = [
        "# SpecForge Change Plan",
        "",
        "## Requested change",
        "",
        change_text.strip() or "No change request provided.",
        "",
        "## Repo summary",
        "",
        format_inspection(inspection),
        "",
        "## Checklist for Codex",
        "",
    ]
    lines.extend(f"{idx}. {action}" for idx, action in enumerate(actions, start=1))
    lines.extend(["", "## Final check", "", "Run `specforge check` after Codex edits the repo."])
    return "\n".join(lines) + "\n"


def _topic(text: str) -> str:
    cleaned = " ".join(text.strip().split())
    if not cleaned:
        return "No change request provided."
    return cleaned[:180] + ("..." if len(cleaned) > 180 else "")


def _changed_files(root: Path) -> list[str]:
    try:
        result = subprocess.run(["git", "status", "--porcelain"], cwd=root, text=True, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return []
    files: list[str] = []
    for line in result.stdout.splitlines():
        if not line:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path:
            files.append(path.replace("\\", "/"))
    return sorted(set(files))


def _is_test(path: str) -> bool:
    lowered = path.lower()
    return any(marker in lowered for marker in TEST_MARKERS)


def _is_doc(path: str) -> bool:
    lowered = path.lower()
    return lowered.startswith("docs/") or lowered.endswith(".md")


def _has_marker(path: str, markers: tuple[str, ...]) -> bool:
    lowered = path.lower()
    return any(marker in lowered for marker in markers)


def _has_generated_header(path: Path) -> bool:
    return "Generated by SpecForge" in _safe_read(path)[:500]


def _safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _join(items: tuple[str, ...] | list[str]) -> str:
    return ", ".join(items) if items else "none"
