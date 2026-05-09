# Claude Code

Use SpecForge to keep behavior changes compact and reviewable.

```bash
specforge validate
specforge plan
specforge apply
```

Claude Code should edit `.specforge/app.appspec` before manually patching generated source files. Generated code still needs normal review.
