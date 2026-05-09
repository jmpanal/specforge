# SpecForge

Executable specs for coding agents.

SpecForge is a small Python CLI that turns one app spec into a generated FastAPI + SQLite API project.

It is for Codex, Claude Code, Cursor, and similar coding agents.

**Agent edited 1 spec file instead of 12 source files.**

## The Problem

Coding agents are good at code, but app changes often spread across many files:

- database model
- schema
- route
- service
- permissions
- tests
- docs
- client code

That gives the agent a large control surface. One missed file can break the change.

## The SpecForge Way

Put the app intent in `.specforge/app.appspec`.

Example:

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

Then run:

```bash
specforge validate
specforge plan
specforge apply
```

SpecForge validates the spec, shows the generated file plan, then writes consistent API code.

## What It Generates Today

v0 generates an API-only FastAPI + SQLite project:

```text
generated/
  README.md
  pyproject.toml
  app/
    main.py
    database.py
    models.py
    schemas.py
    crud.py
    routes.py
    workflows.py
    custom/
      hooks.py
  tests/
    test_app.py
    test_crud.py
    test_workflows.py
```

It does not generate frontend code in v0.

Workflow code is generated as stubs. You add real business logic later.

## Install

```bash
pip install git+https://github.com/YOUR_GITHUB_USERNAME/specforge
```

Local development:

```bash
pip install -e .
```

## Quickstart

Create a new SpecForge setup:

```bash
specforge init
```

Validate the spec:

```bash
specforge validate
```

Preview generated files:

```bash
specforge plan
```

Generate code:

```bash
specforge apply
```

Run the built-in before/after demo:

```bash
specforge demo
```

## Main Demo

The main demo is:

```text
examples/software-spend-approval/.specforge/app.appspec
```

Run:

```bash
specforge demo
```

You will see the normal scattered-edit path and the SpecForge path.

**Agent edited 1 spec file instead of 12 source files.**

## Commands

```bash
specforge init
specforge validate
specforge plan
specforge apply
specforge doctor
specforge explain
specforge demo
specforge privacy-scan
```

`privacy-scan` is a pre-publish check for common private artifacts.

## Examples

- `examples/task-manager`
- `examples/software-spend-approval`
- `examples/recipe-price-finder`

## What SpecForge Is

- a compact application spec layer
- a CLI
- a parser
- a validator
- a planner
- a deterministic generator
- a mapping layer between app intent and generated source files
- a workflow layer for coding agents inside a repo

## What SpecForge Is Not

- not a general-purpose programming language
- not a replacement for Python, TypeScript, Go, Rust, or normal source code
- not a magic app builder
- not a prompt framework
- not a replacement for code review
- not production-ready for every use case

## Best Fit

Good fit:

- internal tools
- CRUD apps
- approval flows
- workflow apps
- business operations apps

Weak fit today:

- custom frontends
- complex distributed systems
- high-security production systems
- apps where the DSL cannot express the behavior yet

## Agent Workflow

For Codex, Claude Code, Cursor, or similar tools:

1. Read `.specforge/app.appspec`.
2. Edit the spec first.
3. Run `specforge validate`.
4. Run `specforge plan`.
5. Run `specforge apply`.
6. Review generated output.
7. Put custom code in generated `custom/` folders.

## Roadmap

- Next.js adapter
- Postgres adapter
- Prisma adapter
- Django adapter
- VS Code syntax highlighting
- Tree-sitter grammar
- real workflow execution engine
- benchmark suite

## Contributing

Try the examples. Open issues for missing DSL primitives, validation rules, or adapters.
