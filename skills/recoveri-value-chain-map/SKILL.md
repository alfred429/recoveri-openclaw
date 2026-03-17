# Recoveri Value Chain & Pillar Map v1.0
# Loaded by all agents via SHARED_SOUL awareness. Referenced by operations-log skill.
# Updated: 17 March 2026

---

## Value Chain Stages

Every task, output, and decision maps to one of these stages. The chain is sequential
but agents may operate at multiple stages simultaneously.

| Stage | Code | Description | Primary Agents |
|---|---|---|---|
| Research | RESEARCH | Market intelligence, competitor analysis, data gathering, literature review | Oracle, Alpha, Data |
| Analysis | ANALYSIS | Pattern recognition, synthesis, feasibility assessment, risk evaluation | Oracle, Kitt, Data |
| Strategy | STRATEGY | Business case development, positioning, resource allocation, go/no-go | Optimus, Oracle |
| Proposition | PROPOSITION | Service/product design, pricing, packaging, value articulation | Alpha, Optimus |
| Development | DEVELOPMENT | Build, test, deploy — code, skills, workflows, infrastructure | Data, Kitt |
| Marketing | MARKETING | Content creation, distribution, audience building, brand execution | Alpha |
| Commercial | COMMERCIAL | Pipeline management, client engagement, revenue conversion, retention | Alpha |

## Strategic Pillars

Every operation maps to at least one pillar. Cross-pillar work is tagged with all applicable pillars.

| # | Pillar | Code | Focus | Status | Lead Agent |
|---|---|---|---|---|---|
| 1 | Core | CORE | Systems Lab — website rescue, AI audits, implementation sprints | ACTIVE | Alpha (revenue), Data (delivery) |
| 2 | Social | SOCIAL | Attention — faceless content, audience growth, engagement patterns | ACTIVE | Alpha |
| 3 | Studios | STUDIOS | Products — Etsy store, digital products, product-led growth | ACTIVE | Alpha (commercial), Data (pipeline) |
| 4 | Traders | TRADERS | Finance — traditional markets, prediction, arbitrage, DeFi, crypto security | ACTIVE | Oracle (research), Data (infrastructure) |
| 5 | Property | PROPERTY | Capital — real estate investment, asset acquisition, portfolio management | FUTURE | Optimus (governance) |
| 6 | Developments | DEVELOPMENTS | Autonomous Co — R&D, new company creation, Pillar 6 mandate | FUTURE | Optimus (authority) |

### Pillar Status Rules
- **ACTIVE**: Work is authorised. Agents may propose and execute projects within governance.
- **FUTURE**: Visible for awareness and planning only. No spend, no resource allocation.
  Activation requires Boss approval with defined milestones and KPIs.
  Initial 18 months: majority reinvestment in 4 ACTIVE pillars.

## Agent-to-Pillar Primary Mapping

| Agent | Primary Pillars | Value Chain Focus |
|---|---|---|
| Neo | All (routing awareness) | Intake routing with pillar + stage hints |
| Optimus | All strategic, Developments (owner) | STRATEGY, PROPOSITION |
| Data | Core, Studios, Traders | DEVELOPMENT, RESEARCH (technical) |
| Alpha | Core, Social, Studios | MARKETING, COMMERCIAL, PROPOSITION |
| Kitt | All (operational governance) | ANALYSIS (ops review), DEVELOPMENT (release pipeline) |
| Oracle | All (research), Traders, Developments | RESEARCH, ANALYSIS |

## Cross-Reference: Combined-Function Teams to Pillars

| Team | Pillars Served |
|---|---|
| Strategy & Governance | All — cross-cutting |
| Commercial & Growth | Core, Social, Studios |
| Operations & Enterprise | All — cross-cutting |
| Technology & Product | Core, Studios, Traders |
| Intelligence, Research & Analysis | All — cross-cutting, especially Traders, Developments |

## Tagging Rules

1. Every logged operation MUST include: `pillar` (1+ codes) and `value_chain_stage` (1 code).
2. Cross-pillar work uses comma-separated pillar codes: `CORE,TRADERS`.
3. Internal infrastructure work (not pillar-specific) uses pillar code `INTERNAL`.
4. FUTURE pillars may appear in RESEARCH and ANALYSIS stages only (planning ahead is permitted).
5. The operations-log skill enforces these tags on every entry.
