---
name: recoveri-task-router
version: 2.0
description: Routes tasks to the correct Recoveri board agent based on domain, cost tier, Oracle gatekeeper rules, and Mac Mini research centre access. Use when Neo or Optimus receives a task and needs to determine which agent should handle it.
trigger: "route|delegate|assign|board task|analysis request|who should handle|research request|mac mini|research centre"
---

# RECOVERI Task Router Skill v2.0

You have access to this skill to route tasks efficiently across the Recoveri board.
Read and apply these rules whenever you receive a task that may belong to another agent.

## INFRASTRUCTURE MAP

| Environment | Host | Agents | Models Available |
|-------------|------|--------|-----------------|
| VPS (recoveri-board-01) | Hetzner 16GB | Neo, Optimus, Data, Alpha, Kitt, Oracle | Grok 4.1-fast (primary), DeepSeek (fallback) |
| Mac Mini (research centre) | Local Mac Mini | Alfred (EA), research workers | Claude Code (terminal), ChatGPT 5 (browser) — zero API cost |

## BRIDGE STATUS CHECK

Before routing to Mac Mini, verify bridge is UP:
```
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18800/health
```
Expect 200. If not 200, fall back to VPS agents.

## ROUTING TABLE — VPS AGENTS

| Domain | Route To | Model Tier | Cost |
|--------|----------|-----------|------|
| Research (deep, multi-source) | Oracle (Consultant) | Grok 4.1-fast | MEDIUM |
| Research (quick lookups) | Alpha (CRO) or Data (CTO) | Grok 4.1-fast | MEDIUM |
| Technical analysis | Data (CTO) | Grok 4.1-fast | MEDIUM |
| Commercial analysis | Alpha (CRO) | Grok 4.1-fast | MEDIUM |
| Code writing | Data (CTO) | Grok 4.1-fast | MEDIUM |
| Code deployment | Data (CTO) | Grok 4.1-fast | MEDIUM |
| Workflow design | Kitt (COO) | Grok 4.1-fast | MEDIUM |
| Operations implementation | Kitt (COO) | Grok 4.1-fast | MEDIUM |
| Financial tracking | Kitt (COO, acting CFO) | Grok 4.1-fast | MEDIUM |
| Security concerns | Kitt (COO, acting CISO) | Grok 4.1-fast | MEDIUM |
| Legal questions | Optimus (CEO, acting CLO) | Grok 4.1-fast | MEDIUM |
| Compliance/AML | Optimus (CEO, acting MLRO) | Grok 4.1-fast | MEDIUM |
| Presentations | Alpha (CRO) | Grok 4.1-fast | MEDIUM |
| Content drafting | Alpha (CRO, acting CMO) | Grok 4.1-fast | MEDIUM |
| Strategic decisions (Tier 2+) | Optimus (CEO) | Grok 4.1-fast | MEDIUM |
| Board coordination | Neo (CoS) | Grok 4.1-fast | MEDIUM |

## ROUTING TABLE — MAC MINI RESEARCH CENTRE

| Domain | Route To | Model | Cost | Bridge Required |
|--------|----------|-------|------|----------------|
| Deep product research (conception stage) | Mac Mini via bridge | Claude Code | FREE | YES |
| Prototype development | Mac Mini via bridge | Claude Code | FREE | YES |
| Complex reasoning tasks | Mac Mini via bridge | ChatGPT 5 | FREE | YES |
| Market analysis (3+ sources) | Mac Mini via bridge | Claude Code | FREE | YES |
| Code architecture review | Mac Mini via bridge | Claude Code | FREE | YES |
| Personal tasks for Boss | Alfred (EA-Personal, Mac Mini) | Claude Code | FREE | YES |

### Mac Mini Routing Rules

1. Bridge check first: verify bridge UP before routing
2. Conception stage work: R&D, prototyping, conception stage prefer Mac Mini
3. Cost gate: route to Mac Mini when task would consume >500 tokens on paid API
4. Fair usage: max 5 concurrent research requests to Mac Mini
5. Response format: results returned as markdown via bridge

### When NOT to Route to Mac Mini

- Time-critical tasks requiring <30 second response
- Tasks requiring VPS-local file access or tools
- Simple queries answerable by VPS agents in <200 tokens
- When bridge status is DOWN or DEGRADED

## ORACLE GATEKEEPER RULES

Oracle runs on Grok 4.1-fast (same tier as other agents).
Oracle role remains as premium research and review consultant:

1. Governance Tier 3+ — after board has done full analysis
2. Security threat assessment — credible threat flagged
3. Final code review — before any release goes live

For deep multi-source research, prefer Mac Mini research centre (zero cost) over Oracle.

## ESCALATION PATH

Tier 1 (routine, zero spend): Agent handles autonomously, logs decision
Tier 2 (strategy within entity): Agent handles, notifies Optimus via Neo
Tier 3 (any spend, new initiatives): STOP — escalate to Boss via Neo
Tier 4 (funds, legal, public statements): HARD STOP — escalate to Boss immediately

## HOW TO ROUTE

1. Check if this is a research/conception task for Mac Mini
2. If Mac Mini: verify bridge status, then route via bridge
3. If VPS: identify correct agent from VPS routing table
4. Respond: "This is a [domain] task — routing to [Agent] ([Role]) for handling."
5. Do NOT attempt the task yourself if it belongs to another domain
6. If uncertain between two agents, route to lower cost tier
7. If uncertain between Mac Mini and VPS, prefer Mac Mini for research, VPS for execution

## COST AWARENESS

- Grok 4.1-fast (all VPS agents): ~$0.20/$1.00 per 1M tokens
- DeepSeek fallback: ~$0.28/$0.42 per 1M tokens
- Mac Mini (Claude Code, ChatGPT 5): $0.00 — zero API cost
- Monthly budget target: under $40 for all VPS agents combined

## ETSY PRODUCT WORKFLOW

| Domain | Route To | Notes |
|--------|----------|-------|
| Etsy research, listing copy, SEO tags | Alpha (CRO) | Read recoveri-etsy-workflow skill |
| Deep market research for Etsy | Mac Mini via bridge | Conception stage, use Claude Code |
| PDF/product creation, mockup images | Data (CTO) | Read recoveri-etsy-workflow skill |
| Product review email to Boss | Alpha (CRO) | Uses gog gmail send with attachments |
