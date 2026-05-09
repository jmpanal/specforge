# Security

SpecForge does not make generated or agent-written code production safe by itself.

Use `specforge check` after agent edits to catch common risks, especially upload changes without validation and environment variable usage without documentation.

Use `specforge privacy-scan` before publishing.

Review any external integration, upload handling, authentication, authorization, and credential handling before production use.
