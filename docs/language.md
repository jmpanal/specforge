# SpecForge Language

SpecForge v0 uses a small line-based DSL.

```appspec
app TaskManager

role User

model Task
  title text required
  status enum todo doing done
  owner ref UserProfile required

screen TaskList
  table Task
  filter status

workflow CompleteTask
  when User completes Task
  require Task.status != done
  set Task.status done
```

## Blocks

Supported top-level blocks:

- `app`
- `role`
- `model`
- `screen`
- `workflow`
- `policy`
- `job`

Top-level blocks start at column 0. Block content uses two-space indentation. Blank lines and `#` comments are allowed.

## Field Types

Supported field types:

`text`, `number`, `money`, `date`, `datetime`, `boolean`, `image`, `file`, `email`, `url`, `uuid`, `geo`, `enum`, `ref`

## Field Syntax

```appspec
name type required
name type optional
name enum value1 value2 value3
name ref ModelName required
```

## Validation

The validator catches missing app declarations, duplicate names, malformed fields, unknown field types, missing refs, screen model errors, workflow model errors, invalid indentation, and unknown blocks.

## Limits

v0 is API-only. Workflows are generated as stubs. Frontend generation, production hardening, and full workflow execution are roadmap items.
