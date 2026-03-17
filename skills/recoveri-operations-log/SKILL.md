# recoveri-operations-log v1.0
# Captures all operational data from day one. Every action, every agent, every pillar.

---

## Purpose

This skill provides a structured logging standard for all agent operations. Every task
executed, decision made, and output produced is logged with pillar and value chain
metadata. This is the data foundation for Kitt's daily OS Review, the Boss Dashboard,
cost tracking, and the Intelligence Layer.

## Log Entry Format

Every operation produces a log entry with these fields:

```
timestamp:        ISO 8601 UTC (e.g. 2026-03-17T14:30:00Z)
agent:            Agent ID who performed the work (neo, optimus, data, alpha, kitt, oracle)
pillar:           Pillar code(s) from value-chain-map (CORE, SOCIAL, STUDIOS, TRADERS, PROPERTY, DEVELOPMENTS, INTERNAL)
value_chain_stage: Stage code from value-chain-map (RESEARCH, ANALYSIS, STRATEGY, PROPOSITION, DEVELOPMENT, MARKETING, COMMERCIAL)
task_summary:     One-line description of what was done (max 200 chars)
outcome:          COMPLETED | PARTIAL | BLOCKED | FAILED | ESCALATED
cost_tier:        LOCAL_FREE | CRON_FREE | ECONOMY | OPERATIONAL | PREMIUM
model_used:       Model identifier (e.g. grok-4-1-fast, qwen-coder-turbo, deepseek-chat)
duration_seconds: Estimated execution time in seconds
tokens_used:      Approximate token count (input + output)
work_order_ref:   Reference to work order if applicable (e.g. BATCH_5A_P3)
decision_log:     Brief rationale for key decisions made during execution (optional)
escalated_to:     Agent ID if escalated (optional)
blocker:          Description of blocker if BLOCKED/PARTIAL (optional)
```

## When to Log

Log on EVERY:
- Task completion (success or failure)
- Strategic decision by Optimus
- Escalation between agents
- Skill deployment or update
- Infrastructure change
- External communication (via Neo)
- Research output delivery
- Cost tier override or exception

## Log Location

Logs are appended to the daily log file:
`/operations-logs/YYYY-MM-DD.jsonl`

Each line is a valid JSON object. One entry per line (JSON Lines format).

## Example Entry

```json
{"timestamp":"2026-03-17T14:30:00Z","agent":"alpha","pillar":"CORE,SOCIAL","value_chain_stage":"MARKETING","task_summary":"Created 3 faceless content posts for test channels","outcome":"COMPLETED","cost_tier":"OPERATIONAL","model_used":"grok-4-1-fast","duration_seconds":45,"tokens_used":3200,"work_order_ref":"","decision_log":"Used carousel format based on engagement data","escalated_to":"","blocker":""}
```

## Aggregation Rules (for Kitt OS Review)

Kitt's daily review aggregates these logs into:

1. **Activity by agent**: task count, completion rate, average duration per agent
2. **Activity by pillar**: which pillars are getting work, which are idle
3. **Value chain coverage**: are all 7 stages active? Where are the gaps?
4. **Cost analysis**: spend by tier, by agent, by pillar. Free tier utilisation %.
5. **Blocker summary**: all BLOCKED/PARTIAL entries surfaced with context
6. **Escalation patterns**: who escalates to whom, frequency, resolution time
7. **Decision audit**: all strategic decisions logged by Optimus with rationale

## Integration Points

| Consumer | What It Uses | Frequency |
|---|---|---|
| Kitt OS Review | Full daily aggregate | Daily |
| Boss Dashboard | Summary metrics by pillar | Real-time where possible |
| Optimus | Decision audit trail | On-demand |
| Oracle | Research output tracking | Per-consultation |
| Data | Cost/token analysis | Daily via cron |

## Validation Rules

Before accepting a log entry:
1. `pillar` must contain valid codes from value-chain-map.md
2. `value_chain_stage` must be exactly one valid stage code
3. `outcome` must be one of: COMPLETED, PARTIAL, BLOCKED, FAILED, ESCALATED
4. `cost_tier` must match tier-map.md definitions
5. `agent` must be a recognised agent ID
6. FUTURE pillars (PROPERTY, DEVELOPMENTS) may only appear with RESEARCH or ANALYSIS stages

## Bootstrapping

At system startup, each agent logs a `SYSTEM_START` entry:
```json
{"timestamp":"...","agent":"optimus","pillar":"INTERNAL","value_chain_stage":"DEVELOPMENT","task_summary":"SYSTEM_START: Optimus online","outcome":"COMPLETED","cost_tier":"OPERATIONAL","model_used":"grok-4-1-fast","duration_seconds":0,"tokens_used":0}
```

This creates a daily heartbeat confirming all agents are operational.
