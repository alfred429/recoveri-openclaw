---
name: recoveri-oracle-gatekeeper
description: Governance checklist for routing tasks to Oracle (VPS Consultant). Use when any agent considers delegating to Oracle — enforces the mandatory checklist (can another agent handle it, does this require genuine multi-source synthesis or specialist depth, has Boss or Optimus explicitly approved Oracle involvement) before routing.
---

# Oracle Gatekeeper — Governance Rules

Read this skill BEFORE routing any task to Oracle (Consultant).

## Why This Exists
Oracle (VPS consultant-agent) runs on Grok 4.1-fast — same cost tier as other board agents.
This skill exists for governance, not cost control.
Oracle is a specialist role. Routing low-value tasks to Oracle dilutes its focus and creates noise.

## Mandatory Checklist (all must be YES to use Oracle)

1. Can Data, Alpha, Kitt, or Optimus handle this without specialist depth? — If YES, route to them instead.
2. Does this require synthesis across 3+ independent data sources, or specialist consulting depth? — If NO, do not use Oracle.
3. Does getting this wrong have significant business or financial consequences? — If NO, do not use Oracle.
4. Has Boss or Optimus explicitly requested Oracle? — If NO, use a board agent.

If ANY answer is NO — do not use Oracle. Route to the appropriate board agent.

## Approved Oracle Tasks
- Market research requiring trend analysis across multiple platforms and data sources
- Probability assessments requiring complex multi-factor reasoning
- UK regulatory analysis (FCA, GDPR) with business risk implications
- Strategic decisions where depth of analysis materially affects the outcome
- Research tasks routed from Mac Mini bridge (Atlas → Oracle hand-off for synthesis)

## Never Use Oracle For
- Simple web searches or fact lookups (use Data or Alpha)
- Content drafting or copywriting (use Alpha)
- Operational questions or status checks (use Kitt)
- Code writing or reviews (use Data)
- Anything answerable in under 200 tokens (use any board agent)
- Summarising single documents (use any board agent)

## Two-Pass Research Pattern
For complex research, use this approach:
1. First pass: Route to a board agent (Data or Alpha) for initial research and data gathering
2. Second pass: Only if synthesis is genuinely needed, route to Oracle with the gathered data
This produces better results than giving Oracle the raw research task.

## Mac Mini Bridge Pattern
For deep research at zero API cost:
1. Route to Mac Mini research centre via bridge (Atlas, Claude Code)
2. Atlas returns results via bridge
3. If synthesis or specialist review is needed: pass to Oracle for final analysis

## Cost Awareness
- All VPS agents (including Oracle): Grok 4.1-fast ~$0.20/$1.00 per 1M tokens
- Mac Mini (Atlas, Claude Code): $0.00 — zero API cost
- Monthly budget target: under $40 for all VPS agents combined
- Kitt (acting CFO) tracks daily API spend
