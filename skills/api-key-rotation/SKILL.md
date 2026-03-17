---
name: api-key-rotation
description: |
  Automated API key rotation lifecycle for the RECOVERI enterprise agent system. Manages a dynamic provider registry, executes key rotation on a 30-day cycle, and enforces governance tiers (auto-rotate, manual-generate, boss-only). Use this skill whenever key rotation is due, a new API provider needs to be added or removed from the rotation schedule, a provider's rotation method or status needs updating, or when checking rotation compliance across all configured providers. Also triggers for: reviewing which keys are overdue, onboarding a new API service, decommissioning a provider, investigating a key authentication failure, or any task involving credential lifecycle management for the RECOVERI system. If someone mentions "rotate", "API key", "credential", "provider config", or "key expiry" in the context of the RECOVERI agent infrastructure, use this skill.
---

# API Key Rotation Skill

## Purpose

This skill manages the full lifecycle of API credentials across the RECOVERI agent system. It reads from a dynamic provider configuration, determines which keys are due for rotation, executes the appropriate rotation method, validates that new keys work, and logs everything for Kitt's OS Review cycle. Keys designated as Boss-only (bank, VPS, OpenClaw) are never touched — the skill sends reminders only.

## Ownership and Governance

The rotation skill operates within the RECOVERI command chain:

- **Skill Owner:** Kitt (COO, acting CISO) — owns the rotation policy, schedules execution, accountable for operational security compliance
- **Executor:** Data (CTO) — performs the actual rotation actions (key generation, environment variable updates, service restarts). Data owns all technical security execution.
- **CISO Oversight:** Kitt (COO, acting CISO) — reviews rotation reports, approves policy changes, owns compliance posture
- **Escalation Path:** Failures escalate Data → Kitt → Optimus (CEO) → Boss
- **Boss-only keys** (bank, VPS, OpenClaw) route reminders directly to Boss. The skill never reads, modifies, or interacts with these credentials in any way.
- **Governance phase:** During PILOT phase, all rotations require Boss approval (see `model-router-governance` skill for phase rules). During POST-PILOT, routine rotations are pre-approved under Kitt's authority.

### Approval Tiers

| Action | Tier |
|---|---|
| Run rotation check (read-only scan) | Auto-execute |
| Rotate a key via provider API (`method: api`) | PILOT: Boss approval. POST-PILOT: Pre-approved (Kitt authority) |
| Flag a key for manual regeneration (`method: manual_gen`) | PILOT: Boss approval. POST-PILOT: Board-level (Optimus notified) |
| Send Boss-only reminder | Auto-execute (notification only) |
| Add/remove a provider from config | Board-level (Optimus approval) |
| Emergency revoke a compromised key | Auto-execute (circuit breaker) then report |
| Rollback to previous key after failed rotation | Auto-execute then report |

## Provider Configuration

The provider registry lives in a YAML config file, separate from the skill logic. This is the core of the dynamic design — adding or removing a provider means editing this file, not modifying the skill.

### Config Location

```
~/.recoveri/key-rotation/providers.yaml
```

### Config Schema

