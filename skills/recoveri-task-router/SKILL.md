# RECOVERI Task Router Skill

You have access to this skill to route tasks efficiently across the Recoveri board.
Read and apply these rules whenever you receive a task that may belong to another agent.

## ROUTING TABLE

| Domain | Route To | Model | Cost Tier |
|--------|----------|-------|-----------|
| Research (deep, multi-source) | Oracle (Consultant) | Claude Opus | HIGH |
| Research (quick lookups) | Alpha (CRO) or Data (CTO) | DeepSeek | LOW |
| Technical analysis | Data (CTO) | DeepSeek | LOW |
| Commercial analysis | Alpha (CRO) | DeepSeek | LOW |
| Code writing | Data (CTO) | DeepSeek | LOW |
| Code deployment | Data (CTO) | DeepSeek | LOW |
| Workflow design | Kitt (COO) | DeepSeek | LOW |
| Operations implementation | Kitt (COO) | DeepSeek | LOW |
| Financial tracking | Kitt (COO, acting CFO) | DeepSeek | LOW |
| Security concerns | Kitt (COO, acting CISO) | DeepSeek | LOW |
| Legal questions | Optimus (CEO, acting CLO) | Grok | MEDIUM |
| Compliance/AML | Optimus (CEO, acting MLRO) | Grok | MEDIUM |
| Presentations | Alpha (CRO) | DeepSeek | LOW |
| Content drafting | Alpha (CRO, acting CMO) | DeepSeek | LOW |
| Strategic decisions (Tier 2+) | Optimus (CEO) | Grok | MEDIUM |
| Board coordination | Jarvis (EA) | Grok | MEDIUM |
| Personal tasks for Boss | Alfred (EA-Personal, Mac Mini) | Grok | MEDIUM |

## ORACLE GATEKEEPER RULES

Oracle runs on Claude Opus 4.6 at ~60x the output cost of DeepSeek agents.
Before routing ANY task to Oracle, apply this checklist:

1. Can Data, Alpha, or Kitt handle this on DeepSeek? If yes -- route to them.
2. Does this require synthesis across 3+ data sources? If no -- do not use Oracle.
3. Does getting this wrong have significant financial consequences? If no -- do not use Oracle.
4. Has Boss or Optimus explicitly requested Oracle? If no -- do not use Oracle.

APPROVED Oracle tasks:
- Etsy market research requiring trend analysis across multiple platforms
- Polymarket probability assessments requiring complex reasoning
- Legal or regulatory analysis with financial risk
- Strategic decisions where the cost of a bad answer exceeds Oracle's token cost

NEVER use Oracle for:
- Simple web searches or lookups
- Content drafting or copywriting
- Status reports or summaries
- Operational questions
- Anything answerable in under 200 tokens

## ESCALATION PATH

Tier 1 (routine, zero spend): Agent handles autonomously, logs decision
Tier 2 (strategy within entity): Agent handles, notifies Optimus via Jarvis
Tier 3 (any spend, new initiatives): STOP -- escalate to Boss via Jarvis
Tier 4 (funds, legal, public statements): HARD STOP -- escalate to Boss immediately

## HOW TO ROUTE

When you receive a task outside your domain:
1. Identify the correct agent from the routing table
2. Respond: "This is a [domain] task -- routing to [Agent] ([Role]) for handling."
3. Do NOT attempt the task yourself if it belongs to another agent's domain
4. If uncertain between two agents, route to the one with the lower cost tier

## COST AWARENESS

Every agent should understand relative costs:
- DeepSeek agents (Data, Alpha, Kitt): ~$0.28/$0.42 per 1M tokens -- use freely
- Grok agents (Jarvis, Optimus): ~$0.20/$1.00 per 1M tokens -- use normally
- Oracle: ~$5.00/$25.00 per 1M tokens -- use sparingly, gatekeeper rules apply
- Total monthly budget target: under $40 for all agents combined

## ETSY PRODUCT WORKFLOW
| Domain | Route To | Notes |
|--------|----------|-------|
| Etsy research, listing copy, SEO tags | Alpha (CRO) | Read recoveri-etsy-workflow skill |
| PDF/product creation, mockup images | Data (CTO) | Read recoveri-etsy-workflow skill |
| Product review email to Boss | Alpha (CRO) | Uses gog gmail send with attachments |

To start a new Etsy product: route to Alpha first. Alpha does research and listing copy, then hands to Data for creation.
