# Recoveri OpenClaw — Configuration Repository

**Classification:** Internal — Recoveri Board
**Status:** Active — Production Configuration

This repository is the durable configuration store for Recoveri's autonomous AI enterprise. The VPS is runtime; GitHub is the source of truth for all deployable configuration.

## Repository Structure

```
recoveri-openclaw/
├── config/           # Agent configuration (openclaw.json)
├── souls/            # Agent identity files (SOUL.md × 6 + ENTERPRISE_SOUL.md)
├── skills/           # Deployed skill definitions ({name}/SKILL.md)
├── governance/       # AGENTS.md, USER.md, Constitution, policy fragments
├── docs/             # Architecture docs, deployment guides
├── .gitignore        # Excludes secrets, runtime data, binaries
└── README.md         # This file
```

## What Lives Here vs Google Drive

| Content | Location | Rationale |
|---------|----------|-----------|
| Agent config (openclaw.json) | GitHub → VPS | Version-controlled, rollback via git |
| Agent SOULs | GitHub → VPS | Identity files need version history + diff |
| Skills (.md) | GitHub → VPS | Skills are code — versioning, PRs, review |
| Constitution | GitHub + Drive | Dual: repo for version control, Drive for Boss access |
| Work orders | Drive only | Operational artifacts, collaboration-friendly |
| Reference docs (.docx/.pdf) | Drive only | Binary files, not suited to git |
| Sprint planning | Drive only | Planning docs, not deployable |
| Runtime logs (.jsonl) | VPS only | Runtime data, ephemeral |

## Deployment Flow

1. Changes made via PR or direct commit (SOUL/Constitution changes require PR + Boss approval)
2. Arthur pulls to VPS: `git pull` → deploy to workspaces
3. Session resets sent to affected agents via Telegram

## Key Conventions

- **workspaces/ is authoritative on VPS**, not agents/
- ENTERPRISE_SOUL.md lives at `{workspace}/shared/ENTERPRISE_SOUL.md`
- Skills deploy as `{workspace}/skills/{skill-name}/SKILL.md`
- Workspace IDs: Neo=`main`, Optimus=`ceo-agent`, Data=`cto-agent`, Alpha=`cro-agent`, Kitt=`coo-agent`, Oracle=`consultant-agent`

## Golden Rules

1. Never hardcode — skills define intent, config defines reality
2. Never overwrite without reviewing the original
3. Document everything
4. Never leave loose ends
