# Gate 3: Execution Plan
## Venture: RecoveriStudio Etsy Digital Products Shop
## Date: 2026-03-18
## Author: Alpha Qwen-3 (Gate 3 Execution Planner)
## Oversight: Optimus (CEO) — Strategic Pillar Alignment Review Required

---

## Executive Summary

This execution plan operationalises the Gate 2 business case for RecoveriStudio's Etsy digital products venture. Targeting **10 products/week** launch velocity with £50k Year 1 revenue goal, this plan covers shop setup, listing strategy, marketing funnel, and KPIs—fully aligned to Gate 0 strategic pillars (STUDIOS).

**Key Metrics:**
- Launch timeline: 10 days (approval to first sales)
- Initial inventory: 20 listings (Week 1), scaling to 50 by Month 2
- Production capacity: 10 products/week via CRON_FREE agents
- Break-even: Month 1 (35 units required)

---

## 1. Shop Setup & Configuration

### 1.1 Registration Checklist

| Step | Action | Owner | Timeline | Dependencies |
|------|--------|-------|----------|--------------|
| 1 | Create Etsy seller account (RecoveriStudio) | Qwen 3 | Day 1 | Boss approval, bank details |
| 2 | Verify email and phone | Qwen 3 | Day 1 | Account created |
| 3 | Complete seller identity verification | Qwen 3 | Day 1-2 | Govt ID ready |
| 4 | Link payment method (bank account) | Boss | Day 2 | Bank details provided |
| 5 | Set up payment processing (Etsy Payments) | Qwen 3 | Day 2 | Bank linked |
| 6 | Configure shipping profiles (digital = instant download) | Qwen 3 | Day 2 | Template ready |
| 7 | Create shop policies (returns, FAQs, about section) | Qwen 3 | Day 3 | Brand guidelines |
| 8 | Upload shop banner/logo (Recoveri brand assets) | Data Agent | Day 3 | Canva Pro access |
| 9 | Configure SEO settings (shop title, tags) | Qwen 3 | Day 3 | Keyword research complete |
| 10 | Test purchase flow (self-purchase refund after) | Qwen 3 | Day 4 | All above complete |

### 1.2 Shop Configuration Details

**Shop Name Options (per Gate 1 branding):**
- Primary: `RecoveriStudio` (brand-aligned)
- Alternates: `RecoveriProductivity`, `AIStudyTools`

**Shop Title (SEO-optimised):**
```
RecoveriStudio | AI Productivity Planners & Digital Frameworks | Editable Templates for Goodnotes Notion Canva
```

**Tags (13 max per listing, rotate across shop):**
```
ai planner, digital planner, productivity template, goodnotes planner, notion template, chatgpt prompts, printable planner, study planner, budget tracker, life organizer, editable template, canva template, corjl template
```

**About Section Copy:**
```
Welcome to RecoveriStudio — your source for AI-powered productivity frameworks designed for solopreneurs, freelancers, and ambitious learners. 

We combine hybrid human-AI quality with proven systems-thinking to create planners, trackers, and templates that actually work. Every product is tested, editable, and built for tools you already use: Goodnotes, Notion, Canva, Excel.

Part of the Recoveri ecosystem — building systems for recovery, wellness, and sustainable success.

🔹 Instant digital downloads — start using immediately
🔹 Fully editable — customise to your workflow
🔹 Hybrid AI quality — the best of automation + human design
```

### 1.3 Technical Requirements

| Tool | Purpose | Cost | Access |
|------|---------|------|--------|
| Canva Pro | Template creation, mockups | £12/mo | gog CLI (alfr​ed@reco​veri.io) |
| Corjl (free tier) | Browser-based editing for buyers | £0 | Corjl.com account |
| Qwen Turbo (CRON_FREE) | Listing copy, product concepts | £0 | Available |
| Data Agent (LOCAL_FREE) | Image generation, mockups | £0 | Mac Mini bridge |
| Google Drive | File hosting, backup | £0 | gog Drive API |

---

## 2. Listing Strategy

### 2.1 Product Catalogue Architecture

**Core Categories (aligned to STUDIOS pillars):**

