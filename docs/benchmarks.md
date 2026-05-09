# Benchmarks

**Agent edited 1 spec file instead of 12 source files.**

No measured benchmark results are published yet.

The new benchmark target is agent completeness, not generator output volume.

## Methodology

Scenario: add photo upload and object detection to an existing app.

Compare:

- normal Codex workflow with a plain prompt
- SpecForge workflow using `inspect`, `propose`, implementation, and `check`

Columns to measure:

- files changed
- related files missed
- tests added or missed
- docs added or missed
- validation gaps found
- total agent turns
- approximate token usage
- time to working change

Target: SpecForge should help the agent catch missing pieces before final review.
