from __future__ import annotations

from pathlib import Path

from .ast import AppSpec, BlockLine, Field, Job, Model, Policy, Role, Screen, ValidationError, Workflow

TOP_LEVEL = {"app", "role", "model", "screen", "workflow", "policy", "job"}
FIELD_TYPES = {"text", "number", "money", "date", "datetime", "boolean", "image", "file", "email", "url", "uuid", "geo", "enum", "ref"}
REQUIREDNESS = {"required", "optional"}


def parse_file(path: str | Path) -> AppSpec:
    p = Path(path)
    return parse_text(p.read_text(encoding="utf-8"), p)


def parse_text(text: str, path: str | Path | None = None) -> AppSpec:
    app_declarations: list[tuple[str, int]] = []
    roles: list[Role] = []
    models: list[Model] = []
    screens: list[Screen] = []
    workflows: list[Workflow] = []
    policies: list[Policy] = []
    jobs: list[Job] = []
    errors: list[ValidationError] = []
    current_kind: str | None = None
    current_index: int | None = None

    def add_block_line(line_no: int, content: str) -> None:
        nonlocal screens, workflows, policies, jobs
        item = BlockLine(line_no, content)
        if current_kind == "screen" and current_index is not None:
            block = screens[current_index]
            screens[current_index] = Screen(block.name, block.line, block.lines + (item,))
        elif current_kind == "workflow" and current_index is not None:
            block = workflows[current_index]
            workflows[current_index] = Workflow(block.name, block.line, block.lines + (item,))
        elif current_kind == "policy" and current_index is not None:
            block = policies[current_index]
            policies[current_index] = Policy(block.name, block.line, block.lines + (item,))
        elif current_kind == "job" and current_index is not None:
            block = jobs[current_index]
            jobs[current_index] = Job(block.name, block.line, block.lines + (item,))

    for line_no, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw:
            errors.append(ValidationError(line_no, "tabs are not valid indentation; use two spaces."))
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()
        if indent == 0:
            parts = stripped.split(maxsplit=1)
            kind = parts[0]
            if kind not in TOP_LEVEL:
                errors.append(ValidationError(line_no, f'unknown top-level block "{kind}".', "Use one of: app, role, model, screen, workflow, policy, job."))
                current_kind = None
                current_index = None
                continue
            if len(parts) == 1 or not parts[1].strip():
                errors.append(ValidationError(line_no, f'{kind} block is missing a name.'))
                current_kind = None
                current_index = None
                continue
            name = parts[1].strip()
            current_kind = kind
            if kind == "app":
                app_declarations.append((name, line_no))
                current_index = None
            elif kind == "role":
                roles.append(Role(name, line_no))
                current_index = None
            elif kind == "model":
                models.append(Model(name, line_no))
                current_index = len(models) - 1
            elif kind == "screen":
                screens.append(Screen(name, line_no))
                current_index = len(screens) - 1
            elif kind == "workflow":
                workflows.append(Workflow(name, line_no))
                current_index = len(workflows) - 1
            elif kind == "policy":
                policies.append(Policy(name, line_no))
                current_index = len(policies) - 1
            elif kind == "job":
                jobs.append(Job(name, line_no))
                current_index = len(jobs) - 1
            continue

        if current_kind is None:
            errors.append(ValidationError(line_no, "indented line appears before any block."))
            continue
        if indent % 2 != 0:
            errors.append(ValidationError(line_no, "invalid indentation; use multiples of two spaces."))
            continue
        if current_kind in {"app", "role"}:
            errors.append(ValidationError(line_no, f"{current_kind} blocks do not accept indented content."))
            continue
        if current_kind == "model":
            if indent != 2:
                errors.append(ValidationError(line_no, "model field lines must be indented by exactly two spaces."))
                continue
            field = _parse_field(stripped, line_no, errors)
            if field is not None and current_index is not None:
                model = models[current_index]
                models[current_index] = Model(model.name, model.line, model.fields + (field,))
        else:
            add_block_line(line_no, raw[2:])

    return AppSpec(
        path=Path(path) if path is not None else None,
        app_declarations=tuple(app_declarations),
        roles=tuple(roles),
        models=tuple(models),
        screens=tuple(screens),
        workflows=tuple(workflows),
        policies=tuple(policies),
        jobs=tuple(jobs),
        parse_errors=tuple(errors),
    )


def _parse_field(text: str, line_no: int, errors: list[ValidationError]) -> Field | None:
    parts = text.split()
    if len(parts) < 2:
        errors.append(ValidationError(line_no, f'malformed field line "{text}".', "Use: field_name type required"))
        return None
    name, field_type = parts[0], parts[1]
    if field_type == "enum":
        values = tuple(parts[2:])
        if len(values) < 2 or any(v in REQUIREDNESS for v in values):
            errors.append(ValidationError(line_no, f'invalid enum declaration "{text}".', "Use: status enum todo doing done"))
        return Field(name=name, type=field_type, line=line_no, enum_values=values, raw=text)
    if field_type == "ref":
        if len(parts) != 4 or parts[3] not in REQUIREDNESS:
            errors.append(ValidationError(line_no, f'malformed ref field "{text}".', "Use: owner ref User required"))
            return Field(name=name, type=field_type, line=line_no, raw=text)
        return Field(name=name, type=field_type, line=line_no, required=parts[3] == "required", ref_model=parts[2], raw=text)
    if len(parts) > 3 or (len(parts) == 3 and parts[2] not in REQUIREDNESS):
        errors.append(ValidationError(line_no, f'malformed field line "{text}".', "Use: field_name type required"))
        return Field(name=name, type=field_type, line=line_no, raw=text)
    required = parts[2] == "required" if len(parts) == 3 else False
    return Field(name=name, type=field_type, line=line_no, required=required, raw=text)
