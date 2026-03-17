# Recoveri Decision & Question Log — Skill Definition
# skill_id: recoveri-decision-log
# version: 1.0
# owner: Neo (CoS) — log keeper
# contributors: All agents
# approval_tier: Tier 1 (auto-execute — logging is non-destructive)
# status: ACTIVE
# pillar: INTERNAL
# value_chain_stage: STRATEGY

---

## Purpose

Track every question Boss poses, every decision made, and every action taken by the enterprise. This creates an auditable trail that feeds into:
- **Skill improvement**: Patterns in questions reveal skill gaps
- **SOUL refinement**: Decision patterns reveal governance gaps
- **Governance iteration**: Escalation patterns reveal tier miscalibration
- **Sprint planning**: Unresolved questions become backlog items

## When to Log

**MANDATORY logging triggers:**
1. Boss asks a question to any agent (via Neo or direct)
2. A decision is made that affects operations, strategy, or governance
3. A task is assigned or completed
4. A governance gate is triggered (any tier)
5. An escalation occurs
6. A skill or SOUL is modified

## Log Format

All entries are appended to `/operations-logs/decisions/YYYY-MM-DD.jsonl`

```json
{
  "timestamp": "ISO 8601",
  "entry_type": "QUESTION | DECISION | ACTION | ESCALATION | GOVERNANCE_GATE",
  "source": "who raised it (Boss, Neo, Optimus, etc.)",
  "target": "who it was directed at",
  "pillar": "CORE | SOCIAL | STUDIOS | TRADERS | PROPERTY | DEVELOPMENTS | INTERNAL",
  "value_chain_stage": "RESEARCH | ANALYSIS | STRATEGY | PROPOSITION | DEVELOPMENT | MARKETING | COMMERCIAL",
  "content": "the actual question, decision, or action description",
  "context": "why this came up — brief background",
  "resolution": "RESOLVED | PENDING | DEFERRED | BLOCKED",
  "resolution_detail": "what was decided or done — null if PENDING",
  "resolved_by": "who resolved it",
  "governance_tier": "T1 | T2 | T3 | T4 | null",
  "follow_up": "any next actions spawned by this entry",
  "tags": ["array", "of", "relevant", "tags"],
  "improvement_signal": "what this entry suggests about skill/soul/governance gaps — null if none obvious"
}
```

## How Agents Use This Skill

### Neo (CoS) — Primary Logger
Neo logs ALL Boss interactions automatically. Every question Boss sends through TG gets a QUESTION entry. Every response that contains a decision gets a DECISION entry.

**Neo's logging rule:** Before closing any Boss interaction, create the log entry. This is non-negotiable.

### C-Level Agents — Action Loggers
When completing tasks, C-Level agents log ACTION entries with their outputs. When triggering governance gates, they log GOVERNANCE_GATE entries.

### Optimus (CEO) — Decision Aggregator
Optimus reviews the decision log daily as part of Kitt's OS Review input. Flags:
- Questions that recur (skill gap signal)
- Decisions that get reversed (governance gap signal)
- Actions that stall (capability gap signal)

## Improvement Feedback Loop

Weekly (or as part of Sprint retrospective):
1. **Kitt** aggregates decision log into patterns report
2. **Optimus** reviews patterns and proposes:
   - Skill updates (if agents keep getting asked the same thing)
   - SOUL updates (if decision-making patterns need adjustment)
   - Governance tier changes (if gates are too loose or too tight)
3. **Neo** presents proposals to Boss for approval
4. Approved changes become Sprint backlog items

## Directory Structure

```
/operations-logs/
├── SCHEMA.md              (existing — general operations)
├── YYYY-MM-DD.jsonl       (existing — operations log)
└── decisions/
    ├── SCHEMA.md           (this skill's schema)
    └── YYYY-MM-DD.jsonl    (daily decision logs)
```

## Example Entries

### Boss Question
```json
{"timestamp":"2026-03-17T14:30:00Z","entry_type":"QUESTION","source":"Boss","target":"Data","pillar":"INTERNAL","value_chain_stage":"STRATEGY","content":"What enterprise services fall under operations?","context":"Smoke test — validating domain knowledge","resolution":"RESOLVED","resolution_detail":"Kitt confirmed: Finance & Tax, Customer Success, HR Ops, Procurement","resolved_by":"Kitt","governance_tier":null,"follow_up":null,"tags":["smoke-test","domain-knowledge","operations"],"improvement_signal":null}
```

### Governance Gate
```json
{"timestamp":"2026-03-17T15:00:00Z","entry_type":"GOVERNANCE_GATE","source":"Neo","target":"Optimus","pillar":"INTERNAL","value_chain_stage":"DEVELOPMENT","content":"Model change request: Data from grok-4-1-fast to deepseek-chat","context":"Boss test of governance enforcement","resolution":"BLOCKED","resolution_detail":"Tier 4 gate held — requires Boss 2FA approval","resolved_by":"System","governance_tier":"T4","follow_up":"Awaiting Boss 2FA if genuine request","tags":["model-change","governance","tier-4","2fa"],"improvement_signal":"Gate working correctly — no skill/soul change needed"}
```

## Integration Points

- **Kitt OS Review (FM5)**: Decision log is a scored data source
- **Boss Dashboard (FM10)**: Decision count, resolution rate, and governance gate stats displayed
- **Sprint Planning**: PENDING/DEFERRED decisions become candidate backlog items
- **Skill Registry (6.11)**: improvement_signal field feeds skill update proposals
