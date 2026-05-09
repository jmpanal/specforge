# Agent Workflow

1. Agent reads `.specforge/app.appspec`.
2. Agent edits the spec.
3. Agent runs `specforge validate`.
4. Agent runs `specforge plan`.
5. Agent runs `specforge apply`.
6. Agent reviews generated output.
7. Agent only edits generated code if the spec cannot express the change.

Generated files are deterministic. User-owned custom code belongs in generated custom extension folders.
