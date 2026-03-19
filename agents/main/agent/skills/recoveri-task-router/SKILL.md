---
name: recoveri-task-router
version: 4.1
description: Routes tasks to the correct Recoveri agent based on domain and tier. Defines the flat dispatch model, announce chain result delivery protocol, and Drive-linked deliverable requirements.
trigger: "route|delegate|assign|board task|analysis request|who should handle|research request|mac mini|research centre|report result|post result"
---
# RECOVERI Task Router Skill v4.1
## AGENT ID MAP (MANDATORY — use exact values in sessions_spawn agentId param)
| Persona | agentId for sessions_spawn |
|---------|---------------------------|
| Neo (CoS) | `main` |
| Optimus (CEO) | `ceo-agent` |
| Data (CTO) | `cto-agent` |
| Alpha (CRO) | `cro-agent` |
| Kitt (COO) | `coo-agent` |
| Oracle (CC) | `consultant-agent` |

> **CRITICAL**: Never use persona names (neo, optimus, data, alpha, kitt, oracle) as agentId.
> The system will silently fail with "Unknown agent id". Always use the exact ID from the table above.

## GOLDEN RULES (apply to ALL work)
1. Never hardcode
2. Never overwrite without reviewing original — READ before WRITE
3. Document everything
4. Never leave loose ends
You have access to this skill to route tasks efficiently across the Recoveri board and to report results correctly.
Read and apply these rules whenever you receive a task OR complete a task.
## DESIGN PRINCIPLE
This skill defines ROUTING LOGIC and RESULT DELIVERY.
Model assignments, fallbacks, and costs are managed by openclaw.json config.
Tier-to-model mapping is in /root/.openclaw/config/tier-map.md.
Never assume a specific model. Always route by DOMAIN and TIER LABEL.
## DISPATCH MODEL (how tasks flow down)
Boss → Neo (intake + REQ-ID) → Optimus (orchestrator)
  ├── C-Levels (strategic tasks, quality review, domain expertise)
  └── Workers (defined tasks, bulk execution, CRON jobs)
Neo can route directly to C-Levels for routine domain queries.
Optimus dispatches to both C-Levels and workers.
Workers are leaf nodes — they execute and report, never delegate.
Optimus decides whether a task needs a C-Level (judgement required) or a worker (defined task, no thinking).
## RESULT DELIVERY (how results flow up)
Results are delivered through the announce chain. Each agent announces their result to the chain, which propagates it up to the board channel.
### Every result MUST include:
REQ-ID: REQ-YYYYMMDD-NNN
Agent: [your name and role]
Task: [one-line summary]
Status: DONE | FAILED | BLOCKED
[Result content]
Evidence:
- Command: [exact gog/shell command run]
- Output: [raw command output — copy/paste, not paraphrased]
- Drive link: [real URL from gog output — NEVER constructed from memory]
### Result rules:
1. No simulated responses. If you did not run the command, say so. If the command failed, report the exact error.
2. No fabricated Drive links. Run gog drive info <filename> to get the real file ID. A URL with [ID] or a made-up hash is a FAILURE.
3. No claiming completion without evidence. "File created" without a Drive link = NOT DONE. "Email sent" without gog output = NOT DONE.
4. If blocked, say so. Status: BLOCKED with the reason is better than a fake DONE.
Neo logs all results that appear on the board channel. Optimus reviews asynchronously and flags quality issues but does NOT gate delivery.
## ROUTING TABLE — WHO HANDLES WHAT
### C-Level Routing (strategic, judgement-required tasks)
Domain → Route To:
- Technical analysis, architecture decisions → Data (CTO)
- Code deployment, infrastructure changes → Data (CTO)
- Security concerns, security review → Data (CTO) + Kitt (COO)
- Commercial analysis, revenue strategy → Alpha (CRO)
- Content strategy, brand decisions → Alpha (CRO)
- Presentations, pitch decks → Alpha (CRO)
- Workflow design, process improvement → Kitt (COO)
- Operations implementation → Kitt (COO)
- Financial tracking, budgets → Kitt (COO, acting CFO)
- Deep research (multi-source) → Oracle (CC) → Mac Mini workers
- Regulatory analysis, advisory → Oracle (CC)
- Legal questions → Optimus (CEO, acting CLO)
- Compliance/AML → Optimus (CEO, acting MLRO)
- Strategic decisions → Optimus (CEO)
- Board coordination → Neo (CoS)
### Worker Routing (defined tasks, no strategic judgement needed)
Task Type → Route To → Tier:
- OS Review, cron monitoring, log processing → Charly (qwen-ops) → CRON_FREE
- Bulk research, document summarisation → Pat (qwen-research) → CRON_FREE
- Content drafts, listing copy, SEO tags → Shaz (qwen-content) → CRON_FREE
- Document OCR, image processing → Ray (qwen-vision) → VISION_FREE
- Code generation, script writing → Z (qwen-code) → CRON_FREE
- Large document ingestion (1M ctx) → Tye (qwen-longctx) → LONGCTX_FREE
- Complex reasoning, chain-of-thought → Dan (deepseek-reason) → ECONOMY
- Prototyping, code review (async OK) → mac-worker (Oracle bridge) → LOCAL_FREE
### Routing Decision Logic
When Optimus receives a task:
1. Does this need strategic judgement? → Route to C-Level
2. Is this a well-defined, repeatable task? → Route to worker
3. Can Oracle handle this on Mac Mini for free? → Route to Oracle (check bridge first)
4. Is this a scheduled/background task? → Route to CRON_FREE worker
5. Unsure? → Route to C-Level (safer to over-qualify than under-qualify)
## GOOGLE DRIVE DELIVERABLE REQUIREMENTS
When any task produces a file or document:
1. Create the file using gog CLI — gog drive upload or gog drive create
2. Store in the correct folder per the Drive folder map:
   - 00_Governance: Constitution, frameworks, policies
   - 01_Sprints: Sprint backlogs, closeouts
   - 02_Architecture: System design, technical architecture
   - 03_Offers_and_Products: Product content, listings, value props
   - 04_Research: Market research, intelligence briefs
   - 05_Finance: Financial models, budgets
   - 06_Experiments: Prototypes, test results
   - 07_Content: Marketing, social media, brand
   - 08_Operations: Process docs, SOPs
   - 09_Security: Security reviews, audits
   - 10_People: Team config, agent SOULs
   - 77_Templates: Reusable templates
   - 99_CEO: Boss curated folder
