# Agent Workflow

SpecForge now starts from a plain English change request.

1. User writes the desired change in `.specforge/change.md`.
2. Agent runs `specforge inspect` to understand the repo shape.
3. Agent runs `specforge propose` to create `.specforge/plan.md`.
4. Agent implements the checklist in the real app.
5. Agent runs the project tests.
6. Agent runs `specforge check` to catch common missing pieces.
7. Agent explains any remaining risk before finalizing.

The older `.appspec` generator is experimental. Use it only when the user explicitly wants generated FastAPI and SQLite starter code.
