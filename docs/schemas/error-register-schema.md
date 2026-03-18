# Recoveri Error Register — JSONL Schema
# Version: 1.0
# Created: 18 March 2026
# Sprint: 7 | Item: 7.6
# Owner: Data (CTO) + Kitt (COO)
# Pattern: Same as operations-log and request-register

## File Convention
- One file per day: `YYYY-MM-DD.jsonl`
- Location: `/root/error-register/`
- Retention: Indefinite (review monthly, archive to Drive 08_Operations if size grows)

## JSONL Record Schema

Each line is a valid JSON object with these fields:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| err_id | string | YES | Unique error reference | "ERR-20260317-001" |
| timestamp | string (ISO 8601) | YES | When the error occurred | "2026-03-17T14:30:00Z" |
| agent | string | YES | Agent ID from openclaw.json | "cro-agent" |
| agent_name | string | YES | Human-readable name | "Alpha" |
| model | string | NO | Model in use when error occurred | "xai/grok-4-1-fast" |
| error_type | string | YES | Category | "api_error", "tool_error", "routing_error", "fabrication", "timeout", "config_error" |
| error_code | string | NO | API/system error code if available | "403", "ECONNREFUSED", "ANNOUNCE_TIMEOUT" |
| message | string | YES | Human-readable error description | "Grok returned 403 when attempting image generation" |
| severity | string | YES | Impact level | "CRITICAL", "HIGH", "MEDIUM", "LOW" |
| context | string | NO | What the agent was trying to do | "Alpha attempted to generate product thumbnail via Grok" |
| resolution | string | NO | How it was fixed (if fixed) | "Known limitation — Grok does not support image generation." |
| resolved | boolean | YES | Whether the error has been resolved | true, false |
| process_id | string | NO | If error occurred during a governed process | "venture-eval-etsy" |
| gate_id | string | NO | If error occurred at a specific gate | "gate-1" |
| req_id | string | NO | Associated request if applicable | "REQ-20260317-005" |

## Error Types

| Type | Description | Typical Severity |
|------|-------------|-----------------|
| api_error | API returned non-200 response | HIGH |
| tool_error | OpenClaw tool execution failed | MEDIUM-HIGH |
| routing_error | Task routed to wrong agent or failed to route | HIGH |
| fabrication | Agent fabricated output instead of executing | CRITICAL |
| timeout | Announce timeout, gateway timeout, session timeout | MEDIUM |
| config_error | Configuration issue preventing execution | HIGH |
| session_drift | Agent behaviour degraded due to context pruning | HIGH |
| permission_error | Agent attempted action outside its authority | MEDIUM |

## Querying

```bash
# All errors today
cat /root/error-register/$(date +%Y-%m-%d).jsonl | jq '.'

# Unresolved errors
cat /root/error-register/*.jsonl | jq 'select(.resolved == false)'

# Errors by severity
cat /root/error-register/*.jsonl | jq 'select(.severity == "CRITICAL")'

# Error count by type
cat /root/error-register/*.jsonl | jq -r '.error_type' | sort | uniq -c | sort -rn
```
