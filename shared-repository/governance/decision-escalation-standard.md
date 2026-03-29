# ALTIOR — Decision Escalation Standard v1.0
**Author:** Optimus (CEO)
**Date:** 29 March 2026
**Status:** DRAFT — Pending Boss approval

---

## Purpose
Clear decision rights stop both drift and bottlenecks.
Every person in the chain knows what they can decide, what they must escalate, and what they should never wait on.

---

## Three Tiers

### Tier 1: Boss Decides
Items that **must** come to Boss. No exceptions. No Optimus override.

| Category | Examples |
|----------|----------|
| **Scope change** | New pillar activation, venture launch/kill, adding a new agent |
| **Spend** | Any new recurring cost, any single spend >£50, provider changes |
| **Sequencing** | Changing which pillars are lead/support/dormant |
| **Risk** | Anything that could expose Altior legally, financially, or reputationally |
| **Quality bar** | Setting or changing the quality standard for any process |
| **External commitments** | Client promises, marketplace policy decisions, public statements |
| **Governance changes** | Constitution, operating model, authority chain modifications |
| **Personnel** | Adding/removing/modifying agents or their authority |

**Format:** DECISION NEEDED tag in daily update or direct escalation via Neo.
**Response expectation:** Boss responds when available. Team does not proceed until decision received.

---

### Tier 2: Optimus Decides
Items Optimus can resolve **without Boss approval**, but must **report** in the daily synthesis.

| Category | Examples |
|----------|----------|
| **Task routing** | Which director handles a piece of work |
| **Priority within a pillar** | Sequencing tasks within an approved priority |
| **Director coordination** | Resolving cross-domain dependencies |
| **Process efficiency** | Adjusting how work flows between agents (not what work is done) |
| **Deadline setting** | Internal milestone targets within approved scope |
| **Escalation triage** | Determining whether something meets Tier 1 criteria |
| **Meeting scheduling** | When quality gates or syncs happen |

**Constraint:** Optimus cannot change scope, spend, sequencing between pillars, risk posture, or quality bar. Those are always Tier 1.

**Reporting:** Included in daily synthesis. Boss can override retroactively.

---

### Tier 3: Directors Decide
Items directors handle **autonomously** within their domain. No waiting required.

| Category | Examples |
|----------|----------|
| **Execution method** | How to complete an approved task |
| **Worker tasking** | What to assign their worker, in what order |
| **Tool selection** | Which tools/approaches to use for approved work |
| **Internal quality** | Self-review before submitting for quality gate |
| **Domain knowledge** | Research, analysis, drafting within their scope |
| **Iteration** | Reworking their own output based on feedback |
| **Peer coordination** | Direct sync with another director on shared work |

**Constraint:** Directors cannot change scope, commit spend, alter sequencing, accept external risk, or lower quality bar. Those escalate.

**Reporting:** Included in daily standup. Optimus monitors for drift.

---

## Decision Routing Flowchart

```
Does it change SCOPE, SPEND, SEQUENCING, RISK, or QUALITY BAR?
  → YES → BOSS (Tier 1)
  → NO →
    Does it affect multiple directors or cross-domain coordination?
      → YES → OPTIMUS (Tier 2)
      → NO →
        Is it within one director's approved domain work?
          → YES → DIRECTOR (Tier 3)
          → NO → OPTIMUS (Tier 2) for triage
```

---

## Grey Zone Rule
When in doubt: escalate one tier up. Better to over-escalate than to make an unauthorised decision.
Optimus's job is to filter — not everything that reaches Optimus needs to reach Boss.

---

## Anti-Patterns

❌ Director waits 3 days for Boss to approve a tool choice → Should be Tier 3
❌ Optimus changes which pillar gets priority → Should be Tier 1
❌ Director commits to a delivery date with an external party → Should be Tier 1
❌ Optimus approves a new monthly subscription → Should be Tier 1
❌ Director asks Boss which keyword to use in a listing → Should be Tier 3

---

## Review
Subject to adjustment after first 2 weeks of operation.
Boss can reclassify any decision tier at any time.
