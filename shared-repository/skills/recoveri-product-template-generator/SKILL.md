# SKILL.md — RecoveriStudio Product Template Generator
## Skill #134 | recoveri-product-template-generator
## Version: 1.0 | Created: 19 March 2026

---

## IDENTITY

**Name:** RecoveriStudio Product Template Generator
**Skill Number:** 134
**Category:** Content Production
**Owner:** RecoveriStudio (Recoveri)
**Status:** ACTIVE

---

## PURPOSE

Generate professional, market-ready digital product templates in the RecoveriStudio visual style. Takes a product brief as input, researches the target market, generates structured template content, and outputs publication-ready files.

This skill codifies the quality standard established by the AI Daily Execution System v5 and Finance Hub v2, ensuring every RecoveriStudio product maintains consistent branding, quality, and market positioning.

---

## INPUT SPECIFICATION

The skill accepts a **Product Brief** with the following fields:

```json
{
  "product_name": "string — product title",
  "product_type": "spreadsheet | pdf_guide | notion_template | workbook | planner | tracker | system",
  "target_market": "string — who this is for",
  "problem_solved": "string — the core problem this product solves",
  "key_features": ["string array — list of features to include"],
  "price_tier": "entry | standard | premium | ultimate",
  "platform": "google_sheets | excel | notion | pdf | multi_platform",
  "category": "finance | productivity | business | health | education | lifestyle",
  "competitor_reference": "string — optional, top competitor to outperform",
  "style_variant": "dark | light | bold | minimal",
  "include_sections": ["overview | tracker | calculator | planner | dashboard | goals | reports | guide"],
  "special_instructions": "string — optional, additional requirements"
}
```

---

## OUTPUT SPECIFICATION

The skill produces:

1. **Template Content Document** (Markdown) — full structured content for every section
2. **Visual Style Guide** (Markdown) — colours, typography, layout specs for this specific product
3. **Listing Assets** (Markdown) — Etsy/marketplace optimised title, description, tags, thumbnail concepts
4. **Production Checklist** — step-by-step guide to build the final product from the content

---

## VISUAL STYLE STANDARD

All RecoveriStudio products follow this visual identity system:

### Branding
- **Logo:** RecoveriStudio wordmark, top-left of every page/sheet
- **Tagline placement:** Below logo or in footer
- **Copyright:** "© 2026 RecoveriStudio. All rights reserved."

### Typography
- **Headings:** Bold, clean sans-serif (Inter Bold / SF Pro Display Bold)
- **Body:** Light-weight readable sans-serif (Inter Regular / Plus Jakarta Sans)
- **Data/Numbers:** Monospace for numerical displays (SF Mono / JetBrains Mono)
- **Hierarchy:** H1 (24px) → H2 (18px) → H3 (14px) → Body (12px)

### Colour System — WGSN + Coloro Spring/Summer 2026 Palette

**Primary Palette:**
| Name | Hex | Usage |
|------|-----|-------|
| Deep Navy | #0F1117 | Dark theme backgrounds |
| Warm White | #FAFBFC | Light theme backgrounds |
| Electric Blue | #3B82F6 | Primary accent, CTAs, links |
| Emerald | #10B981 | Success states, positive values, growth |
| Amber | #F59E0B | Warnings, pending states, attention |
| Coral Red | #EF4444 | Errors, negative values, urgency |

**Extended Palette (SS26):**
| Name | Hex | Usage |
|------|-----|-------|
| Soft Indigo | #6366F1 | Secondary accent, categories |
| Teal | #14B8A6 | Highlights, alternative accent |
| Warm Orange | #F97316 | Energy, motivation elements |
| Soft Pink | #EC4899 | Lifestyle variant accent |
| Purple | #8B5CF6 | Premium/exclusive elements |
| Cyan | #06B6D4 | Data visualisation, info elements |

