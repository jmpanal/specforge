# Codex

Use SpecForge to help Codex avoid incomplete changes.

Recommended flow:

```bash
specforge inspect
specforge propose
```

Then ask Codex to implement `.specforge/plan.md`.

After Codex edits the repo:

```bash
specforge check
```

If `check` reports missing tests, missing docs, upload validation gaps, or direct generated file edits, fix those before finalizing.
