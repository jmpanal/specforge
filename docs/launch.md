# Launch

**Agent edited 1 spec file instead of 12 source files.**

## GitHub Description

Executable specs so coding agents edit product intent instead of patching scattered source files.

## Hacker News Title

SpecForge: executable specs so coding agents edit 1 file instead of 12

## Hacker News Post

SpecForge is an installable development layer for coding agents.

It is not another app generator. It is a control layer: agents edit `.specforge/app.appspec`, then SpecForge validates, plans, and generates deterministic API code.

The first adapter is intentionally small: FastAPI + SQLite, API-only, workflow stubs. No fake benchmark numbers yet; the benchmark methodology is included in the repo.

## Reddit Draft

I built SpecForge, a small spec layer for coding agents. Instead of asking an agent to patch models, schemas, routes, tests, docs, and client code by hand, the agent edits one compact app spec. SpecForge validates it, shows the file plan, and generates deterministic FastAPI + SQLite code.

## X Thread Draft

1. SpecForge is executable specs for coding agents.
2. The goal: reduce scattered agent edits.
3. Agent edited 1 spec file instead of 12 source files.
4. v0 ships a parser, validator, planner, CLI, and FastAPI + SQLite generator.
5. It is experimental, API-only, and workflow support is stub-based.

## LinkedIn Draft

SpecForge is a compact application spec layer for coding agents. The thesis: agents are strongest when the control surface is small. Edit intent in one spec file, validate, plan, generate, then review.

## Demo GIF Ideas

- `specforge demo` before/after terminal run
- edit one workflow block
- `specforge plan` file mapping
- generated FastAPI route smoke test
- privacy scan before publish

## Issue Labels

- good first issue
- adapter
- language
- docs
- validation

## Good First Issues

- Add DSL examples for date fields.
- Improve validator fix messages.
- Add more workflow examples.
- Add generated route tests for update/delete.
- Add stack file validation details.
- Add JSON output for `specforge plan`.
- Add docs for custom hooks.
- Add command examples for Windows shells.
- Add app spec syntax highlighting notes.
- Add more privacy scan patterns.

## Comparison Angles

- normal scattered agent edits vs one spec edit
- source patching vs intent patching
- manual file discovery vs generated file map
- inconsistent edits vs deterministic generation
- prompt-only workflow vs validated spec workflow