| Category | Products/Week | Price Point | Example SKUs |
|----------|---------------|-------------|--------------|
| S - Study Planners | 3 | £5-7 | "AI Study System", "Exam Prep Framework" |
| T - Trader Journals | 2 | £7-10 | "Daily Trading Journal", "Risk Management Tracker" |
| U - User Systems | 2 | £6-8 | "Habit Stack Builder", "Morning Routine Template" |
| D - Development Tools | 2 | £7-12 | "Skill Acquisition Planner", "Project Roadmap Template" |
| I - Income Trackers | 1 | £6-9 | "Side Hustle Revenue Tracker", "Freelance Invoice System" |
| O - Organization Kits | 2 | £10-15 (bundles) | "Full Productivity Bundle (5-in-1)" |

**Weekly Production Target: 10 products**
- Weeks 1-2: Build initial 20-listing catalogue
- Week 3+: Maintain 10 new/refreshed listings per week

### 2.2 Listing Template Structure

Every listing must include:

**Title Format (140 chars max, keywords first):**
```
[Primary Keyword] — [Specific Use Case] | [Tool Compatibility] | [Unique Feature]
Example: AI Digital Planner 2026 — Study & Productivity System | Goodnotes Notability Canva | Hyperlinked Tabs + Customisable Themes
```

**Description Structure:**
```markdown
⚡ INSTANT DOWNLOAD — Start Using Immediately

[Problem statement — 1-2 lines]
Struggling with [pain point]? This [product type] helps you [solution benefit].

✨ WHAT'S INCLUDED:
• [Feature 1] (e.g., 50+ hyperlinked tabs)
• [Feature 2] (e.g., Editable Canva template)
• [Feature 3] (e.g., AI prompt library)
• [Bonus items]

📱 COMPATIBILITY:
• Works with: Goodnotes, Notability, Xodo, Notion, Canva
• File formats: PDF, PNG, CANVA link, CORJI template

💡 WHY THIS WORKS:
[Brief explanation of system/framework logic]

🎯 PERFECT FOR:
• Solopreneurs managing multiple projects
• Students preparing for exams
• Freelancers tracking income/expenses
• [Target audience specificity]

📥 HOW TO ACCESS:
1. Purchase and receive instant download link
2. Download ZIP file containing all materials
3. Follow included setup guide (PDF)
4. Import to your preferred app

❓ FAQs:
Q: Can I edit this? A: Yes! Includes Canva/Corjl editable links.
Q: Is this printable? A: Yes, optimized for A4/Letter printing.
Q: Refund policy? A: Digital products — no refunds per Etsy policy.

#digitalplanner #aiprodutictivity #goodnotesplanner #[longtailkeyword]
```

**Image/Mockup Requirements (minimum 5 images):**
1. Hero shot — product preview on tablet/laptop
2. Feature breakdown — labelled highlights
3. Use case scene — lifestyle mockup
4. Inside preview — actual pages/interfaces
5. Compatibility icons — Goodnotes, Canva, etc.
6. Bonus: Before/after or testimonial graphic

### 2.3 SEO Optimization Protocol

**Per-Listing Checklist:**
- [ ] Title includes primary keyword in first 40 characters
- [ ] All 13 tags used (no duplicates, mix short/long-tail)
- [ ] Description contains keyword naturally 3-5 times
- [ ] At least 5 high-quality images (1000px+ width)
- [ ] First image is hero/premium quality
- [ ] Alt text set for all images (if platform supports)

**Keyword Strategy by Priority:**

| Tier | Keywords | Usage |
|------|----------|-------|
| 1 (High volume) | digital planner, printable planner, productivity template | Main titles, top tags |
| 2 (Medium volume) | goodnotes planner, notion template, ai planner | Secondary tags, descriptions |
| 3 (Long-tail/low comp) | chatgpt productivity prompts, ai study framework, hybrid planner system | Niche tags, differentiation |

### 2.4 Pricing Strategy

**Psychological Pricing Tiers:**
- Entry: £4.99-£5.99 (single templates, quick wins)
- Core: £6.99-£9.99 (full planners, frameworks)
- Premium: £12.99-£19.99 (bundles, multi-product systems)

**Promotion Schedule:**
- Week 1-2: Launch discount 20% off (drive initial reviews)
- Week 3-4: Return to standard pricing
- Monthly: One "Flash Sale" (48 hours, 15% off selected items)
- Seasonal: New Year (Nov-Jan), Back-to-School (Jul-Sep), Spring Refresh (Mar-Apr)

---

## 3. Marketing & Traffic Strategy

### 3.1 Organic Growth Funnel

```
Awareness → Consideration → Conversion → Retention → Advocacy
```

