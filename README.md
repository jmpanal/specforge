# SpecForge

Executable specs for coding agents.

SpecForge is a tool that helps coding agents make app changes by editing one simple spec file first.

Think of the spec file as a small blueprint for a backend app. It says what models exist, what fields they have, what workflows matter, and what basic rules the app should follow. SpecForge reads that blueprint, checks it for mistakes, shows which files it is going to create, and then generates backend code from it.

The point is not to replace normal code. The point is to give coding agents a cleaner place to start. When an agent edits many files by hand, it can easily miss one. When the agent edits the spec first, SpecForge can generate the matching backend files in a repeatable way.

**Agent edited 1 spec file instead of 12 source files.**

## For Example

Imagine you have an app where employees request paid software, managers approve it, and finance needs to review expensive requests.

Without SpecForge, a coding agent might need to edit the database model, the API schema, the route, the service logic, the permission check, test fixtures, test assertions, docs, and client code. That is a lot of places for one rule.

With SpecForge, the agent can edit one workflow block in `.specforge/app.appspec`.

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

In plain English, this says that a manager can approve a submitted software request. If the monthly cost is above 500, the request goes to finance. Otherwise, it is approved.

After editing the spec, the agent runs three commands.

```bash
specforge validate
specforge plan
specforge apply
```

`validate` checks that the spec makes sense. `plan` shows the files that SpecForge will create or update. `apply` writes the generated FastAPI and SQLite backend project.

## Install

```bash
pip install git+https://github.com/jmpanal/specforge
```

For local development, run this from the repository root.

```bash
pip install -e .
```

## Quickstart

Create a SpecForge setup in a repo.

```bash
specforge init
```

Validate the default spec.

```bash
specforge validate
```

Preview the generated files.

```bash
specforge plan
```

Generate the backend project.

```bash
specforge apply
```

Run the demo.

```bash
specforge demo
```

The demo prints the same before and after story from the software spend approval example.

## What Gets Generated

SpecForge v0 generates a FastAPI and SQLite backend project. It includes API routes, SQLite persistence, Pydantic schemas, CRUD helpers, workflow stubs, tests, and a custom folder for code that you own.

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

The generated code is meant to be reviewed. SpecForge gives you a consistent starting point, not a finished production system.

## What It Does Not Do Yet

SpecForge does not generate a frontend in v0. It does not fully execute workflows yet. Workflows are generated as metadata and service stubs so you have a clear place to add real business logic.

SpecForge is also not a general purpose programming language. It is not a replacement for Python, TypeScript, Go, Rust, or normal source code. It is not a magic app builder and it is not a replacement for code review.

## How To Use It With Codex Or Claude Code

When you use Codex, Claude Code, Cursor, or another coding agent, ask the agent to read `.specforge/app.appspec` before editing generated code.

For normal product behavior, the first edit should be in the spec. Then the agent should run `specforge validate`, `specforge plan`, and `specforge apply`. After that, review the generated code like you would review any other code.

If the spec cannot express what you need, put custom logic in the generated `custom` folder or edit normal source files directly. SpecForge is useful because it handles the boring repeatable parts, not because it can express every possible app.

## Examples

The repository includes three examples. The task manager example is a small CRUD app with a completion workflow. The software spend approval example is the main demo. The recipe price finder example shows how external services can be represented as workflow stubs.

These examples are meant to show that SpecForge is not tied to one specific app.

## Current Status

SpecForge is experimental. The first adapter generates FastAPI and SQLite backend projects. The best current use cases are internal tools, CRUD apps, approval flows, workflow apps, and business operations software.

Generated code should be reviewed before production use.

## Prepublish Check

Before publishing a repo that uses SpecForge, run this command.

```bash
specforge privacy-scan
```

The scan looks for common private artifacts such as local paths, credential markers, private notes, and accidental instruction files.

## Roadmap

Future work includes a Next.js adapter, a Postgres adapter, a Prisma adapter, a Django adapter, editor syntax support, a Tree sitter grammar, real workflow execution, and a benchmark suite.

## Contributing

Try the examples and open issues for missing language primitives, validation rules, or adapters. Small, concrete issues are the most useful right now.
