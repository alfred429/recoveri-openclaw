# P1 Plan — Runtime Behaviour Fixes
# Source: Codex plan, G-approved
# Date: 2026-03-29
# Status: Approved — awaiting concrete work order

---

## Delivery Sequence

- **Phase A:** Inventory all router copies, TG delivery paths, systemd unit files
- **Phase B:** Patch task-router + TG targeting together
- **Phase C:** Live messaging tests
- **Phase D:** Clean secret-bearing unit files after runtime is stable

## 1. Task-Router Skill Update

**Goal:** Make routing canon match runtime authority.

**Scope:**
- Update live altior-task-router copies:
  - Neo routes to Optimus
  - Optimus routes to directors
  - Directors spawn their own workers
  - Workers report back to their supervisor
- Remove any "Optimus is sole worker spawner" language
- Keep openclaw.json as enforcement, skill as behaviour guidance only

**Check before edit:**
- Find every live router copy still loaded or synced
- Confirm governance-sync will not reintroduce stale router text

**Acceptance:**
- No live router copy says Optimus owns worker spawning
- Director -> worker ownership matches runtime config exactly
- One request path documented consistently end-to-end

**Risk:** If only one router copy is updated, drift returns immediately.

## 2. TG Outbound Topic Targeting

**Goal:** Replies return to the originating topic, not General.

**Scope:**
- Trace where topic selection is decided:
  - Router skill
  - AGENTS/TG procedure
  - Gateway delivery logic / --deliver --reply-to usage
  - Any cron/helpers that post directly
- Make outbound replies preserve source topic/thread unless explicitly overridden

**Test cases:**
- Boss posts in a director topic -> reply lands in same topic
- Director-triggered worker result -> supervisor reply lands in correct topic
- General/default topic still works for non-threaded traffic

**Acceptance:**
- Source-topic reply routing works for Neo, Optimus, directors
- No regression for direct Telegram API scripts

**Risk:** Some posts may bypass OpenClaw and use raw TG API — fix may need more than one layer.

## 3. Gateway Inline Secrets Cleanup

**Goal:** Remove secrets from retired user unit, leave one clean service path.

**Scope:**
- Archive or remove old user-scope unit containing inline Environment= secrets
- Move required gateway env to a dedicated root-readable env file
- Ensure only active system unit is authoritative

**Acceptance:**
- No live or dormant unit file contains plaintext secrets
- System unit still restarts cleanly
- No user-scope watcher/service can respawn and conflict

**Risk:** Cleaning wrong unit without checking lingering/default.target links can recreate watcher conflict.

## Definition of Done

- Router canon matches openclaw.json
- Topic replies stay in originating topic
- Only one gateway service path exists
- No plaintext secrets in obsolete unit files
- Governance-sync cannot roll back any of the above

## UAT Model

Alfred (Matrix terminal) UATs each phase before Codex deploys next phase.