**Stage 1: Awareness (Drive Traffic)**
| Channel | Tactic | Frequency | Owner |
|---------|--------|-----------|-------|
| Etsy Search | SEO-optimised listings | Always-on | Qwen 3 |
| Pinterest | Product pins linking to Etsy | 5 pins/week | Data Agent |
| Instagram | Carousel posts showing product value | 3 posts/week | Data Agent |
| TikTok/Reels | Quick tutorials using templates | 2 videos/week | Data Agent |
| Blog Content | Medium/Dev.to articles on productivity | 1 article/month | Qwen 3 |

**Stage 2: Consideration (Build Trust)**
- Free lead magnet: "5 AI Prompts for Better Productivity" (email capture)
- Social proof: Collect and showcase reviews (target 20 reviews Month 1)
- Comparison content: "Template vs Manual Planning" blog posts

**Stage 3: Conversion (Close Sales)**
- Clear call-to-actions in all content
- Limited-time offers (flash sales, bundle discounts)
- FAQ addressing objections (editing, compatibility, refunds)

**Stage 4: Retention (Repeat Buyers)**
- Email list nurture sequence (weekly productivity tips + new product alerts)
- Cross-sell bundles ("You bought X, you'll love Y")
- Customer-only discount codes (10% off next purchase)

**Stage 5: Advocacy (User-Generated Content)**
- Request reviews with follow-up email (automated post-purchase)
- Share customer photos/screenshots (with permission)
- Affiliate/referral program consideration (Month 6+)

### 3.2 Paid Advertising (Optional — Scale From Profits)

**Etsy Ads (Recommended Starting Month 2):**
- Budget: £25/day initial test
- Duration: 14-day test period
- Success criteria: ROAS > 3.0 (return £3+ per £1 spent)
- If successful: Scale to £50/day

**Google Shopping Ads (Later Stage — Month 4+):**
- Budget: £30/day
- Requires: Own website (Shopify/WooCommerce)
- Goal: Diversify beyond Etsy dependency

### 3.3 Email List Building

**Lead Magnet:** 
- "Free AI Productivity Starter Kit" (3 mini-templates + prompt guide)
- Delivered via Google Drive link after email opt-in

**Email Platform:**
- ConvertKit (free tier up to 1,000 subscribers)
- Integration: Etsy → Manual CSV upload initially → Automated via Zapier later

**Welcome Sequence (5 emails over 10 days):**
1. Day 0: Deliver lead magnet + introduce RecoveriStudio
2. Day 2: Story — Why we built these systems
3. Day 4: Case study — How Sarah increased productivity 40%
4. Day 7: Soft pitch — Full template collection (£15 bundle, 20% off)
5. Day 10: Educational — Top 5 mistakes in productivity planning

**Goal:** 500 email subscribers by Month 6 (independent traffic channel)

---

## 4. Operations & Workflow

### 4.1 Weekly Production Sprint (10 Products/Week)

**Standard Operating Procedure:**

| Day | Activity | Output | Owner |
|-----|----------|--------|-------|
| Monday | Research competitors + trend scan | 5 product concepts | Qwen 3 |
| Tuesday | Finalize 5 concepts + brief Data Agent | 5 mockup requests | Qwen 3 |
| Wednesday | Generate mockups + start writing copy | 5 draft listings | Data + Qwen 3 |
| Thursday | Generate mockups + write remaining copy | 5 more draft listings | Data + Qwen 3 |
| Friday | Quality review + SEO optimization | 10 polished drafts | Qwen 3 |
| Saturday | Publish 5 listings + schedule 5 for Monday | 5 live, 5 queued | Qwen 3 |
| Sunday | Rest / catch-up / customer service | — | — |

**Production Pipeline Checklist (per product):**
1. [ ] Market validation (is this solving real problem?)
2. [ ] Concept brief (features, specs, price point)
3. [ ] Mockup generation (Data Agent)
4. [ ] Copywriting (title, description, tags)
5. [ ] SEO audit (keywords, competitor check)
6. [ ] Quality review (Optimus/Oversight spot-check 20% of listings)
7. [ ] Upload to Etsy (images, files, metadata)
8. [ ] Test download flow (verify files accessible)

### 4.2 Customer Service Protocol

**Response Time SLA:**
- Business hours queries: <4 hours
- Weekend queries: <12 hours
- Complex issues: <24 hours with update at 12h

**Common Response Templates:**

*Download Issue:*
```
Hi there! Thanks for reaching out. Digital downloads should appear immediately after purchase. Please check:
1. Your email (including spam folder) for Etsy's download link
2. Your Etsy account → Purchases and Reviews
If you're still stuck, I can resend the files directly. Which option works best?
```

