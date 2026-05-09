# SpecForge

Executable specs for coding agents.

SpecForge lets coding agents change software by editing compact executable specs instead of patching scattered source files.

**Agent edited 1 spec file instead of 12 source files.**

## Before / After

Before: an agent patches 12 files.

After: an agent edits 1 spec file. SpecForge validates, plans, and generates consistent code.

## Quickstart

```bash
pip install git+https://github.com/YOUR_GITHUB_USERNAME/specforge
specforge init
specforge validate
specforge plan
specforge apply
specforge demo
```

Local development:

```bash
pip install -e .
```

## 30-second Demo

The main demo uses `examples/software-spend-approval/.specforge/app.appspec`.

```appspec
workflow ApproveSoftwareRequest
  when Manager approves SoftwareRequest
  require SoftwareRequest.status = submitted
  if SoftwareRequest.monthly_cost > 500
    set SoftwareRequest.status pending_finance
    notify Finance
  else
    set SoftwareRequest.status approved
```

Generated output:

```text
generated/
  app/
    main.py
    database.py
    schemas.py
    crud.py
    routes.py
    workflows.py
  tests/
    test_app.py
    test_crud.py
    test_workflows.py
```

**Agent edited 1 spec file instead of 12 source files.**

## Why This Exists

Coding agents are powerful, but they can make scattered inconsistent edits. SpecForge reduces the agent control surface: edit product intent in one spec file, validate it, plan the generated files, then apply deterministic output.

## What It Is Not

- Not a general-purpose programming language.
- Not a replacement for developers.
- Not a magic app builder.
- Not production-ready for every use case.
- Not a substitute for reviewing generated code.

## Current Status

Experimental. Best fit: internal tools, CRUD apps, workflow apps, approval flows, and business operations apps.

v0 generates API-only FastAPI + SQLite projects. Workflow support is stub-based.

## Examples

- `examples/task-manager`
- `examples/software-spend-approval`
- `examples/recipe-price-finder`

## Agent Workflow

With Codex, Claude Code, Cursor, or similar tools:

```bash
specforge validate
specforge plan
specforge apply
```

Agents should edit `.specforge/app.appspec` first, then review generated output.

## Roadmap

- Next.js adapter
- Postgres adapter
- Prisma adapter
- Django adapter
- VS Code syntax highlighting
- Tree-sitter grammar
- real workflow execution engine
- benchmark suite

## Try It

If this matches a problem you have with coding agents, star the repo, try the examples, and open issues for missing primitives or adapters.
