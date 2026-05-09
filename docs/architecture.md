# Architecture

SpecForge has five small parts.

- Parser: line-based parser that preserves line numbers.
- Validator: agent-readable errors with specific fixes.
- Planner: stable file list showing generated paths and source blocks.
- Generator: deterministic output for one adapter.
- Adapter: stack-specific rendering. v0 ships `fastapi-sqlite-basic`.

`.specforge/specmap.json` records generated files, sources, adapter, and reasons.