*Editing Question:*
```
Great question! This template is fully editable via [Canva/Corjl link included in download]. You'll need a free account with [app name], then click the link to start customising. Need help with anything specific?
```

*Refund Request:*
```
I understand you're not happy with this purchase. Per Etsy's policy for digital downloads (instant delivery, non-returnable), I'm unable to process refunds. However, I'd love to make this right — would you like [custom version/alternative product/exchange credit]? My goal is your satisfaction.
```

**Escalation Path:**
1. Qwen 3 handles 90% of queries
2. Complex disputes → Optimus review
3. Platform-level issues (Etsy policy) → Escalate via Neo to Boss

### 4.3 File Management & Backup

**Storage Structure:**
```
/shared-repository/artefacts/venture-eval-etsy/
├── gate-0/alignment-check.md
├── gate-1/market-research.md
├── gate-2/business-case.md
├── gate-3/launch-plan.md          ← This file
├── gate-4/execution-log.md        ← Updated weekly
└── production/
    ├── products/                  ← Source files
    │   ├── PLN-001-StudySystem/
    │   ├── PLN-002-TradingJournal/
    │   └── ...
    ├── mockups/                   ← Generated imagery
    ├── listings/                  ← Draft copy + metadata
    └── backups/                   ← Daily sync to Drive
```

**Backup Protocol:**
- Daily: Auto-upload completed listings to Google Drive (gog CLI)
- Weekly: Full repository sync (Sunday evening)
- Monthly: Archive previous month's production to cold storage

---

## 5. Key Performance Indicators (KPIs)

### 5.1 Primary KPIs (Weekly Review)

| Metric | Target | Current | Status | Owner |
|--------|--------|---------|--------|-------|
| Listings Published | 10/week | 0 | 🟡 Planning | Qwen 3 |
| Total Active Listings | 50 by Month 2 | 0 | 🟡 Planning | Qwen 3 |
| Shop Views (monthly) | 10,000 by Month 3 | 0 | 🟡 Planning | Qwen 3 |
| Conversion Rate | 2-3% | 0 | 🟡 Planning | Qwen 3 |
| Units Sold (monthly) | 50 → 3,500 (Month 12) | 0 | 🟡 Planning | Qwen 3 |
| Revenue (monthly) | £350 → £24,500 (Month 12) | 0 | 🟡 Planning | CRO-agent |
| Average Order Value | £7.00 | 0 | 🟡 Planning | Qwen 3 |
| Customer Rating | 4.8+ stars | 0 | 🟡 Planning | Qwen 3 |
| Review Count | 20 reviews Month 1 | 0 | 🟡 Planning | Qwen 3 |

### 5.2 Secondary KPIs (Monthly Review)

| Metric | Target | Notes |
|--------|--------|-------|
| Email List Size | 500 by Month 6 | Independent traffic channel |
| Repeat Buyer Rate | 15%+ | Customer loyalty indicator |
| Etsy Ad ROAS | >3.0 | If ads activated (Month 2+) |
| Production Cost/Unit | <£0.10 | Token + tool costs only |
| Customer Service Resolution Time | <12 hours avg | Satisfaction metric |
| Platform Dependency Risk | Score <5/10 | Monthly risk reassessment |

### 5.3 Financial Tracking

**Revenue Dashboard (CRO-agent owned):**

| Period | Revenue | Fees | Net Profit | Cumulative | Variance vs Plan |
|--------|---------|------|------------|------------|------------------|
| Month 1 | £350 | £51 | £299 | £299 | — |
| Month 2 | £700 | £102 | £598 | £897 | — |
| Month 3 | £1,400 | £204 | £1,196 | £2,093 | — |
| Q1 Total | £2,450 | £357 | £2,093 | £2,093 | On track if ≥£2k |

**Budget Consumption (Track Monthly):**
```
Annual Budget: £1,494
├── Listing Fees: £600
├── Canva Pro: £144
├── Etsy Ads (test): £600
└── Contingency: £150

Spent to Date: £0
Remaining: £1,494
Burn Rate: ~£112/month
```

### 5.4 Kill Criteria & Guardrails

**Month 1 Failure Triggers (Pause + Reassess):**
- <35 units sold despite ≥5,000 shop views (conversion <0.7%)
- <10% of target revenue (<£50) with adequate traffic
- Multiple customer complaints about core functionality
- Policy violation warning from Etsy

