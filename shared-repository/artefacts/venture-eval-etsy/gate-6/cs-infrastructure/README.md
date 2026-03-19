# Recoveri CS Infrastructure — Gate 6

**Sprint:** 9 | **Date:** 18 March 2026 | **Priority:** HIGH

---

## Overview

Ephemeral customer service responder pipeline for Recoveri's Etsy shop (RecoveriStudio). Categorises incoming customer messages, drafts template-based responses, logs tickets to JSONL, and escalates to Boss via Telegram when human review is needed.

**Flow:**
```
Etsy message → Gmail Watcher (VPS:18802) → Mac Mini bridge (Tailscale)
    → spawn cs-responder.py → categorise → draft → log → escalate? → terminate
```

---

## Architecture

| Component | Location | Status |
|---|---|---|
| Gmail Watcher (`gog` CLI) | VPS port 18802 | ✅ Running (spawned by openclaw-gateway) |
| VPS ↔ Mac Mini bridge | Tailscale hook | ✅ Active |
| CS Responder script | VPS: `/root/shared-repository/artefacts/venture-eval-etsy/gate-6/cs-infrastructure/` | ✅ Deployed |
| JSONL ticket log | VPS: `/root/shared-repository/data/customer-service/tickets.jsonl` | ✅ Active |
| Telegram escalation | Bot token in `.openclaw/.env` | ✅ Configured |
| Ollama/Qwen (fallback LLM) | VPS systemd service, port 11434 | ✅ Running |
| DeepSeek API (primary LLM) | `api.deepseek.com` | ✅ Configured (needs API key env var) |
| CS Skill 132 (templates) | VPS: `/root/shared-repository/skills/skill-132-cs-templates/` | ⏳ Awaiting Cowork |

---

## Files

| File | Purpose |
|---|---|
| `cs-responder.py` | Main ephemeral agent script — the pipeline |
| `cs-config.json` | All configuration (Golden Rule 1 — nothing hardcoded) |
| `README.md` | This documentation (Golden Rule 3) |

---

## Bucket Categorisation

| Bucket | Name | Escalate? |
|---|---|---|
| A | Order Status | No |
| B | Digital Download Issue | No |
| C | Product Question | No |
| D | Refund Request | **Yes** |
| E | Complaint / Dispute | **Yes** |
| F | Custom Request | No |
| G | Unmatched / Unknown | **Yes** |

Escalation triggers a Telegram alert to Boss with the full ticket, draft response, and a note requiring manual review before sending.

---

## Usage

### Basic run
```bash
python3 cs-responder.py \
  --message "I can't download my file" \
  --context '{"customer_name": "Sarah", "market": "UK", "order_id": "ETY-12345"}'
```

### Dry run (categorise and draft, no logging or escalation)
```bash
python3 cs-responder.py --dry-run \
  --message "I want a refund" \
  --context '{"customer_name": "John", "market": "US"}'
```

### Pipe from stdin (for webhook integration)
```bash
echo '{"message": "...", "context": {"customer_name": "Emma"}}' | python3 cs-responder.py --stdin
```

### Context fields
```json
{
  "customer_name": "Sarah",
  "market": "UK",
  "order_id": "ETY-12345",
  "product": "Party Planner Bundle",
  "etsy_conversation_id": "conv_abc123"
}
```

---

## Model Configuration

**Primary:** DeepSeek V3.2 (`deepseek-chat`) — cheap API, great for templated work
- Requires `DEEPSEEK_API_KEY` environment variable
- Cost: ~$0.28/$0.42 per million tokens (input/output)

**Fallback:** Qwen 2.5 3B on VPS Ollama — free, runs locally
- Ollama systemd service on VPS (port 11434)
- Model: `qwen2.5:7b` (Q4_K_M, 1.9GB)
- No API key needed

The script automatically falls back to Qwen if DeepSeek is unavailable.

---

## Constraints (Enforced)

1. **NEVER deviate from templates** — LLM personalises within template structure only
2. **NEVER promise refunds** — acknowledge and escalate (Bucket D/E)
3. **NEVER skip logging** — every message gets a JSONL ticket entry
4. **Language: en-GB only** (v1)
5. **Max response length:** 500 characters

---

## Telegram Escalation

- **Bot token:** From `TELEGRAM_BOT_TOKEN` env var
- **Chat IDs:** From `TELEGRAM_ESCALATION_CHAT_IDS` env var (comma-separated) or config defaults
- **Triggers:** Buckets D (Refund), E (Complaint), G (Unmatched)
- **Format:** Markdown message with ticket ID, bucket, customer details, original message, and draft response

---

## Ollama/Qwen on VPS

**Systemd service:** `/etc/systemd/system/ollama.service`

```bash
# Status
systemctl status ollama

# Restart
systemctl restart ollama

# Logs
journalctl -u ollama -f

# List models
curl http://localhost:11434/api/tags
```

**Previous issue:** Ollama was run manually (not systemd), causing orphan processes after gateway reloads. Now fixed with a proper systemd unit that auto-restarts.

---

## Dependencies on Other Work

| Dependency | Owner | Status |
|---|---|---|
| Skill 132 (CS templates, buckets, escalation triggers) | Cowork | ⏳ In progress |
| Gmail Watcher restart fix (JOB 3 from Sprint 7) | — | ⏳ Known issue |

When Skill 132 is deployed to `/root/shared-repository/skills/skill-132-cs-templates/SKILL.md`, the responder will automatically load it instead of the placeholder templates.

---

## JSONL Ticket Schema

Each line in `tickets.jsonl` is a JSON object:

```json
{
  "ticket_id": "CS-20260318-2711D931",
  "timestamp": "2026-03-18T21:17:50.760275+00:00",
  "customer_name": "Emma",
  "customer_message": "Original message text",
  "market": "UK",
  "order_id": "ETY-12345",
  "product": "Party Planner Bundle",
  "etsy_conversation_id": "",
  "bucket": "C",
  "bucket_name": "Product Question",
  "draft_response": "Drafted response text",
  "template_source": "placeholder-v1",
  "model_used": "deepseek",
  "escalated": false,
  "escalation_sent": false,
  "status": "drafted",
  "context": {}
}
```

**Status values:** `drafted` (ready to send), `escalated` (needs Boss review)

---

## Golden Rules Compliance

| Rule | How |
|---|---|
| 1. NEVER HARDCODE | All values in `cs-config.json`, API keys from env vars |
| 2. NEVER OVERWRITE WITHOUT REVIEWING | JSONL is append-only, templates loaded from skill file |
| 3. DOCUMENT EVERYTHING | This README, JSONL logging, stderr progress output |
| 4. NEVER LEAVE LOOSE ENDS | Unmatched messages (Bucket G) always escalate, Telegram alerts for risky buckets |
