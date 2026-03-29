# Altior VPS — Current State
# Generated: 29 March 2026
# After: Governance reset, model upgrade, TG lane policy, persistence config

## Team Structure

| Agent | Role | Agent ID | Model | Supervisor | Worker |
|-------|------|----------|-------|------------|--------|
| Neo | Chief of Staff | main | claude-sonnet-4-6 | Boss | — |
| Optimus | CEO & Orchestrator | ceo-agent | claude-opus-4-6 | Neo/Boss | — |
| Data | CTO | cto-agent | gpt-5.4 (Codex) | Optimus | Bolt |
| Alpha | CRO | cro-agent | claude-opus-4-6 | Optimus | Pixel |
| Kitt | COO | coo-agent | claude-opus-4-6 | Optimus | Scout |
| Oracle | Consultant | consultant-agent | gpt-5.4 (Codex) | Optimus | Sage |
| Bolt | Head of Pipeline Ops | qwen-1 | claude-sonnet-4-6 | Data | — |
| Sage | Head of Research Ops | qwen-2 | claude-sonnet-4-6 | Oracle | — |
| Pixel | Head of Content Ops | qwen-3 | claude-sonnet-4-6 | Alpha | — |
| Scout | Head of Web Ops | qwen-4 | claude-sonnet-4-6 | Kitt | — |

All Claude agents on Anthropic Max OAuth. GPT-5.4 agents on OpenAI Codex OAuth.
All fallbacks: xai/grok-4-1-fast.

## Telegram Lane Policy

| Topic | Lane | Agent | requireMention |
|-------|------|-------|---------------|
| 1 | Neo intake | main | false |
| 2 | Reports | ceo-agent | true |
| 3 | TECH working | cto-agent | false |
| 6 | CSM working | cro-agent | false |
| 8 | OPS working | coo-agent | false |
| 10 | R&D working | consultant-agent | false |
| 12 | OPS worker | qwen-4 (Scout) | true |
| 14 | R&D worker | qwen-2 (Sage) | true |
| 625 | TECH worker | qwen-1 (Bolt) | true |
| 627 | CSM worker | qwen-3 (Pixel) | true |
| 16 | Inactive | — | disabled |
| 18 | System | — | disabled |
| 624 | Insights | — | disabled |

## Governance Model

- AGENTS.md = primary governance carrier (loaded every session, inherited by sub-agents)
- SOUL.md = agent-specific identity, role, boundaries, qualifications, operational protocols
- USER.md = shared TG topology + per-agent role supplement + Boss context
- MEMORY.md = cross-pillar durable truths (no venture narrowing)
- ENTERPRISE_SOUL.md = source canon only, NOT runtime governance

Rule: If it is not in an auto-loaded workspace-root file, it is not runtime governance.

## Runtime Config

- Session persistence: directors persistent (mode:session), workers on-demand (mode:run)
- Session maintenance: enforce mode (pruneAfter 30d, maxEntries 500, rotateBytes 10mb)
- Memory search: hybrid (FTS + vector), provider: ollama/nomic-embed-text (local, zero cost)
- Memory flush: enabled (pre-compaction auto-save)
- Context pruning: cache-ttl mode, 1h TTL
- Context tokens: 100,000 per agent
- Heartbeat: 30m all agents, 05:30-23:59

## Gateway

- systemd service: openclaw-gateway.service (system-level, enabled, auto-restart)
- Port: 18789
- Gmail watcher: gog on port 18802
- Bot: @R1VPSBOT, polling mode

## Cron Agents (32 jobs)

- L-series: L1 (15m), L2 (2h), L3 (2h), L4 (1h) — all on qwen2.5:3b local
- A-series: A1-A7 (2-6h intervals) — DeepSeek
- D-series: D1-D4 (1-3h) — DeepSeek
- G-series: G1 (1h), G2 (2h) — Groq/Llama
- Trading loop (4h), Google Trends (12h), RSS (4h), HN (4h), AI Trends (6h)
- Governance sync (15m), Spawn audit (15m), Session reaper (1h)
- Kitt OS Review (daily 06:00), A7 digest to Boss (06:10)

## Backups (today)

- /root/governance-deploy-backup/20260329_085426 — pre-governance
- /root/governance-merge-backup-20260329_095016 — pre-merge-back
- /root/.openclaw/openclaw.json.bak-pre-persistence-* — pre-persistence
- /root/.openclaw/openclaw.json.bak-pre-embedding-* — pre-embedding
- /root/.openclaw/openclaw.json.bak-pre-tg-lanes-* — pre-TG lanes
- /root/.openclaw/openclaw.json.bak-pre-model-upgrade-* — pre-model upgrade

## Known Issues (open)

- Task-router skill needs update to match new spawn model
- TG outbound topic targeting (replies may still go to General)
- Gateway CLI probe reports "unreachable" (cosmetic, service is healthy)
- Gateway reports "systemd not installed" (cosmetic, only checks user-scope)
- 7 plaintext secrets remaining (SEC-INC-001)
- Firewall not active (ports 18803, 8901 exposed)
- L2 cron waste (translates same 5 strings), A2 blocked (403)
- 1,821 unrotated cron output files
- Old user-level systemd unit has inline secrets
- governance-sync manifest has 9 legacy task-router lines


## Late Session Updates - 29 March evening

### Dashboard and Auth
- ops.altior.one live with HTTPS - Let s Encrypt production cert
- board.craab.io also serving HTTPS
- Google OAuth migrated to Web application client - Recoveri Board
- Credentials in OpenClaw secret manager - dashboard-google.env
- altior-dashboard.service wired to new env file
- Dashboard route split intentional: 18803 auth catch-all, 8901 v2 APIs no auth yet

### Security Cleanup - Sprint 1
- 6 secret-bearing backup files archived to security-archive
- 3 stale user-scope services disabled
- Mozart retired workspace archived and removed
- Gateway systemd unit: zero inline secrets
- nftables: ports 22/80/443 opened and persisted
- Hetzner cloud firewall: SSH/HTTP/HTTPS rules applied

### Backlog Status
- P1: EMPTY - first time since 24 March
- Cadence, escalation standard, scoreboard moved to P3
- Next focus: P2 stability items
