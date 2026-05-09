# Launch

**Agent edited 1 spec file instead of 12 source files.**

## GitHub Description

Guardrails that help Codex plan changes and check whether the final diff is complete.

## Hacker News Title

SpecForge: guardrails for coding agents changing existing repos

## Hacker News Post

SpecForge helps coding agents avoid incomplete repo changes.

The workflow is intentionally simple. Write the change you want in plain English. Run `specforge inspect` to summarize the repo. Run `specforge propose` to create a checklist for Codex. After Codex edits the code, run `specforge check` to flag common missing pieces such as code without tests, API changes without docs, upload logic without validation, or direct edits to generated files.

The older `.appspec` FastAPI generator still exists, but it is now experimental. The main product is the guardrail workflow for existing apps.

## Reddit Draft

I built SpecForge as a guardrail tool for coding agents. It does not replace Codex. It helps Codex work more safely by inspecting the repo, creating a concrete implementation checklist, and checking the final diff for common omissions.

## X Thread Draft

1. SpecForge is guardrails for coding agents.
2. Write a change request in plain English.
3. Run `specforge inspect` and `specforge propose`.
4. Let Codex implement the plan.
5. Run `specforge check` to catch missing tests, docs, upload validation, and direct generated file edits.

## LinkedIn Draft

SpecForge started as an executable spec experiment. The sharper version is a guardrail workflow for coding agents: inspect the repo, create a checklist, let the agent implement, then check the diff for common missing pieces.

## Demo GIF Ideas

- `specforge inspect` on a mobile app repo
- writing `.specforge/change.md`
- `specforge propose` creating a Codex checklist
- `specforge check` flagging code without tests
- privacy scan before publish

## Issue Labels

- good first issue
- adapter
- language
- docs
- validation

## Good First Issues

- Improve framework detection in `inspect`.
- Add more `check` rules for mobile apps.
- Add JSON output for `inspect`.
- Add JSON output for `check`.
- Add docs for non programmers using Codex.
- Add command examples for Windows shells.
- Add more privacy scan patterns.
- Add examples for image upload apps.
- Add examples for auth changes.
- Add tests for rename handling in Git status.

## Comparison Angles

- prompt only agent work vs inspect plan check workflow
- scattered edits vs checklist driven edits
- raw diff review vs consistency checks
- hidden missing tests vs explicit test warning
- app generator promise vs agent guardrail promise
