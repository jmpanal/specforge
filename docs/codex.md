# Codex

Use SpecForge as the first edit surface for app behavior.

```bash
specforge validate
specforge plan
specforge apply
```

Recommended flow:

- Read `.specforge/app.appspec`.
- Change the smallest relevant spec block.
- Validate before generation.
- Review the generated diff.
- Put custom logic in generated custom extension folders.