```yaml
# Provider Registry for API Key Rotation
# Edit this file to add/remove providers. The skill reads it at runtime.
# Changes to this file require Board-level approval (Optimus).

rotation_policy:
  cycle_days: 30              # Default rotation interval
  check_frequency: weekly     # How often the skill scans for due keys
  reminder_days_before: 7     # Send Boss reminder this many days before boss_only keys are due
  max_retry_attempts: 3       # Retries before marking rotation as failed
  rollback_on_failure: true   # Auto-revert to previous key if new key fails validation

providers:
  xai:
    display_name: "xAI (Grok)"
    rotation: auto
    method: api
    api_endpoint: "https://api.x.ai/v1/api-keys/rotate"
    response_key_field: "api_key"         # JSON field in rotation response containing the new key
    auth_scheme:                          # How this provider authenticates requests
      type: bearer                        # bearer | header | query | url_embed
    env_var: XAI_API_KEY
    environment: mac
    cycle_days: 30
    last_rotated: "2026-03-15"
    previous_key_backup: true
    validation:
      test_endpoint: "https://api.x.ai/v1/models"
      test_method: GET
      expected_status: 200
      auth_scheme:
        type: bearer
    tags: [active, primary-llm]

  deepseek:
    display_name: "DeepSeek"
    rotation: auto
    method: manual_gen
    dashboard_url: "https://platform.deepseek.com/api-keys"
    auth_scheme:
      type: bearer
    env_var: DEEPSEEK_API_KEY
    environment: mac
    last_rotated: "2026-03-01"
    previous_key_backup: true
    validation:
      test_endpoint: "https://api.deepseek.com/v1/models"
      test_method: GET
      expected_status: 200
      auth_scheme:
        type: bearer
    tags: [active, fallback]

  qwen:
    display_name: "Qwen"
    rotation: auto
    method: api
    api_endpoint: "https://dashscope.aliyuncs.com/api/v1/api-keys/rotate"
    response_key_field: "api_key"
    auth_scheme:
      type: header                        # Custom header name
      header_name: "Authorization"
      header_template: "Bearer {key}"     # Template — {key} replaced at runtime
    env_var: QWEN_API_KEY
    environment: mac
    last_rotated: "2026-03-10"
    previous_key_backup: true
    validation:
      test_endpoint: "https://dashscope.aliyuncs.com/api/v1/models"
      test_method: GET
      expected_status: 200
      auth_scheme:
        type: header
        header_name: "Authorization"
        header_template: "Bearer {key}"
    tags: [active]

  web_search:
    display_name: "Web Search API"
    rotation: auto
    method: manual_gen
    dashboard_url: null
    auth_scheme:
      type: query                         # Key passed as URL query parameter
      param_name: "api_key"
    env_var: WEB_SEARCH_API_KEY
    environment: vps
    last_rotated: "2026-03-15"
    previous_key_backup: true
    validation: null
    tags: [active]

  telegram:
    display_name: "Telegram Bot"
    rotation: auto
    method: manual_gen
    dashboard_url: "https://t.me/BotFather"
    auth_scheme:
      type: url_embed                     # Key embedded in URL path
      url_template: "https://api.telegram.org/bot{key}"
    env_var: TELEGRAM_BOT_TOKEN
    environment: vps
    last_rotated: "2026-03-15"
    previous_key_backup: true
    validation:
      test_endpoint: "https://api.telegram.org/bot{key}/getMe"
      test_method: GET
      expected_status: 200
      auth_scheme:
        type: url_embed
    tags: [active, comms]

  # --- BOSS-ONLY: Reminder only, never touched ---

  openclaw:
    display_name: "OpenClaw Gateway"
    rotation: boss_only
    environment: vps
    last_rotated: "2026-03-15"
    cycle_days: 30
    tags: [infrastructure]
    note: "Boss rotates manually. Reminder only."

  vps_access:
    display_name: "VPS SSH/Access"
    rotation: boss_only
    environment: vps
    last_rotated: null
    cycle_days: 90            # Longer cycle for infrastructure keys
    tags: [infrastructure]
    note: "Boss manages directly. Includes SSH keys and VPS provider credentials."

  bank:
    display_name: "Banking Credentials"
    rotation: boss_only
    environment: n/a
    last_rotated: null
    cycle_days: 90
    tags: [financial]
    note: "Boss manages directly. Never accessed by any agent."
```

### Adding a New Provider

To add a provider, append a new entry to the `providers` section with all required fields. The minimum required fields are:

```yaml
  new_provider:
    display_name: "Human-readable name"
    rotation: auto | boss_only      # auto = system manages, boss_only = reminder only
    method: api | manual_gen        # only needed for rotation: auto
    env_var: ENV_VAR_NAME           # only needed for rotation: auto
    environment: vps | mac | both
    last_rotated: "YYYY-MM-DD"      # or null if never rotated
    auth_scheme:                    # REQUIRED for rotation: auto — how this provider authenticates
      type: bearer | header | query | url_embed
    tags: []
```

For `method: api`, also provide:
- `api_endpoint` — the rotation API URL
- `response_key_field` — the exact JSON field name in the API response that contains the new key (e.g., `"api_key"`, `"token"`, `"secret"`)

For `method: manual_gen`, provide `dashboard_url` if available.

#### Auth Scheme Types

Every `auto` provider must declare how it authenticates. The `auth_scheme` block tells the script exactly how to attach the key to requests — no guessing, no fallback chains.

| Type | Description | Required Fields | Example |
|---|---|---|---|
| `bearer` | Standard Bearer token in Authorization header | (none extra) | Most OpenAI-style APIs |
| `header` | Custom header with configurable name and format | `header_name`, `header_template` | APIs using `x-api-key` or custom auth headers |
| `query` | Key passed as a URL query parameter | `param_name` | APIs that authenticate via `?api_key=xxx` |
| `url_embed` | Key embedded directly in the URL path | `url_template` (with `{key}` placeholder) | Telegram bot API style |

The `auth_scheme` is defined at the provider level (for rotation API calls) and optionally inside `validation` (for test endpoint calls). If the validation block has no `auth_scheme`, it inherits from the provider level.

