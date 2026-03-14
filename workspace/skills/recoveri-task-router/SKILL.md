---
name: recoveri-task-router
version: 1.0
description: Cost-aware routing and governance for Recoveri board agents
trigger: "route|delegate|assign|board task|analysis request|who should handle"
tools: []
author: recoveri
---

# RECOVERI Task Router Skill

You have access to this skill to route tasks efficiently across the Recoveri board.
Read and apply these rules whenever you receive a task that may belong to another agent.

## ROUTING TABLE

Domain → Agent → Cost Tier

Research (deep, multi-source)
→ Oracle (Consultant)
→ HIGH

Research (quick lookups)
→ Alpha (CRO) or Data (CTO)
→ LOW

Technical analysis
→ Data (CTO)
→ LOW

Commercial analysis
→ Alpha (CRO)
→ LOW

Code writing
→ Data (CTO)
→ LOW

Code deployment
→ Data (CTO)
→ LOW

Workflow design
→ Kitt (COO)
→ LOW

Operations implementation
→ Kitt (COO)
→ LOW

Financial tracking
→ Kitt (COO acting CFO)
→ LOW

Security concerns
→ Kitt (COO acting CISO)
→ LOW

Legal questions
→ Optimus (CEO acting CLO)
→ MEDIUM

Compliance / AML
→ Optimus (CEO acting MLRO)
→ MEDIUM

Presentations
→ Alpha (CRO)
→ LOW

Content drafting
→ Alpha (CRO acting CMO)
→ LOW

Strategic decisions (Tier 2+)
→ Optimus (CEO)
→ MEDIUM

Board coordination
→ Jarvis (EA)
→ MEDIUM

Personal tasks for Boss
→ Alfred (EA Personal)
→ MEDIUM


## ORACLE GATEKEEPER RULES

Oracle is extremely expensive compared to DeepSeek agents.

Before routing ANY task to Oracle apply this checklist:

1. Can Data, Alpha, or Kitt solve it?  
   → If yes, do NOT use Oracle.

2. Does it require synthesis across 3 or more sources?  
   → If no, do NOT use Oracle.

3. Would an incorrect answer create financial or legal risk?  
   → If no, do NOT use Oracle.

4. Has Boss or Optimus explicitly requested Oracle?  
   → If no, do NOT use Oracle.


### Approved Oracle tasks

• Cross-platform market research  
• Complex probability / prediction analysis  
• Legal or regulatory interpretation  
• Strategic decisions with financial consequences


### Never send to Oracle

• Simple searches  
• Content writing  
• Status reports  
• Operational questions  
• Anything solvable in under ~200 tokens


## ESCALATION PATH

Tier 1  
Routine operational work  
→ Agent handles autonomously

Tier 2  
Strategy inside existing entity  
→ Agent completes work and informs Optimus via Jarvis

Tier 3  
Any spending or new initiative  
→ STOP and escalate to Boss via Jarvis

Tier 4  
Funds, legal, public statements  
→ HARD STOP and escalate immediately


## ROUTING PROTOCOL

When receiving a task outside your domain:

1. Identify correct agent using the routing table  
2. Respond:

"This is a [domain] task. Routing to [Agent] ([Role])."

3. Do NOT attempt the task yourself  
4. If unsure between two agents choose the lower-cost agent


## COST AWARENESS

DeepSeek agents  
(Data, Alpha, Kitt)

→ cheapest  
→ default for most work


Grok agents  
(Jarvis, Optimus)

→ strategic reasoning


Oracle  
→ extremely expensive  
→ use only under gatekeeper rules


Monthly target budget  
→ under $40 for the entire board
