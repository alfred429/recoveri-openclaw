---
name: model-router-governance
version: 2.0
description: Manages model selection, API key rotation, and provider configuration changes through the RECOVERI governance chain. No config change happens without proper approval.
trigger: "model change|key rotate|tier promote|fallback update|model governance|provider change"
---

# model-router-governance v2.0

## Description
Manages model selection, API key rotation, and provider configuration changes through the RECOVERI governance chain. No config change happens without proper approval.

## DESIGN PRINCIPLE

Model assignments live in `openclaw.json`. Tier labels live in `/root/.openclaw/config/tier-map.md`.
This skill governs the PROCESS for changing them.
This skill does NOT define which agent runs which model — that is config's job.
This skill defines WHO can propose, approve, and execute model changes.

## Governance Flow
1. **Propose** — Data (CTO) or Alfred (Boss) submits a change request
2. **Validate** — Skill checks the request is well-formed and within budget
3. **Approve** — Optimus (CEO) reviews and approves/rejects
4. **Execute** — Optimus (CEO) applies the approved change to `openclaw.json` AND updates `tier-map.md`
5. **Monitor** — Kitt (COO) monitors post-change health for 24h

## Supported Change Types

### model-change
Change the primary or fallback model for an agent.
```
/model-change --agent neo --slot primary --model <provider/model-name> --reason "Cost optimisation"
```

### key-rotate
Rotate an API key for a provider.
```
/key-rotate --provider <provider-name> --reason "Scheduled monthly rotation"
```

### tier-promote
Promote an agent to a higher cost tier.
```
/tier-promote --agent <agent-name> --from <current-tier> --to <target-tier> --reason "Revenue milestone hit"
```

### fallback-update
Change fallback configuration for an agent.
```
/fallback-update --agent <agent-name> --fallback <provider/model-name> --reason "Better performance on fallback"
```

## Change Request Schema
Every change request MUST include:
- `change_type`: model-change | key-rotate | tier-promote | fallback-update
- `agent`: Target agent name (or "global" for provider-level changes)
- `proposed_by`: Agent or user who proposed the change
- `reason`: Why this change is needed
- `impact`: Expected cost/performance impact
- `rollback_plan`: How to revert if things go wrong

## Approval Rules
- **Model changes**: Optimus approval required. Data must confirm technical compatibility.
- **Key rotations**: Kitt can approve routine rotations. Optimus for emergency rotations.
- **Tier promotions**: Optimus approval required. Must include budget justification.
- **Fallback updates**: Data can approve if within same cost tier. Optimus if crossing tiers.

## Execution Protocol
Once approved, Optimus executes by:
1. Creating a backup of current config: `cp openclaw.json openclaw.json.bak.$(date +%s)`
2. Applying the change via OpenClaw CLI or direct config edit
3. Updating `/root/.openclaw/config/tier-map.md` to reflect the change
4. Restarting the gateway if required
5. Running a smoke test (single message to affected agent)
6. **Resetting affected agent sessions** with `/new` so they pick up new config
7. Reporting result back through chain

## Post-Change Monitoring (Kitt)
After any change, Kitt monitors for 24 hours:
- Response latency (flag if >2x baseline)
- Error rate (flag if >5%)
- Cost per message (flag if >1.5x projected)
- Fallback trigger rate (flag if >20%)

Alert thresholds trigger automatic rollback proposal to Optimus.

## Budget Guardrails
Current monthly budget: check with Kitt for live figure (target: under enterprise budget cap)
- No single agent may exceed 40% of total budget
- Tier promotions require projected monthly cost to stay under cap
- Emergency budget override requires Boss (Alfred) approval only

## Tier System (labels only — config maps these to actual models)

| Tier | Label | Description | Typical Use |
|------|-------|-------------|-------------|
| 0 | LOCAL_FREE | Mac Mini workers via Oracle bridge | R&D, conception, zero-cost research |
| 0 | CRON_FREE | Qwen free tier (1M tokens/day) | Scheduled/background tasks |
| 1 | PREMIUM | Highest reasoning capability | Reserved for future use |
| 1.5 | ELEVATED | Above operational | High-value analysis, business cases |
| 2 | OPERATIONAL | Standard working tier | All routine board agent work |
| 3 | ECONOMY | Lowest cost | Sub-agents, fallback models |

**Current tier assignments per agent: read `/root/.openclaw/config/tier-map.md`.**

## Tier Promotion Rules

Promotions follow capability need and budget availability:
- ECONOMY → OPERATIONAL: Data can approve if budget allows
- OPERATIONAL → ELEVATED: Optimus approval required + budget justification
- ELEVATED → PREMIUM: Optimus approval + Boss sign-off required
- Any tier → LOCAL_FREE: Automatic if Mac Mini bridge is available and task is suitable

**Demotions** (cost reduction): Data can approve. No governance overhead for moving DOWN tiers.

## Audit Trail
Every change is logged to `/root/.openclaw/governance/model-changes.log`:
```
[2026-03-16T10:00:00Z] PROPOSED by=Data type=model-change agent=neo model=<new-model> reason="Cost opt"
[2026-03-16T10:05:00Z] APPROVED by=Optimus change_id=MC-001
[2026-03-16T10:06:00Z] EXECUTED by=Optimus change_id=MC-001 result=success sessions_reset=[neo] tier_map_updated=yes
[2026-03-16T10:06:30Z] MONITORING by=Kitt change_id=MC-001 status=watching expires=2026-03-17T10:06:00Z
```

## Critical: Session Reset After Model Changes

**Any model change MUST be followed by session resets** for affected agents.
Stale sessions retain the OLD model config loaded at session start.
Optimus must execute `/new` for every affected agent after applying config changes.
This is NOT optional — without session reset, agents continue on the old model indefinitely.

---

## CHANGELOG

| Version | Date | Change |
|---------|------|--------|
| 1.0 | March 2026 | Initial governance skill |
| 2.0 | 16 March 2026 | **FULL REDESIGN** — Optimus as executor (Mozart merged), tier-map.md as reference file, CRON_FREE tier added, removed all hardcoded model names, mandatory session reset + tier-map update in execution protocol |