```yaml
  # Example: bearer auth (most common)
  auth_scheme:
    type: bearer

  # Example: custom header
  auth_scheme:
    type: header
    header_name: "x-api-key"
    header_template: "{key}"        # Just the raw key, no prefix

  # Example: query parameter
  auth_scheme:
    type: query
    param_name: "access_token"

  # Example: URL-embedded
  auth_scheme:
    type: url_embed
    url_template: "https://api.example.com/v1/{key}/resources"
```

Validation config is optional but strongly recommended — without it, the skill can't confirm new keys work.

Adding or removing a provider requires Board-level approval (Optimus). The skill validates the config schema on load and will reject malformed entries rather than silently ignoring them.

### Removing a Provider

Don't delete the entry — set `rotation: decommissioned` and add a `decommissioned_date`. This preserves the audit trail. The skill will skip decommissioned providers entirely but they remain in the log history.

```yaml
  old_provider:
    rotation: decommissioned
    decommissioned_date: "2026-04-15"
    # ... keep other fields for audit
```

## Rotation Execution Flow

When the skill runs (triggered by cron or manual invocation), it follows this sequence:

### 1. Load and Validate Config

Read `providers.yaml`. Validate schema — every `auto` provider must have `method`, `env_var`, and `environment`. Reject the run (don't silently skip) if any active provider has missing required fields. Log the validation result.

### 2. Determine What's Due

For each provider where `rotation` is `auto` or `boss_only`:

```
days_since_rotation = today - last_rotated
cycle = provider.cycle_days or rotation_policy.cycle_days

if rotation == "boss_only":
    if days_since_rotation >= (cycle - reminder_days_before):
        → queue Boss reminder
elif rotation == "auto":
    if days_since_rotation >= cycle:
        → queue for rotation
```

### 3. Execute Rotations (Auto Providers Only)

For each provider queued for rotation, the method determines the process:

**Method: `api`**
1. Back up current key (if `previous_key_backup: true`): store in `~/.recoveri/key-rotation/backups/{provider}_{date}.enc`
2. Call the provider's rotation API endpoint to generate a new key
3. Update the environment variable with the new key
4. Run validation (see step 4)
5. If validation passes: update `last_rotated` in config, log success
6. If validation fails: rollback to backed-up key, log failure, alert Data (CTO) for review

**Method: `manual_gen`**
1. The skill cannot generate the key itself — it creates a rotation request ticket
2. The ticket includes: provider name, dashboard URL (if configured), which env var to update, and a deadline
3. The ticket routes to the appropriate handler: if environment is `mac`, it goes to the Mac-side agent; if `vps`, it stays VPS-side
4. Once the new key is provided (either by an agent who accessed the dashboard, or by Boss), the skill picks up from step 3 of the `api` method: update env var, validate, log

The distinction matters because some providers don't offer programmatic key rotation. Rather than pretending they do or skipping them, the skill explicitly handles the human-in-the-loop case. As more providers add rotation APIs in the future, their method can be upgraded from `manual_gen` to `api` with a config change — no skill modification needed.

### 4. Validate New Keys

For each rotated key, if `validation` is configured:

```
auth = build_auth(validation.auth_scheme or provider.auth_scheme, new_key)

response = HTTP {test_method} to {test_endpoint}
            with auth applied per auth_scheme type:
              bearer  → Authorization: Bearer {key}
              header  → {header_name}: {header_template with {key} replaced}
              query   → ?{param_name}={key} appended to URL
              url_embed → {key} substituted into test_endpoint URL

if response.status == expected_status:
    → validation passed
else:
    → validation failed, trigger rollback
```

The same auth_scheme logic applies to rotation API calls. The script reads the provider's `auth_scheme` config to determine how to authenticate — it never guesses or falls back to defaults. If `auth_scheme` is missing for an `auto` provider, config validation rejects the entry at load time.

If `validation` is null (not configured), log a warning that the rotation was applied without verification. This should be treated as technical debt — Data (CTO) should add validation config as a follow-up.

### 5. Rollback on Failure

If a rotation fails validation and `rollback_on_failure` is `true`:

1. Restore the backed-up key to the environment variable
2. Validate the restored key works (it should — it was working before)
3. Log the rollback with full details: which provider, what failed, what was restored
4. Alert Kitt (owner) and Data (CTO) for investigation
5. If rollback also fails (backed-up key no longer works): escalate immediately to Optimus, then Boss. This is a service-impacting incident.

Retry logic: before triggering rollback, retry the validation up to `max_retry_attempts` times with a brief delay. Transient API errors (rate limits, timeouts) shouldn't trigger a rollback on first failure.

### 6. Send Boss-Only Reminders

For `boss_only` providers approaching their cycle deadline:

```
Subject: [RECOVERI] Key rotation reminder: {display_name}
Due: {cycle_days - days_since_rotation} days remaining
Last rotated: {last_rotated}
Note: {note}
Action required: Boss manual rotation
```

Reminders are informational only. The skill does not follow up, nag, or escalate if Boss doesn't act. Boss manages these keys on their own terms.

### 7. Log Everything

Every run produces a log entry in `~/.recoveri/key-rotation/logs/rotation-{date}.json`:

```json
{
  "run_date": "2026-04-15",
  "run_trigger": "cron",
  "providers_checked": 8,
  "rotations_executed": 2,
  "rotations_succeeded": 2,
  "rotations_failed": 0,
  "rollbacks_triggered": 0,
  "manual_gen_tickets_created": 1,
  "boss_reminders_sent": 1,
  "validation_warnings": 0,
  "details": [
    {
      "provider": "xai",
      "action": "rotated",
      "method": "api",
      "validation": "passed",
      "previous_key_age_days": 31
    },
    {
      "provider": "deepseek",
      "action": "ticket_created",
      "method": "manual_gen",
      "ticket_id": "ROT-2026-04-15-001"
    },
    {
      "provider": "openclaw",
      "action": "reminder_sent",
      "days_remaining": 5
    }
  ]
}
```

These logs feed into Kitt's OS Review cycle. Kitt should be tracking: rotation compliance rate (percentage of keys rotated on schedule), validation pass rate, rollback frequency, and mean key age across all auto providers.

## Cross-Machine Considerations

The RECOVERI system runs across a VPS and a Mac that are bridged via Tailscale. This affects key rotation:

- **VPS-side providers** (web_search, telegram, openclaw, vps_access): Rotation and env var updates happen directly on the VPS
- **Mac-side providers** (xai, deepseek, qwen): Rotation commands must cross the Tailscale bridge. Data issues the command; the bridge relays to Mac-side infrastructure
- **If the bridge is down:** VPS-side rotations proceed normally. Mac-side rotations queue until connectivity restores. The skill does not skip validation or force-deploy across a broken bridge. Queued rotations are retried on the next scheduled run.

When checking environment variables for Mac-side providers, the skill must reach across the bridge to read the Mac's environment — not the VPS's local env. A key that's set correctly on the VPS but not on the Mac (or vice versa) is a split-brain scenario that should be flagged immediately.

## Emergency: Compromised Key Response

If a key is suspected or confirmed compromised (detected by any agent, flagged by a monitoring system, or reported by Boss):

1. **Immediate revoke** — this is auto-execute tier regardless of the provider's normal approval level. Disable or rotate the key instantly.
2. **Validate the new/revoked state** — confirm the old key no longer authenticates
3. **Audit exposure** — check logs for when the key was last used, by which agent, for what purpose
4. **Alert chain** — Kitt → Optimus → Boss, with the audit trail attached
5. **Post-incident** — Data (CTO) reviews how the compromise occurred and recommends preventive measures

This overrides the normal approval workflow because speed matters more than process when a credential is compromised. Report everything after the fact.

## Cron Schedule

The rotation check runs on a weekly cron (sufficient to catch any 30-day cycle with margin):

```
# RECOVERI API Key Rotation Check
# Owner: Kitt (COO) | Executor: Data | Reviewer: Data (CTO)
0 7 * * 1    /usr/bin/recoveri-rotate --config ~/.recoveri/key-rotation/providers.yaml --log ~/.recoveri/key-rotation/logs/
```

Runs every Monday at 07:00 local time. This catches any key approaching or past its 30-day cycle. The daily security audit cron (owned by Neo) can also flag overdue rotations as a secondary check.

## Skill Registry Entry

This skill should be registered in the RECOVERI skill registry:

```yaml
skill_id: api-key-rotation-v1.1
skill_version: 0.1.1
owner_agent: Kitt (COO, acting CISO)
executor_agent: Data (CTO)
deployed_by: Data
approved_by: Optimus
approval_tier: PILOT=Boss approval, POST-PILOT=Pre-approved (check) / Board-level (config changes)
environment: both
status: Active
dependencies: [tailscale-bridge, env-manager, model-router-governance]
review_dimensions: [security_compliance, operational_continuity]
```

---

## CHANGELOG

| Version | Date | Change |
|---------|------|--------|
| 0.1.0 | 15 March 2026 | Initial deployment — 11 providers, cron active |
| 0.1.1 | 17 March 2026 | **EXECUTOR FIX** — Mozart→Data (CTO) as executor (Mozart merged into Optimus). Kitt confirmed as CISO owner. Added PILOT/POST-PILOT governance phase alignment with model-router-governance v2.1. Added dependency on model-router-governance. |
