# SpecForge Claude Code Guide

- Start behavior changes in `.specforge/app.appspec`.
- Run `specforge validate`, then `specforge plan`, then `specforge apply`.
- Avoid manual edits to generated files unless the spec cannot express the change.
- Put custom logic in generated custom extension folders.
- Keep changes small, deterministic, and covered by tests.
