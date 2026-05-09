from __future__ import annotations

import re

from .ast import AppSpec, Field, ValidationError
from .parser import FIELD_TYPES


def validate_spec(spec: AppSpec) -> list[ValidationError]:
    errors: list[ValidationError] = list(spec.parse_errors)
    if not spec.app_declarations:
        errors.append(ValidationError(1, "missing app declaration.", "Add:\n  app TaskManager"))
    if len(spec.app_declarations) > 1:
        for _, line in spec.app_declarations[1:]:
            errors.append(ValidationError(line, "duplicate app declaration."))

    _duplicates("role", [(r.name, r.line) for r in spec.roles], errors)
    _duplicates("model", [(m.name, m.line) for m in spec.models], errors)

    model_names = {m.name for m in spec.models}
    model_fields: dict[str, set[str]] = {}
    for model in spec.models:
        _duplicates("field", [(f.name, f.line) for f in model.fields], errors, f' in model "{model.name}"')
        model_fields[model.name] = {f.name for f in model.fields}
        for field in model.fields:
            _validate_field(field, model_names, errors)

    for screen in spec.screens:
        for line in screen.lines:
            parts = line.text.strip().split()
            if len(parts) >= 2 and parts[0] in {"table", "form", "upload"} and parts[1] not in model_names:
                errors.append(ValidationError(line.line, f'screen "{screen.name}" references missing model "{parts[1]}".'))

    for workflow in spec.workflows:
        body = "\n".join(line.text.strip() for line in workflow.lines)
        for model_name, field_name in re.findall(r"\b([A-Z][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)", body):
            if model_name not in model_names:
                errors.append(ValidationError(workflow.line, f'workflow "{workflow.name}" references missing model "{model_name}".'))
            elif field_name not in model_fields.get(model_name, set()):
                errors.append(ValidationError(workflow.line, f'workflow "{workflow.name}" references missing field "{model_name}.{field_name}".'))
        for model_name in re.findall(r"\b(?:approves|completes|creates|updates|reviews|submits|compares)\s+([A-Z][A-Za-z0-9_]*)\b", body):
            if model_name not in model_names:
                errors.append(ValidationError(workflow.line, f'workflow "{workflow.name}" references missing model "{model_name}".'))

    return sorted(errors, key=lambda e: (e.line, e.message))


def _duplicates(kind: str, items: list[tuple[str, int]], errors: list[ValidationError], suffix: str = "") -> None:
    seen: dict[str, int] = {}
    for name, line in items:
        if name in seen:
            errors.append(ValidationError(line, f'duplicate {kind} name "{name}"{suffix}; first declared on line {seen[name]}.'))
        else:
            seen[name] = line


def _validate_field(field: Field, model_names: set[str], errors: list[ValidationError]) -> None:
    if field.type not in FIELD_TYPES:
        errors.append(ValidationError(field.line, f'field "{field.raw}" uses unknown type "{field.type}".', "Use one of: text, number, money, date, datetime, boolean, image, file, email, url, uuid, geo, enum, ref."))
    if field.type == "enum" and len(field.enum_values) < 2:
        errors.append(ValidationError(field.line, f'field "{field.raw}" must define at least two enum values.'))
    if field.type == "ref" and field.ref_model and field.ref_model not in model_names:
        errors.append(ValidationError(field.line, f'field "{field.raw}" references missing model "{field.ref_model}".', f"Add:\n  model {field.ref_model}\n    name text required"))
