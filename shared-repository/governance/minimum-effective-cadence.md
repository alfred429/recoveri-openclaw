# ALTIOR — Minimum Effective Operating Rhythm
**Author:** Optimus (CEO)
**Date:** 29 March 2026
**Status:** RECOMMENDATION — Pending Boss approval
**Input:** All four directors consulted

---

## Design Principle
Maximise Boss steering power. Minimise Boss time in meetings.
Based on director feedback: the #1 accelerator is **fast binary decisions**, not more meetings.

---

## The Rhythm

### 1. Daily Async Cycle (~10 min Boss time)

**08:00 UTC — Director cutoff**
Each director posts structured update to their working lane.

**09:00 UTC — Optimus daily brief**
Single synthesised message to Reports lane (Topic 2) containing:
- Priority status across all active work
- Any DECISION NEEDED items (with options + recommendation + impact of delay)
- Any BLOCKED items (with owner + what's needed)
- Velocity note (private to Boss/Neo/Optimus — not surfaced to team)

**Boss response — at his discretion**
- Respond only to DECISION NEEDED and BLOCKED items
- Target: <24hr turnaround on binary Go/No-Go decisions (this is the single biggest throughput multiplier the team identified)
- No response needed on items proceeding normally

### 2. Weekly Strategy Session (~30 min, can go async if nothing needs live)

**Standing attendees:** Boss, Neo, Optimus
**Directors:** joined only when their domain has an agenda item

**Agenda:**
1. Scoreboard delta (5 min) — what moved, what didn't
2. Decisions queue (10 min) — only items meeting Tier 1 escalation criteria
3. Quality gate status (5 min) — what's ready for Boss review
4. Priority refresh (5 min) — any shifts in pillar weighting or focus
5. Kill list (5 min) — explicitly stop low-value work

**Output:** Updated scoreboard + recorded decisions + kill confirmations
**Posted to:** Reports lane within 1 hour

**Cancellation rule:** If no Tier 1 decisions pending and scoreboard is green, session replaced by async confirmation from Optimus.

### 3. Quality Gate Reviews (Triggered, not scheduled)

**Trigger:** Director tags `QG REVIEW READY` in their working lane
**Scheduling:** Optimus offers Boss a slot within next available window
**Format:** Director presents deliverable → Boss critiques → Go/Adjust/Kill captured
**Duration:** 15 min max per review
**Output:** Verbatim Boss feedback + decision recorded in gate template

### 4. Live Escalation (Rare — <1x/week expected)

**Trigger conditions (any director can flag):**
- Cross-director conflict blocking delivery
- Ambiguous trade-off requiring Boss judgment
- Findings that materially change strategy
- High-risk approval (irreversible, security, external commitment)
- Unclear strategic intent affecting architecture or scope

**Format:** Director flags `LIVE DISCUSSION REQUESTED` with context. Boss offers slot or pushes to async.

---

## What This Means for Boss's Time

| Activity | Frequency | Boss Time |
|----------|-----------|-----------|
| Read daily brief | Daily | ~5 min |
| Respond to decisions | Daily | ~5 min |
| Weekly strategy session | Weekly | ~30 min |
| Quality gate reviews | As triggered | ~15 min each |
| Live escalations | <1x/week | ~10 min each |

**Total estimated:** ~1 hour/day in active weeks. ~30 min/day in steady-state.
**Meetings:** 1 recurring (weekly, cancellable). Everything else triggered.

---

## Decision Escalation Summary (from separate standard)

| Tier | Who Decides | Criteria |
|------|-------------|----------|
| **Boss** | Scope, spend, sequencing, risk, quality bar, external commitments, governance, personnel |
| **Optimus** | Task routing, intra-pillar priority, director coordination, process efficiency, meeting scheduling |
| **Directors** | Execution method, worker tasking, tool selection, internal quality, domain knowledge, iteration |

**Grey zone rule:** When in doubt, escalate one tier up.

---

## Key Director Requests Embedded

✅ Alpha: Fast visual/brief sign-offs (<24hr) — addressed by daily decision cycle
✅ Data: V1 scope boundaries + "experiment/internal/external" label — added to decision format
✅ Kitt: No recurring ops meetings, flag-based live escalation — adopted as standard
✅ Oracle: Clean decision framing (what question, what confidence, when to stop) — embedded in weekly priority refresh + explicit kill list

---

## Boss Steering Toolkit (6 high-leverage actions)

These are the actions that give Boss maximum control with minimum time:

1. **Fast Go/No-Go** — binary decisions on structured proposals (<24hr)
2. **Priority rank** — weekly refresh of what matters most
3. **Scope label** — "experiment / internal / external" on each active initiative
4. **Good enough definition** — per deliverable, what quality bar applies
5. **Kill list** — explicitly stop work that's not worth continuing
6. **Priority shift signal** — immediate async notification when direction changes

---

## Review
This rhythm is subject to adjustment after 2 weeks of operation.
If it creates drag, we simplify. If Boss needs more control, we add touchpoints.
The goal is minimum viable governance — not bureaucracy.
