# Claude Code

Use SpecForge to create a concrete checklist before Claude Code edits the repo.

```bash
specforge inspect
specforge propose
```

Claude Code should read `.specforge/plan.md`, implement the checklist, run tests, and then run:

```bash
specforge check
```

The `.appspec` generator is experimental and should not be the default workflow for existing apps.
