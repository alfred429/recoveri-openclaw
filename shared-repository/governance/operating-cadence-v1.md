# ALTIOR — Formal Operating Cadence v1.0
**Author:** Optimus (CEO)
**Date:** 29 March 2026
**Status:** DRAFT — Pending director feedback + Boss approval

---

## Design Principle
Maximise Boss steering power. Minimise Boss time in meetings.
Every rhythm exists to surface decisions, not to share status that could be read.

---

## 1. Daily Async Standup

**Director cutoff:** 08:00 UTC daily
Each director posts to their working lane using the standard reporting template (see §6).

**Optimus synthesis:** 09:00 UTC daily
Single consolidated brief posted to Reports lane (Topic 2). Boss reads one message, not four.

**Boss response window:** At Boss's discretion
Respond only to items tagged `DECISION NEEDED` or `BLOCKED`. Everything else flows without input.

**Rules:**
- Directors who miss cutoff get a single prompt from Optimus at 08:15
- No update = assumed "continuing previous plan, no blockers"
- Optimus synthesis is factual, not editorial — Boss sees what directors reported, not Optimus's interpretation layered on top

---

## 2. Weekly Strategy Session

**Duration:** 30 minutes maximum
**Attendees:** Boss, Neo, Optimus (standing). Directors joined only when their domain is on agenda.
**Day/time:** To be set by Boss once unblocked

**Standing agenda:**
1. **Velocity review** (5 min) — Optimus presents scoreboard delta from last week
2. **Blockers & decisions** (10 min) — Only items that meet escalation criteria (see §3)
3. **Quality gate status** (5 min) — What's ready for Boss review, what's in progress
4. **Strategic steering** (10 min) — Boss direction, priority shifts, new inputs

**Output:** Updated scoreboard, unblocked items, any Go/Adjust/Kill decisions recorded.
**Posted to:** Reports lane within 1 hour of session end.

**Rules:**
- No item on agenda without a proposed action or decision
- No director attends unless they have an agenda item
- If nothing needs discussion, session is cancelled (replaced by async confirmation)

---

## 3. Quality Gate Reviews (Triggered)

**Trigger:** A process step or deliverable is ready for Boss critique
**Requested by:** Director via their working lane, tagged `QG REVIEW READY`
**Scheduled by:** Optimus, within Boss's next available window

**Format:**
- Director presents: what was done, how it was done, output sample
- Boss reviews: critique, feedback, pass/fail/iterate
- Optimus captures: Go / Adjust / Kill decision + specific feedback
- Director acts on feedback immediately

**Rules:**
- No quality gate review without a concrete deliverable to review
- Boss feedback is captured verbatim, not summarised by Optimus
- Outcome posted to relevant working lane within 30 minutes

---

## 4. Director-to-Director Sync (Optional)

Directors may coordinate directly in working lanes when cross-domain work requires it.
No Boss involvement unless it meets escalation criteria.
Optimus monitors for conflicts or scope creep.

---

## 5. Escalation Triggers

See Decision Escalation Standard (separate document).

---

## 6. Standard Reporting Template

### Director Daily Update
```
## [Director Name] — [Date]

### DONE
- [Completed item with evidence/link]

### DOING
- [Active work, expected next step]

### BLOCKED
- [What's blocked, why, what's needed to unblock]

### DECISION NEEDED
- [Specific decision required]
- [Options if applicable]
- [Recommendation]
- [Impact of delay]
```

### Rules:
- DECISION NEEDED must meet escalation criteria or it stays at director level
- BLOCKED must name the specific dependency
- DONE must reference output, not activity ("listed 3 products" not "worked on products")
- Maximum 5 items per section. If more, prioritise.

---

## 7. Go/Adjust/Kill Template

Used at every quality gate review and weekly strategy session decision point.

```
## DECISION: [Item name]

**Presented by:** [Director]
**Date:** [Date]
**Gate:** [Which quality gate or milestone]

### Summary
[One paragraph: what was done, what's the output]

### Evidence
[Links, data, samples — concrete proof]

### Recommendation
[Director's recommendation: Go / Adjust / Kill]

### Decision
☐ GO — Proceed as planned
☐ ADJUST — Proceed with changes: [specific changes]
☐ KILL — Stop. Reason: [reason]. Resources reallocated to: [where]

### Next Action
[Specific next step, owner, by when (milestone, not date)]

### Boss Notes
[Captured verbatim from Boss feedback]
```

---

## Review
This cadence is itself subject to review. If it creates drag instead of clarity, we adjust.
First review: after 2 weeks of operation.
