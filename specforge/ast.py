from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class ValidationError:
    line: int
    message: str
    fix: str | None = None

    def format(self) -> str:
        out = f"Line {self.line}: {self.message}"
        if self.fix:
            out += f"\nFix:\n{self.fix}"
        return out


@dataclass(frozen=True)
class BlockLine:
    line: int
    text: str


@dataclass(frozen=True)
class Role:
    name: str
    line: int


@dataclass(frozen=True)
class Field:
    name: str
    type: str
    line: int
    required: bool | None = None
    enum_values: tuple[str, ...] = ()
    ref_model: str | None = None
    raw: str = ""


@dataclass(frozen=True)
class Model:
    name: str
    line: int
    fields: tuple[Field, ...] = ()


@dataclass(frozen=True)
class Screen:
    name: str
    line: int
    lines: tuple[BlockLine, ...] = ()


@dataclass(frozen=True)
class Workflow:
    name: str
    line: int
    lines: tuple[BlockLine, ...] = ()


@dataclass(frozen=True)
class Policy:
    name: str
    line: int
    lines: tuple[BlockLine, ...] = ()


@dataclass(frozen=True)
class Job:
    name: str
    line: int
    lines: tuple[BlockLine, ...] = ()


@dataclass(frozen=True)
class PlannedFile:
    path: str
    action: str
    source: str
    reason: str


@dataclass(frozen=True)
class AppSpec:
    path: Path | None = None
    app_declarations: tuple[tuple[str, int], ...] = ()
    roles: tuple[Role, ...] = ()
    models: tuple[Model, ...] = ()
    screens: tuple[Screen, ...] = ()
    workflows: tuple[Workflow, ...] = ()
    policies: tuple[Policy, ...] = ()
    jobs: tuple[Job, ...] = ()
    parse_errors: tuple[ValidationError, ...] = ()

    @property
    def app_name(self) -> str | None:
        return self.app_declarations[0][0] if self.app_declarations else None

    @property
    def source_label(self) -> str:
        if self.path is None:
            return ".specforge/app.appspec"
        parts = self.path.as_posix().split("/")
        if ".specforge" in parts:
            idx = parts.index(".specforge")
            return "/".join(parts[idx:])
        return self.path.as_posix()
