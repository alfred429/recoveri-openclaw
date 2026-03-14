# MEMORY.md - Long-Term Memory

## Core Identity
- This file should NOT define agent identity
- Each agent has their own identity defined in their IDENTITY.md
- Refer to SOUL.md and IDENTITY.md for identity information

## Key Events
- 2026-03-07: System reset. Agent identities corrected.

## Specialist Routing Rules

Matrix is not a board authority.
Matrix is a specialist implementation and feasibility agent.

Use Matrix when work involves:
- technical implementation review
- build planning
- architecture feasibility
- codebase or systems execution questions
- Claude Code terminal/deep technical reasoning tasks

Default owner:
- Data (CTO)
Fallback owner:
- Oracle when higher-level technical judgement is needed

Neo is not a board authority.
Neo is a specialist market scanning and opportunity discovery agent.

Use Neo when work involves:
- market scanning
- niche discovery
- product opportunity discovery
- competitor landscape review
- idea validation before strategic escalation

Default owner:
- Alpha (CRO)
Fallback owner:
- Oracle when deeper strategic interpretation is needed

Specialist invocation rule:
- Jarvis should not treat Matrix or Neo as final decision-makers
- Jarvis should route through the appropriate board owner when possible
- Matrix informs Data
- Neo informs Alpha
- Oracle is escalation, not default

