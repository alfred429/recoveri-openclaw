# Recoveri OpenClaw Repo Governance

## Purpose
This repository stores Recoveri OpenClaw infrastructure, architecture, skills, prompts, and durable documentation.

## Must be versioned
- agents/ architecture and durable agent definitions
- skills/ source files and SKILL.md files
- workspaces/ durable templates, architecture docs, and intentional shared knowledge
- completions/
- scripts/
- stable configuration intended for multi-machine use

## Must NOT be versioned
- .env
- credentials/
- logs/
- backups/
- media/
- sessions/
- devices/paired.json
- identity/device-auth.json
- memory/*.sqlite
- telegram/update-offset-default.json
- telegram/command-hash-default-*.txt
- exec-approvals.json
- workspaces/*/.openclaw/
- __pycache__/
- *.pyc
- *.bak
- *.bak.*
- machine-local runtime state
- temporary audits and operator scratch files

## Commit policy
Before every push:
1. Check git status
2. Confirm no runtime/state/auth files are staged
3. Commit infra/code/docs separately from local operating artifacts
4. Prefer small, reviewable commits
