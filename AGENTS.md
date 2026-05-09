# SpecForge Agent Guide

- When changing app behavior, edit `.specforge/app.appspec` first.
- Run `specforge validate`.
- Run `specforge plan`.
- Run `specforge apply`.
- Do not manually edit generated files unless required.
- If custom code is needed, put it in generated custom extension folders.
- Keep generated output deterministic.
- Keep errors specific and actionable.
- Run tests before finalizing changes.
