# Adapter API

Adapters receive a validated `AppSpec` and return a mapping of relative file paths to complete file contents.

Rules for future adapters:

- deterministic output for identical input
- stable sorted models, fields, routes, and tests
- generated headers for generated source files
- custom extension folders for user-owned code
- no frontend generation unless the adapter explicitly supports it
- no hidden network calls