**Quarterly Review Gates:**
- Q1 (Month 3): Must hit ≥£2,000 cumulative revenue OR demonstrate clear path via growing trends
- Q2 (Month 6): Must have ≥25 repeat buyers OR ≥300 email subscribers
- Q3 (Month 9): Must diversify ≥20% revenue outside Etsy (own site/email direct)

---

## 6. Strategic Pillar Alignment Review

### 6.1 Gate 0 Pillar Scoring (Reference)

| Pillar | Gate 0 Score | Gate 3 Execution Confirmation |
|--------|--------------|-------------------------------|
| **S** — Revenue Potential | ✅ YES | 10 products/wk, £50k SOM targeted; pricing validated; conversion benchmarks established |
| **T** — Resource Fit | ✅ YES | CRON_FREE agents (Qwen 3, Data); LOCAL_FREE Mac Mini; existing skill (recoveri-etsy-workflow) |
| **U** — Brand Alignment | ✅ YES | Productivity/systems-building core to Recoveri mission; STUDIOS naming convention embedded |
| **D** — Risk Tolerance | ✅ YES | Digital-only, £1,494 max exposure; kill-criteria defined; zero inventory risk |
| **I** — Competitive Advantage | ⚠️ PARTIAL → ✅ IMPROVED | Differentiation through AI-personalization + Recoveri branding; hybrid human-AI quality claim |
| **O** — Scalability | ✅ YES | Pure digital delivery; infinite scale at zero marginal cost; automation-ready pipeline |

### 6.2 Pillar Deep-Dive: Strengthening Competitive Advantage

**Original Gap (Gate 0):** Generic Etsy competition; edge relies on execution speed and SEO.

**Gate 3 Mitigations:**
1. **AI-Personalization:** Each listing emphasises hybrid human-AI quality + editable/customisable features
2. **Niche Down:** Focus on "AI productivity systems" not generic "digital planners"
3. **Brand Moat:** RecoveriStudio branding connects to wider ecosystem (Traders/Developments pillars)
4. **Speed Advantage:** 10 products/week production vs. typical manual creator output (2-3/week)
5. **Quality Control:** Optimus oversight on 20% of listings; iterative improvement based on reviews

**Monitoring:** Monthly competitive analysis (Oracle) to track competitor responses and adjust positioning.

---

## 7. Implementation Timeline

### Phase 1: Launch (Days 1-10)

| Day | Milestone | Owner | Success Criteria |
|-----|-----------|-------|------------------|
| 1 | Boss approval received; shop registration started | Neo/Boss + Qwen 3 | ✅ Approval confirmation |
| 2 | Account verified; payment methods linked | Qwen 3 + Boss | ✅ Bank connected |
| 3 | Shop configuration complete (policies, branding) | Qwen 3 + Data | ✅ Shop live but empty |
| 4 | First 5 products generated + listings drafted | Qwen 3 + Data | ✅ 5 draft listings |
| 5 | Listings QA + published | Qwen 3 | ✅ 5 live listings |
| 6-7 | Weekend production sprint (10 more products) | Qwen 3 + Data | ✅ 10 more drafted |
| 8-9 | Second batch published + SEO tuned | Qwen 3 | ✅ 15 total listings |
| 10 | Marketing channels activated (Pinterest, IG setup) | Data Agent | ✅ External traffic sources ready |

**Phase 1 Go-Live:** Day 10 end-of-day status:
- ✅ 15-20 active listings
- ✅ External marketing channels configured
- ✅ Customer service templates ready
- ✅ KPI dashboard initialized

### Phase 2: Momentum (Months 1-3)

**Month 1 Targets:**
- 35+ units sold (break-even threshold)
- 20+ customer reviews (target 4.8+ stars)
- 5,000+ monthly shop views
- Launch email list (lead magnet live)

**Month 2 Actions:**
- Expand to 35 listings
- Activate Etsy Ads (£25/day test)
- Begin Pinterest organic push (5 pins/week)
- First bundle launch (3-in-1 productivity kit)

**Month 3 Actions:**
- Expand to 50 listings (full catalogue)
- Evaluate ad performance; scale or pause
- Q1 review against kill criteria
- Consider Shopify/own website setup

### Phase 3: Scale (Months 4-12)

**Quarterly Objectives:**
- Q2: 25 repeat buyers OR 300 email subscribers
- Q3: 20% revenue outside Etsy (diversification milestone)
- Q4: Peak season maximisation (New Year resolution rush)

