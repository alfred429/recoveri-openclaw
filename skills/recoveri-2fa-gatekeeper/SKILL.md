---
name: recoveri-2fa-gatekeeper
description: internal recoveri skill for step-up approval and two-factor gating of protected actions. use when jarvis or another recoveri agent needs to gate a sensitive action behind a one-time approval challenge, deliver a 4-digit code to boss via telegram dm and email, verify the approval response, bind approval to the exact action, enforce expiry and retry limits, and write audit events.
---

# recoveri 2fa gatekeeper v0.1

Implement step-up approval for protected Recoveri actions.

## Core rules

- Treat this skill as an internal control skill.
- Generate a fresh random 4-digit code for every protected action.
- Never use a fixed password.
- Allow only one active challenge at a time.
- Bind each challenge to the exact action under review.
- Bind each challenge to the requester channel, requester session, and requester agent.
- Expire each challenge after 5 minutes.
- Allow at most 3 verification attempts.
- Cancel or reject any new protected request while one challenge is active.
- Deliver the challenge code to Boss via:
  - Telegram DM
  - Email: mike@recoveri.io
- Accept approval input only in webchat for v0.1.
- Approval format must be:
  - 007-<challenge_id>-<code>
  - example: 007-A1-4826
- Write audit events for create, verify-success, verify-fail, expire, and cancel.

## Runtime files

Use these exact runtime files:

- State:
  `/root/.openclaw/workspaces/main/shared/approval-state.json`
- Audit log:
  `/root/.openclaw/workspaces/main/shared/APPROVAL_EVENTS.jsonl`

## Direct / step-up / blocked intent

Use this skill only for step-up actions, such as:

- config changes
- SOUL or governance file edits
- elevated exec
- gateway restart
- cron create, edit, delete
- approval policy changes

Do not use this skill for direct actions such as routine reports, audits, RB posts, memory search, or normal workspace reads.

Do not approve blocked actions such as self-amendment of core authority or self-replication if doctrine forbids them.

## Required state fields

Persist challenge state with at least:

- challenge_id
- code
- action_summary
- action_hash
- requester_channel
- requester_session
- requester_agent
- delivery_channels
- created_at
- expires_at
- retry_count
- max_retries
- status

## Required audit event fields

Append JSONL events with at least:

- timestamp
- event_type
- challenge_id
- action_summary
- action_hash
- requester_channel
- requester_session
- requester_agent
- delivery_channels
- result
- retry_count

## Execution flow

### 1. Create challenge

When a step-up action is requested:

- Refuse if a live challenge already exists.
- Generate:
  - short challenge id
  - random 4-digit code
  - action hash
- Save state.
- Write create event.
- Return a delivery payload for Telegram and email.

### 2. Deliver challenge

Delivery message format:

Recoveri Security Approval Required

Action: <action_summary>
Challenge: <challenge_id>
Code: <code>
Expires: 5 minutes

Approve in webchat using:
007-<challenge_id>-<code>

### 3. Verify approval

When Boss replies in webchat:

- Parse `007-<challenge_id>-<code>`
- Verify:
  - challenge exists
  - challenge id matches
  - code matches
  - not expired
  - retry count below max
  - action hash still matches pending action
  - requester context still matches stored state
- On success:
  - mark approved
  - write verify-success event
  - clear active challenge
  - return approved
- On failure:
  - increment retry_count
  - write verify-fail event
  - return denied or expired or retry-limit-reached

### 4. Expiry

If current time exceeds expires_at:

- mark expired
- write expire event
- clear active challenge
- return expired

## Implementation notes

Use the script in `scripts/approval_gate.py` for deterministic state handling.

Keep responses short and structured for agent use.

