# SpecForge

Guardrails for coding agents.

SpecForge helps Codex, Claude Code, Cursor, and similar tools make safer changes in an existing repo. You describe the change you want in plain English. SpecForge inspects the repo, creates a checklist for the agent, and checks the final diff for common missing pieces.

The main idea is simple. Coding agents can move quickly, but they can also miss related files. A photo upload feature might need UI code, an API endpoint, file validation, a model or database change, tests, and documentation. SpecForge does not write the feature by itself. It helps the agent avoid treating the change as one isolated file edit.

**Agent edited 1 spec file instead of 12 source files.**

## A Beginner Example

Imagine you are building a mobile app where a user uploads a photo, and the app returns a sentence like this:

```text
There is a sofa, a table, and a TV.
```

You write that request in `.specforge/change.md` using normal language.

```text
I want users to upload a photo. The app should analyze the photo and return a short sentence listing the objects in it, such as sofa, table, and TV.
```

Then you run:

```bash
specforge inspect
specforge propose
```

`inspect` looks at the repo and reports what kind of app it seems to be, where source files live, what test command probably exists, and whether there are obvious missing pieces.

`propose` reads `.specforge/change.md` and writes `.specforge/plan.md`. That plan is a checklist you can give to Codex. For the photo app, it will remind Codex to look for the upload screen, backend upload endpoint, image analysis boundary, file validation, tests, and documentation.

After Codex makes the change, run:

```bash
specforge check
```

`check` looks at the current Git diff and reports common risks, such as code changed without tests, API changes without docs, upload logic without obvious file validation, environment variable usage without documentation, or direct edits to generated files.

## Install

```bash
pip install git+https://github.com/jmpanal/specforge
```

For local development, run this from the repository root.

```bash
pip install -e .
```

## Quickstart

Create SpecForge files in your repo.

```bash
specforge init
```

Write your feature request in:

```text
.specforge/change.md
```

Inspect the repo.

```bash
specforge inspect
```

Create the agent checklist.

```bash
specforge propose
```

Ask Codex to implement `.specforge/plan.md`.

After Codex edits files, check the result.

```bash
specforge check
```

## What SpecForge Does

SpecForge gives coding agents a safer workflow:

1. Describe the change in plain English.
2. Inspect the repo before editing.
3. Produce a practical implementation checklist.
4. Let Codex or another agent edit the real app.
5. Check the final diff for common missing pieces.

This is meant for people who want to use coding agents without manually knowing every file that might need to change.

## Experimental Generator

SpecForge still includes an experimental `.appspec` parser and FastAPI plus SQLite generator. That older workflow can create a backend starter project from `.specforge/app.appspec`.

The generator is not the main product promise anymore. It is useful for experiments and internal CRUD style apps, but it is not what you should start with if you are using Codex to change an existing app.

Generator commands still exist:

```bash
specforge validate
specforge plan
specforge apply
specforge demo
```

## What It Does Not Do

SpecForge does not build your full app. It does not generate mobile screens. It does not call image recognition services. It does not replace Codex, Claude Code, Cursor, or code review.

For the photo app example, SpecForge can help Codex plan the upload flow and check for missing pieces. Codex still needs to implement the actual app logic and any AI vision integration.

## Best Fit

SpecForge is best for agent assisted changes where several parts of a repo may need to move together. Examples include uploads, API changes, CRUD features, settings screens, permission changes, workflow changes, and integration work.

It is less useful for one line fixes or fully custom product logic where there is no repeatable structure to check.

## Prepublish Check

Before publishing a repo that uses SpecForge, run:

```bash
specforge privacy-scan
```

The scan looks for common private artifacts such as local paths, credential markers, private notes, and accidental instruction files.
