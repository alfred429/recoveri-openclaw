# Recoveri TG Board Posting — Skill Definition
# skill_id: recoveri-tg-board-posting
# version: 1.1
# owner: Optimus (CEO & Orchestrator) — posting authority
# contributors: All C-Level agents
# approval_tier: Tier 1 (auto-execute for status updates), Tier 2+ (document standard required)
# status: ACTIVE
# pillar: INTERNAL
# value_chain_stage: COMMERCIAL

---

## Purpose

Enable C-Level agents to post updates directly to the Recoveri Board TG channel for items they are solely responsible for. This eliminates the bottleneck of routing every update through Neo → Boss → manual post.

## Posting Tiers

### Tier 1 — Auto-Post (No Approval Needed)
C-Level agents can post directly to TG Board for:
- **Task completion reports** for tasks they own
- **Status updates** on assigned Sprint items
- **Daily/weekly metric summaries** from their domain
- **Research findings** tagged to their assigned pillars
- **Operational alerts** (system health, cost alerts, security notices)

**Format requirement:** All Tier 1 posts must use the TG Post Template (below).

### Tier 2 — Peer Approval + Board Document Required
These require Optimus sign-off AND a professionally formatted document before posting:
- **Strategic recommendations** (anything that could change direction)
- **Cross-pillar updates** (touching domains outside the agent's assignment)
- **External-facing content** (anything that might reach clients or partners)
- **Budget requests or cost escalations**

### Tier 3 — Board Approval + Board Document Required
These require Boss approval AND a professionally formatted document:
- **Governance changes** (tier reassignments, role changes)
- **New pillar or project proposals** (portfolio-level decisions)
- **Anything involving money, contracts, or commitments**

### Tier 4 — Boss Only + Board Document Required
- **Constitutional amendments**
- **Public announcements**
- **External partnerships or commitments**

---

## FORMAT STANDARDS

### Tier 1 — TG Post Template

All Tier 1 TG Board posts MUST use this format:

```
[PILLAR] [VALUE_CHAIN_STAGE] — [AGENT_NAME] ([ROLE])

[Update Title]

[2-4 sentence update body]

Status: [COMPLETED | IN PROGRESS | BLOCKED | FOR REVIEW]
Sprint Item: [6.X if applicable | N/A]
Next Action: [what happens next | none]

— [Agent Name] ([Role])
```

### Tier 2-4 — Recoveri Board Document Standard

**ALL Tier 2, 3, and 4 updates MUST be produced as professionally formatted PDF documents matching the Recoveri Board Document Standard.**

This is non-negotiable. The standard is defined by the Strategic Horizon Plan v3 and applies to all board-level communications. Recoveri outputs must exceed competitor quality in every dimension.

#### What This Means for Agents

When producing a Tier 2-4 update, the agent must:

1. **Draft the content** in structured markdown with all required sections (see Content Structure below)
2. **Route to Arthur** (Claude Code on Mac Mini) via the `recoveri-board-doc-formatter` skill for professional PDF formatting
3. **Arthur produces the PDF** matching Recoveri Board Document Standard
4. **PDF is posted/attached** to TG Board alongside a brief TG summary message

#### Content Structure for Tier 2-4 Drafts

Agents must provide their content in this structured format for Arthur to process:

```markdown
# DOCUMENT METADATA
- title: [Document Title]
- subtitle: [Optional Subtitle]
- classification: Internal — Recoveri Board
- author: [Agent Name] ([Role])
- date: [DD Month YYYY]
- version: v[X.Y]
- pillar: [PILLAR CODE]
- value_chain_stage: [STAGE]
- governance_tier: [T2 | T3 | T4]
- sprint_item: [6.X | N/A]

# EXECUTIVE SUMMARY
[2-3 paragraphs. What is this about, why does it matter, what's the recommendation.]

# SECTIONS
[Numbered sections with clear headings. Each section should contain:]
[- Prose paragraphs explaining the context and reasoning]
[- Tables where structured comparison or data is needed]
[- Bold key terms and italicised callout quotes where appropriate]

# RECOMMENDATIONS
[Numbered list of specific, actionable recommendations]

# NEXT ACTIONS
[What happens after this document is approved/reviewed]

# APPENDICES (if needed)
[Supporting data, detailed tables, reference material]
```

#### Recoveri Board Document Standard — Visual Specification

The PDF output must match these specifications:

**Header:**
- Top-left: "RECOVERI LTD" (bold, dark navy, 10pt)
- Top-right: "[Document Title] v[X.Y]" (grey, 10pt)

**Title Page:**
- "RECOVERI LTD" (bold, dark navy, 28pt)
- Document title (navy blue, 24pt)
- Subtitle (blue, 16pt)
- Classification line, Author line, Date line (10pt, grey)
- Italicised mission statement or key principle quote (12pt)

**Body:**
- Section numbers: "1. Section Title" (bold, dark navy, 18pt)
- Subsection numbers: "1.1 Subsection Title" (blue, 14pt)
- Body text: 11pt, left-aligned, generous line spacing
- Tables: dark navy header row with white text, alternating row shading, clean borders
- Bold key terms inline
- Italicised callout quotes for emphasis

**Footer:**
- Bottom-left: "Internal — Recoveri Board" (grey, 8pt)
- Bottom-right: "Page [N]" (grey, 8pt)

**General:**
- A4 page size
- Professional margins (25mm all sides)
- Clean whitespace — never cramped
- Page breaks between major sections

#### TG Summary for Tier 2-4

When posting a Tier 2-4 document to TG Board, include a brief TG message:

```
[PILLAR] [VALUE_CHAIN_STAGE] — [AGENT_NAME] ([ROLE])

📄 BOARD DOCUMENT: [Document Title] v[X.Y]

[1-2 sentence summary of what this document covers and its key recommendation]

Classification: Internal — Recoveri Board
Governance Tier: [T2 | T3 | T4]
Status: [FOR REVIEW | PENDING APPROVAL | APPROVED]
Sprint Item: [6.X | N/A]

[PDF attached]

— [Agent Name] ([Role])
```

---

## Tier 1 Example Posts

**Kitt (COO) — Daily Review:**
```
[INTERNAL] [ANALYSIS] — Kitt (COO)

Daily OS Review — 17 March 2026

Scorecard complete. 12/15 dimensions scored. Token spend: £4.20 today (76% of daily budget). 2 idle agent periods detected (Oracle 3h, Alpha 1.5h). No SOUL integrity issues. Full scorecard in operations-log.

Status: COMPLETED
Sprint Item: 6.1
Next Action: Review findings with Optimus for optimisation

— Kitt (COO)
```

**Data (CTO) — Operational Alert:**
```
[INTERNAL] [DEVELOPMENT] — Data (CTO)

VPS Memory Alert

Server memory at 82% (13.1/16GB). Primary consumer: 6 concurrent agent processes. Recommendation: implement agent idle-sleep for non-active agents. No immediate risk but approaching threshold.

Status: FOR REVIEW
Sprint Item: N/A
Next Action: Optimus to approve idle-sleep implementation

— Data (CTO)
```

## Tier 2 Example — Document Route

**Alpha produces a competitor analysis (strategic recommendation = Tier 2):**

1. Alpha drafts content in structured markdown with all sections
2. Alpha sends to Optimus: "Tier 2 board document ready for formatting. Content attached."
3. Optimus reviews content, approves, routes to Arthur via Mac Mini bridge
4. Arthur runs `recoveri-board-doc-formatter` skill → produces `RECOVERI_UK_Website_Rescue_Competitor_Analysis_v1.pdf`
5. PDF returned to Optimus → posted to Recoveri Board TG with summary message
6. Decision logged to `/operations-logs/decisions/`

---

## Agent-to-Pillar Posting Rights

| Agent | Role | Tier 1 (TG Post) | Tier 2-4 (Board Doc) |
|-------|------|-------------------|----------------------|
| Optimus | CEO & Orchestrator | ALL pillars + INTERNAL | ALL — also acts as approval gateway |
| Data | CTO | INTERNAL, any pillar for tech updates | INTERNAL, tech strategy |
| Alpha | CRO | CORE, SOCIAL, STUDIOS | CORE, SOCIAL, STUDIOS |
| Kitt | COO | INTERNAL, operational updates for any pillar | INTERNAL, operational strategy |
| Oracle | Consultant | TRADERS, DEVELOPMENTS, research for any pillar | TRADERS, DEVELOPMENTS |

**Neo (CoS)** does NOT post to Board directly — Neo's role is relay to Boss via DM, not board broadcasting.

---

## Implementation

### How It Works in OpenClaw

**Tier 1 flow:**
1. Agent formats update using TG Post Template
2. Agent sends to Optimus (TG posting gateway)
3. Optimus validates format compliance → posts to Recoveri Board TG
4. Logged to decision log

**Tier 2-4 flow:**
1. Agent drafts content in structured markdown (Content Structure above)
2. Agent sends to Optimus with governance tier classification
3. Optimus reviews (Tier 2: approves/rejects; Tier 3-4: routes to Neo → Boss)
4. Once approved, content sent to Arthur via Mac Mini bridge
5. Arthur runs `recoveri-board-doc-formatter` → produces branded PDF
6. PDF returned → Optimus posts to Recoveri Board TG with summary message
7. PDF stored in Google Drive under appropriate pillar folder
8. Logged to decision log

### Anti-Spam Rules

- Maximum 3 Tier 1 posts per agent per day
- No duplicate posts (same content within 24h)
- Optimus can batch multiple Tier 1 updates into a single board post to reduce noise
- Kitt's daily OS Review gets a dedicated posting slot (not counted against limits)
- Tier 2-4 documents are not subject to daily limits (they require approval anyway)

---

## Rollback

If this workflow creates noise or governance concerns:
1. Boss can revoke Tier 1 posting rights for any agent via Neo
2. Optimus can temporarily suspend all Tier 1 posting (escalating everything to Tier 2)
3. Tier 2-4 document requirement can be relaxed to Tier 3-4 only if found to be overkill
4. Full rollback: remove this skill, all posts go back through Neo → Boss pipeline
