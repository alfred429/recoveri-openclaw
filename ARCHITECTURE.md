# Recoveri OpenClaw Architecture

## Repository layout
- agents/ -> durable agent definitions and role configuration
- skills/ -> reusable capabilities and workflows
- workspace/ -> top-level shared workspace content
- workspaces/ -> role-specific and enterprise workspace content
- completions/ -> CLI shell completions
- scripts/ -> repo automation and bootstrap helpers

## Operating model
- GitHub stores infrastructure, architecture, prompts, skills, and durable docs
- The VPS stores runtime state, credentials, sessions, logs, offsets, caches, and local memory
- Runtime state must not be committed to GitHub

## Deployment principle
A new machine should be able to clone this repository and recreate the durable system shape without inheriting machine-specific state.
