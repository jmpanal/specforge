# Architecture

SpecForge has two layers.

The main layer is the agent guardrail workflow.

- Inspector: scans package files, source folders, framework clues, likely test commands, API folders, UI folders, and setup warnings.
- Proposer: reads `.specforge/change.md` and writes `.specforge/plan.md`, a practical checklist for Codex or another coding agent.
- Checker: reads the current Git status and reports common consistency risks in the diff.

The experimental layer is the older generator workflow.

- Parser: line based `.appspec` parser that preserves line numbers.
- Validator: agent readable errors with specific fixes.
- Planner: stable generated file list.
- Generator: deterministic FastAPI and SQLite output through `fastapi-sqlite-basic`.

The generator remains available, but the primary product is now the guardrail workflow.
