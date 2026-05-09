# SpecForge

Executable specs for coding agents.

SpecForge is a Python CLI for projects where coding agents make repeated application changes. Instead of asking an agent to patch models, schemas, routes, tests, documentation, and client code by hand, you give the agent a smaller surface to edit: one application spec.

The spec lives in `.specforge/app.appspec`. It describes the app in terms of models, screens, workflows, policies, and jobs. SpecForge reads that spec, validates it, shows which files it plans to write, and generates a consistent FastAPI and SQLite API project.

**Agent edited 1 spec file instead of 12 source files.**

## Why This Helps

Coding agents are useful because they can move through code quickly. The same speed can become a problem when a change touches many files. A new approval rule might require a database field, a schema change, a route update, service logic, permissions, fixtures, assertions, docs, and client code. If the agent misses one of those places, the result can look complete while still being inconsistent.

SpecForge changes the workflow. The agent edits the product intent first. The generator then applies that intent to the generated code in a repeatable way. This does not remove the need to review code. It reduces the number of places where the agent has to make judgment calls for routine app changes.

## A Small Example

Here is a workflow from the software spend approval example.

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

That block says what should happen when a manager approves a software request. A normal coding agent might spread that change across many files. With SpecForge, the agent edits the workflow block, then runs validation, planning, and generation.

```bash
specforge validate
specforge plan
specforge apply
```

`validate` checks the spec and prints specific errors. `plan` shows the files that would be created or updated. `apply` writes the generated FastAPI and SQLite project.

## What Gets Generated

SpecForge v0 generates an API project. It includes FastAPI routes, SQLite persistence, Pydantic schemas, CRUD helpers, workflow stubs, tests, and a custom folder for user owned code.

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

Workflow support is intentionally limited in v0. SpecForge generates workflow metadata and service stubs, but it does not pretend to implement every business process. You put real custom behavior in the generated `custom/` folder when the spec is not enough.

## Install

```bash
pip install git+https://github.com/jmpanal/specforge
```

For local development:

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

Generate the API project.

```bash
specforge apply
```

Run the demo.

```bash
specforge demo
```

The demo prints the before and after story for the software spend approval example, including the exact file list a normal agent might patch.

## How To Use It With Coding Agents

When you use Codex, Claude Code, Cursor, or another coding agent, ask the agent to read `.specforge/app.appspec` before editing generated code. For normal product behavior, the first edit should be in the spec.

The usual loop is simple. Edit the spec. Run `specforge validate`. Run `specforge plan`. Run `specforge apply`. Review the generated code. Only edit generated code directly when the spec cannot express what you need.

This works best when the change is about application structure, data models, CRUD behavior, approval flows, or workflow intent. It is less useful for highly custom code where the important details live inside hand written business logic.

## Examples

The repository includes three examples.

1. Task manager. A small task CRUD app with a completion workflow.
2. Software spend approval. The main demo, with Employee, Manager, and Finance roles.
3. Recipe price finder. A workflow app for recipe upload, ingredient review, and price comparison stubs.

The examples are meant to show that SpecForge is not tied to one specific app.

## What SpecForge Is

SpecForge is a compact application spec layer, a CLI, a parser, a validator, a planner, a deterministic generator, and a mapping layer between product intent and generated source files.

It is built for agent workflows inside normal software repositories.

## What SpecForge Is Not

SpecForge is not a general purpose programming language. It is not a replacement for Python, TypeScript, Go, Rust, or normal source code. It is not a magic app builder, a prompt framework, or a replacement for code review. It is experimental and not production ready for every use case.

## Current Status

SpecForge is experimental. The first adapter generates FastAPI and SQLite API projects. Frontend generation is not included in v0. Workflow execution is stub based. Generated code should be reviewed before production use.

The best current use cases are internal tools, CRUD apps, approval flows, workflow apps, and business operations software.

## Prepublish Check

Before publishing a repo that uses SpecForge, run:

```bash
specforge privacy-scan
```

The scan looks for common private artifacts such as local paths, credential markers, private notes, and accidental instruction files.

## Roadmap

Future work includes a Next.js adapter, a Postgres adapter, a Prisma adapter, a Django adapter, editor syntax support, a Tree sitter grammar, real workflow execution, and a benchmark suite.

## Contributing

Try the examples and open issues for missing language primitives, validation rules, or adapters. Small, concrete issues are the most useful right now.
