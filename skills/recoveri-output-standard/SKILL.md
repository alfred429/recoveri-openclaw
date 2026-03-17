# recoveri-output-standard

## Skill Metadata
- **Name:** recoveri-output-standard
- **Version:** 1.0
- **Author:** Boss (via Cowork)
- **Created:** 2026-03-16
- **Scope:** All agents producing deliverables
- **Trigger:** Any task that produces a report, analysis, recommendation, briefing, plan, or significant written output

---

## Purpose

This skill defines the Recoveri Output Standard — the minimum quality bar for any deliverable produced by any agent in the Recoveri enterprise system. If your output is going to Boss or to the Board channel, it meets this standard. No exceptions.

---

## When This Standard Applies

This standard applies when you are producing a **deliverable** — a standalone piece of work that will be read, reviewed, or acted upon. Examples:

- Reports, analyses, recommendations
- Briefings, summaries, status updates
- Plans, proposals, strategies
- Research findings, audit results
- Any output posted to the Recoveri Board channel

This standard does **NOT** apply to:
- Quick conversational replies in DM
- Acknowledgements ("understood", "task received")
- Internal agent-to-agent handoff messages
- Debug logs or diagnostic output

**Rule of thumb:** If it would embarrass you on a boardroom table, it's not ready.

---

## The Standard

### 1. Structure

Every deliverable MUST have:
- **Title** — clear, specific, not generic. "Q1 Commercial Pipeline Analysis" not "Report".
- **Date** — when it was produced.
- **Author** — which agent produced it and on whose authority.
- **Executive Summary** — 2-3 sentences at the top. Boss reads this first. If he stops here, he still knows the key takeaway.
- **Body** — organised with clear sections. Use headings. Use tables where data is tabular. Use bullet points only when listing discrete items, not as a substitute for prose.
- **Recommendations / Next Steps** — what should happen as a result of this work. Every deliverable should answer "so what?"

### 2. Formatting

- Professional tone throughout. No filler, no padding, no "as an AI" disclaimers.
- Numbers are formatted consistently (£1,250 not 1250, percentages to 1 decimal place).
- Tables are used for comparisons, timelines, and structured data — not buried in paragraphs.
- Code blocks only where code is genuinely relevant (configs, commands, scripts).
- No walls of text. Break it up. White space is your friend.

### 3. Quality Checks Before Submission

Before marking a deliverable as complete, verify:
- [ ] Executive summary present and accurate
- [ ] All claims supported by data or reasoning (no unsourced assertions)
- [ ] No stale references (check agent names, model names, tier labels against current state)
- [ ] No placeholder text left in ("TBD", "TODO", "INSERT HERE")
- [ ] Spelling and grammar clean
- [ ] Consistent formatting throughout (don't mix styles)
- [ ] Recommendations are actionable, not vague

### 4. Output Format — PDF

All deliverables MUST be converted to PDF before delivery. Not markdown. Not plain text. PDF.

**Why:** PDF is the professional standard. It preserves formatting, is universally readable, and signals that the work is finished — not a draft scribbled in a text editor.

**How:** Use the PDF generation tools available in your environment. If you cannot generate a PDF directly, produce clean markdown and flag it for conversion.

### 5. Delivery — Telegram Board Channel

All completed deliverables are posted to the **Recoveri Board** Telegram group channel. This is the official record of completed work.

**Posting format:**
```
📋 [DELIVERABLE TYPE] — [Title]
Author: [Agent Name] ([Role])
Requested by: [Who asked for this]
Date: [Production date]

[Executive Summary — 2-3 sentences]

📎 [PDF attached]
```

**Do NOT:**
- Post drafts to the Board channel
- Post without a PDF attachment
- Post without the executive summary in the message body
- Flood the channel with incremental updates (use DM for progress, Board for finished work)

---

## Escalation

If you cannot meet this standard for a given task (e.g., time pressure, missing data, tooling limitation), you MUST:
1. Flag the gap explicitly: "This deliverable does not meet full Recoveri Output Standard because [reason]"
2. State what's missing
3. Propose a timeline to bring it up to standard

Never silently ship substandard work.

---

## Examples

### Good Deliverable Header
```
# Recoveri — Weekly Commercial Pipeline Analysis
**Date:** 17 March 2026
**Author:** Alpha (CRO), on behalf of Optimus (CEO)
**Classification:** OPERATIONAL

## Executive Summary
Pipeline value increased 12% week-on-week to £34,200 across 8 active opportunities.
Two deals moved to proposal stage. One risk flag: the Meridian account has gone
silent for 9 days and needs re-engagement by Wednesday.
```

### Bad Deliverable Header
```
# Report
Here is the commercial update you asked for. We looked at the pipeline and
things are going well overall with some improvements...
```

---

## Integration with Value Chain

When producing deliverables, tag the value chain stage this work belongs to:

| Stage | Example Deliverable |
|-------|-------------------|
| RESEARCH | Market scan, competitor audit, data collection summary |
| ANALYSIS | Data analysis report, trend identification, pattern recognition |
| STRATEGY | Strategic recommendation, positioning paper, opportunity assessment |
| PROPOSITION | Value proposition draft, offer design, pricing analysis |
| DEVELOPMENT | Technical spec, build report, integration plan |
| MARKETING | Campaign brief, content plan, channel analysis |
| COMMERCIAL | Pipeline report, deal review, commercial forecast |

This tag goes in the deliverable metadata and in the Board channel post. It feeds into the value chain tracking system (Phase 1 — awareness layer).

---

*This skill is mandatory for all agents. It is not optional. It is not aspirational. It is the standard.*
