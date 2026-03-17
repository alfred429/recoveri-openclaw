# Recoveri Operations Log — JSONL Schema
# Version: 1.0
# Created: 17 March 2026
# Source: recoveri-operations-log skill + Google Ecosystem Standards v1.1

## File Convention
- One file per day: `YYYY-MM-DD.jsonl`
- Location: `/root/operations-logs/`
- Retention: Indefinite (archive monthly to Drive 07_Operations if size grows)

## JSONL Record Schema

Each line is a valid JSON object with these fields:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| timestamp | string (ISO 8601) | YES | When the action occurred | "2026-03-17T09:15:00Z" |
| agent | string | YES | Agent ID from openclaw.json | "main", "ceo-agent", "cto-agent" |
| agent_name | string | YES | Human-readable agent name | "Neo", "Optimus", "Data" |
| pillar | string | YES | Pillar code(s) from value-chain-map | "CORE", "TRADERS", "INTERNAL" |
| value_chain_stage | string | YES | Stage from value chain | "RESEARCH", "ANALYSIS", "STRATEGY" |
| action | string | YES | What was done | "routed_task", "produced_report", "deployed_skill" |
| result | string | YES | Outcome | "success", "failure", "blocked", "delegated" |
| req_id | string | NO | Request reference if applicable | "REQ-20260317-001" |
| tokens_used | integer | NO | Token count for this action | 4500 |
| model | string | NO | Model used (from config, NOT hardcoded) | "xai/grok-4-1-fast" |
| duration_ms | integer | NO | Duration in milliseconds | 12500 |
| cost_estimate | float | NO | Estimated cost in GBP | 0.003 |
| tier | string | NO | Tier label from tier-map | "OPERATIONAL", "CRON_FREE" |
| details | string | NO | Free-text additional context | "Routed to Data for IT Security review" |

## Example Records

```jsonl
{"timestamp":"2026-03-17T09:00:00Z","agent":"main","agent_name":"Neo","pillar":"INTERNAL","value_chain_stage":"STRATEGY","action":"daily_briefing","result":"success","tokens_used":2100,"model":"xai/grok-4-1-fast","tier":"OPERATIONAL"}
{"timestamp":"2026-03-17T09:15:00Z","agent":"main","agent_name":"Neo","pillar":"CORE","value_chain_stage":"ANALYSIS","action":"routed_task","result":"delegated","req_id":"REQ-20260317-001","details":"Website audit request routed to Optimus with pillar hint CORE/ANALYSIS"}
```

## Querying

```bash
# All actions today
cat /root/operations-logs/$(date +%Y-%m-%d).jsonl

# Filter by agent
cat /root/operations-logs/2026-03-17.jsonl | jq 'select(.agent == "cto-agent")'

# Count actions per agent
cat /root/operations-logs/2026-03-17.jsonl | jq -r '.agent_name' | sort | uniq -c | sort -rn

# Total tokens today
cat /root/operations-logs/2026-03-17.jsonl | jq '.tokens_used // 0' | paste -sd+ | bc
```