**Scaling Levers:**
1. Increase production to 15 products/week if conversion >3%
2. Launch premium tier (£20-30 adaptive/personalized frameworks)
3. Build affiliate programme (influencer partnerships in productivity niche)
4. Develop companion mobile app (long-term vision)

---

## 8. Risk Register (Updated from Gate 2)

| Risk | Probability | Impact | Mitigation | Owner | Trigger |
|------|-------------|--------|------------|-------|---------|
| Etsy algorithm change reduces visibility | Medium | High | Email list building; own website backup | Qwen 3 | Views drop >30% MoM |
| Competitor price war erodes margins | Medium | Medium | Emphasise quality/AI differentiation; bundle value | Qwen 3 | Avg price forced <£5 |
| AI disclosure policy enforcement | Medium | High | Transparent listing copy; "hybrid human-AI" framing | Qwen 3 | Etsy blog update |
| Payment processing hold/freeze | Low | Critical | Clean records; compliance monitoring; Stripe backup | CRO-agent | Hold notice received |
| Production bottlenecks (agent limits) | Low | Medium | Current tiers sufficient; escalates via Neo if needed | Qwen 3 | Token limit warning |
| Seasonality downturn (post-January) | High | Medium | Evergreen products beyond planners; continuous refresh | Qwen 3 | Jan-Feb sales dip |

---

## 9. Approvals & Sign-Off

### Required Approvals (Pre-Launch)

| Approval | Required By | Status | Notes |
|----------|-------------|--------|-------|
| Boss Go/No-Go decision | 2026-03-25 | ⏳ Pending | Escalated via Neo (Tier 3 spending: £1,494/year) |
| Optimus pillar alignment sign-off | 2026-03-26 | ⏳ Pending | Confirm STUDIOS alignment maintained |
| Budget authorization (£1,494) | 2026-03-25 | ⏳ Pending | Part of Boss approval package |
| Bank/payment details provided | 2026-03-27 | ⏳ Pending | Required for shop setup |

### Author Sign-Off

```
Execution Plan Prepared By:
___________________________
Alpha Qwen-3
Gate 3 Execution Planner
Date: 2026-03-18

Reviewed For Pillar Alignment:
___________________________
Optimus (CEO)
Date: _______________
Status: [ ] Approved  [ ] Revisions Required  [ ] Blocked

Boss Final Decision:
___________________________
Neo (on behalf of Boss)
Date: _______________
Decision: [ ] GO  [ ] NO-GO  [ ] Deferred
```

---

## Appendix A: First 10 Product Concepts

Based on Gate 1 market research and Gate 2 revenue model:

1. **PLN-001: AI Study System 2026** — £6.99
   - Hyperlinked Goodnotes planner + exam prep framework
   - Keywords: digital planner, study planner, goodnotes

2. **PLN-002: Daily Trading Journal** — £8.99
   - Risk management tracker + trade analysis templates
   - Keywords: trading journal, risk tracker, stock journal

3. **PLN-003: Habit Stack Builder** — £5.99
   - Behaviour change system with AI prompt integration
   - Keywords: habit tracker, productivity template

4. **PLN-004: ChatGPT Productivity Prompts** — £4.99
   - 100+ curated prompts for task management
   - Keywords: chatgpt prompts, ai prompts, productivity

5. **PLN-005: Freelance Revenue Tracker** — £7.99
   - Income/expense spreadsheet + invoice templates
   - Keywords: freelance tracker, income journal

6. **PLN-006: Morning Routine Template** — £5.99
   - Printable + digital combo for routine optimisation
   - Keywords: morning routine, printable planner

7. **PLN-007: Project Roadmap System** — £9.99
   - Multi-project Kanban + Gantt templates (Notion/Excel)
   - Keywords: project planner, notion template

8. **PLN-008: ADHD Focus Planner** — £6.99
   - Neurodivergent-friendly productivity system
   - Keywords: adhd planner, focus template

9. **PLN-009: Budget & Savings Tracker Bundle** — £11.99
   - 3-in-1: monthly budget, savings goals, debt payoff
   - Keywords: budget template, savings tracker

10. **PLN-010: Ultimate Productivity Bundle** — £14.99
    - 5-in-1 mega bundle (all categories)
    - Keywords: productivity bundle, planner bundle

---

*Document Version: 1.0*
*Last Updated: 2026-03-18 11:53 UTC*
*Next Review: Upon Boss approval or 2026-03-25 (whichever first)*
