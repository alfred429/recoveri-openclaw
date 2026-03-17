# Recoveri Request Register — JSONL Schema
# Version: 1.0
# Created: 17 March 2026
# Source: recoveri-request-tagging skill + Google Ecosystem Standards v1.1

## File Convention
- One file per day: `YYYY-MM-DD.jsonl`
- Location: `/root/request-register/`

## JSONL Record Schema

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| req_id | string | YES | Unique request reference | "REQ-20260317-001" |
| timestamp | string (ISO 8601) | YES | When request was received | "2026-03-17T09:00:00Z" |
| source | string | YES | Where request came from | "telegram_dm", "cowork", "agent_generated" |
| summary | string | YES | Brief description | "Website audit for client X" |
| pillar | string | YES | Pillar code(s) | "CORE" |
| stage | string | YES | Value chain stage | "ANALYSIS" |
| priority | string | YES | URGENT / HIGH / STANDARD / LOW | "HIGH" |
| status | string | YES | Current status | "OPEN", "IN_PROGRESS", "BLOCKED", "COMPLETED" |
| assigned_agent | string | NO | Agent handling the request | "cto-agent" |
| assigned_agent_name | string | NO | Human-readable name | "Data" |
| completed_at | string (ISO 8601) | NO | When completed | "2026-03-17T14:30:00Z" |
| deliverable | string | NO | Link to output | "Drive: 03_Offers_and_Products/Core/audit_report.md" |
| blocked_reason | string | NO | Why it is blocked | "Waiting for Boss approval" |

## Example

```jsonl
{"req_id":"REQ-20260317-001","timestamp":"2026-03-17T09:00:00Z","source":"telegram_dm","summary":"Website audit for potential Core client","pillar":"CORE","stage":"ANALYSIS","priority":"HIGH","status":"OPEN","assigned_agent":"cto-agent","assigned_agent_name":"Data"}
```