### Layout Principles
- **Grid:** 12-column grid system, 16px gutters
- **Cards:** Rounded corners (10px), subtle border (1px #2A2E3A), hover state
- **Spacing:** 8px base unit (8, 16, 24, 32, 48)
- **Shadows:** Minimal — 0 2px 8px rgba(0,0,0,0.1) for cards
- **White space:** Generous — minimum 24px between sections

### Special Elements
- **Pro Tips:** Highlight box with coloured left border (4px), light background tint, "💡 Pro Tip" or "⚡ Power Move" header
- **Phase Headers:** Full-width coloured banner with phase number and title
- **Progress Indicators:** Horizontal bar with percentage, colour-coded (red → amber → green)
- **Fillable Sections:** Dotted border, light grey background, placeholder text in italic
- **Data Cards:** Compact stat display — large number, small label, optional trend arrow

---

## PROCESSING PIPELINE

### Stage 1: Market Research
```
Input: product_brief.target_market + product_brief.category
Actions:
  1. Search for top 10 competing products in the category
  2. Analyse pricing distribution
  3. Identify feature gaps (what competitors lack)
  4. Extract common buyer complaints from reviews
  5. Identify the #1 differentiator opportunity
Output: market_context.json
```

### Stage 2: Content Architecture
```
Input: product_brief + market_context
Actions:
  1. Define section structure based on product_type and include_sections
  2. Map features to sections
  3. Determine content depth per section (overview vs detailed)
  4. Create content outline with heading hierarchy
  5. Identify data fields, formulas, and automations needed
Output: content_architecture.json
```

### Stage 3: Content Generation
```
Input: content_architecture + product_brief
Actions:
  1. Write section headers and descriptions
  2. Generate instructional content (how-to-use guides)
  3. Create example data sets (realistic, relevant to target market)
  4. Write pro tips and power moves for each section
  5. Generate FAQ content (5-10 questions)
  6. Write the "What's Included" inventory
Output: template_content.md
```

### Stage 4: Visual Specification
```
Input: product_brief.style_variant + product_brief.price_tier
Actions:
  1. Select colour palette variant (dark/light/bold/minimal)
  2. Specify typography for each element type
  3. Define layout grid for each section
  4. Create thumbnail image descriptions (3 concepts)
  5. Specify chart/graph styles for data sections
Output: visual_spec.md
```

### Stage 5: Listing Optimisation
```
Input: template_content + market_context + product_brief
Actions:
  1. Generate SEO-optimised title (140 chars for Etsy)
  2. Write 3 listing description variants (feature-led, story-led, benefit-led)
  3. Select optimal 13 tags based on keyword research
  4. Define pricing recommendation (entry + premium if applicable)
  5. Create thumbnail concept descriptions
Output: listing_assets.md
```

### Stage 6: Quality Assurance
```
Input: all previous outputs
Actions:
  1. Verify all product_brief features are addressed
  2. Check branding consistency (logo, colours, typography)
  3. Validate content completeness (no placeholder text remaining)
  4. Verify SEO keyword integration in content
  5. Check for spelling, grammar, tone consistency
  6. Score against RecoveriStudio quality rubric (must score 8+/10)
Output: qa_report.json
```

---

## QUALITY RUBRIC

Every product template is scored against these criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Completeness | 20% | All brief requirements addressed, no gaps |
| Visual Consistency | 15% | Adheres to RecoveriStudio style guide |
| Content Quality | 20% | Clear, professional, error-free writing |
| Market Fit | 15% | Addresses real buyer needs identified in research |
| Differentiation | 15% | Clear advantages over top competitors |
| Usability | 15% | Easy to understand, intuitive structure, clear instructions |

**Minimum score to ship: 8.0/10**

---

## EXAMPLE INVOCATION

```json
{
  "skill": 134,
  "brief": {
    "product_name": "Freelancer Income OS",
    "product_type": "spreadsheet",
    "target_market": "Freelancers and self-employed professionals managing irregular income",
    "problem_solved": "Irregular income makes budgeting impossible with traditional tools",
    "key_features": [
      "Variable income tracker",
      "Tax reserve calculator (UK/US)",
      "Client payment tracker",
      "Invoice log",
      "Quarterly tax estimation",
      "Annual summary with tax-ready export",
      "Emergency fund calculator based on income volatility"
    ],
    "price_tier": "premium",
    "platform": "multi_platform",
    "category": "finance",
    "competitor_reference": "Top Etsy freelancer budget templates",
    "style_variant": "dark",
    "include_sections": ["dashboard", "tracker", "calculator", "reports", "guide"],
    "special_instructions": "Include UK tax brackets and National Insurance calculations"
  }
}
```

---

## DEPENDENCIES

- **Swarm 1 (Market Intel):** Pricing data, market trends
- **Swarm 2 (Product Discovery):** Competitor analysis, gap identification
- **Swarm 5 (Content Generation):** Core content production engine
- **Swarm 6 (Skill Evolution):** Quality improvement loop, pattern recognition

---

## GOVERNANCE

- All output reviewed against Constitution v4.1 fabrication policy
- No fabricated reviews, sales numbers, or testimonials in listing assets
- All market claims must be sourced or clearly marked as estimates
- Price recommendations based on real competitor data, not assumptions
- PILOT phase: all output requires Boss approval before publication

---

## FILE STRUCTURE

```
/root/shared-repository/skills/recoveri-product-template-generator/
├── SKILL.md                    (this file)
├── style-guide.md              (visual identity reference)
├── quality-rubric.json         (scoring criteria, machine-readable)
├── templates/
│   ├── spreadsheet-base.md     (base template for spreadsheet products)
│   ├── pdf-guide-base.md       (base template for PDF guide products)
│   ├── listing-copy-base.md    (base template for marketplace listings)
│   └── thumbnail-brief-base.md (base template for image concepts)
└── examples/
    ├── finance-hub-v2/         (reference implementation)
    └── ai-daily-execution-v5/  (reference implementation)
```

---

*RecoveriStudio | Sprint 9 Session 12 | 19 March 2026*
*Skill #134 | recoveri-product-template-generator*
*Status: REGISTERED*