3. Get the real Drive link — run gog drive info <filename> and include the URL in your result
4. Never fabricate a URL — if you do not have the real file ID, your task is NOT DONE
## ROUTING TABLE — MAC MINI (via Oracle)
- Deep product research (conception stage) → Oracle → Mac Mini workers (FREE, bridge required)
- Prototype development → Oracle → Mac Mini workers (FREE, bridge required)
- Complex reasoning tasks → Oracle → Mac Mini workers (FREE, bridge required)
- Market analysis (3+ sources) → Oracle → Mac Mini workers (FREE, bridge required)
- Code architecture review → Oracle → Mac Mini workers (FREE, bridge required)
- Personal tasks for Boss → Alfred (EA-Personal, Mac Mini) (FREE, bridge required)
### Mac Mini Routing Rules
1. Bridge check first: Oracle verifies bridge is UP (curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18800/health — expect 200). If DOWN, notify team and request VPS fallback.
2. Conception stage work: Any task tagged as R&D, prototyping, or conception stage should prefer Mac Mini.
3. Cost gate: Route to Mac Mini when the task would consume >500 tokens on a paid API and can tolerate async response.
4. Fair usage: Max 5 concurrent research requests to Mac Mini. Queue additional.
5. Response format: Mac Mini returns results as markdown files in the shared bridge workspace.
### When NOT to Route to Mac Mini
- Time-critical tasks requiring <30 second response
- Tasks requiring VPS-local file access or tools
- Simple queries answerable by VPS agents in <200 tokens
- When Oracle reports bridge status is DOWN or DEGRADED
## TIER LABELS (reference only — config defines actual models)
Tier 0 LOCAL_FREE: Mac Mini workers via Oracle bridge — zero cost, R&D/conception
Tier 0 CRON_FREE: Qwen free tier (1M tokens/day) — scheduled/background tasks
Tier 1 PREMIUM: Highest reasoning — reserved for future use
Tier 1.5 ELEVATED: Above operational — high-value analysis
Tier 2 OPERATIONAL: Standard working tier — all routine board agent work
Tier 3 ECONOMY: Sub-agents, fallback models
Current tier assignments: read /root/.openclaw/config/tier-map.md.
## ESCALATION PATH
Tier 1 (routine, zero spend): Agent handles autonomously, logs decision
Tier 2 (strategy within entity): Agent handles, notifies Optimus via Neo
Tier 3 (any spend, new initiatives): STOP — escalate to Boss via Neo
Tier 4 (funds, legal, public statements): HARD STOP — escalate to Boss immediately
## BRIDGE STATUS CODES
UP: Bridge operational, Mac Mini responsive → Route normally via Oracle
DEGRADED: Bridge connected but high latency (>5s) → Route only essential research
DOWN: Bridge unreachable → Oracle alerts team, fall back to VPS
QUEUED: Mac Mini at capacity (5 concurrent) → Queue request, notify requestor
## COST AWARENESS
Cost awareness is managed by openclaw.json config, /root/.openclaw/config/tier-map.md, and the model-router-governance skill.
Routing principles (tier-based, not model-specific):
- LOCAL_FREE / CRON_FREE = zero cost — prefer these paths first
- OPERATIONAL tier = standard — default for real-time domain work
- PREMIUM tier = most expensive — reserve for when budget allows
- Total monthly budget target: managed by governance — check current budget with Kitt
Never hardcode model prices in routing decisions. Prices change. Tiers are stable.
## ETSY PRODUCT WORKFLOW
- Etsy research, listing copy, SEO tags → Alpha (CRO) or Shaz (worker). Strategy = Alpha, bulk copy = Shaz
- Deep market research for Etsy → Oracle → Mac Mini workers. Conception stage, LOCAL_FREE
- PDF/product creation, mockup images → Data (CTO) or Ray (vision worker). Complex = Data, OCR/image = Ray
- Product review email to Boss → Alpha (CRO). Uses gog gmail draft with attachments
