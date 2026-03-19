# Gate 3: Resources Plan
## Venture: RecoveriStudio Etsy Digital Products Launch
## Date: 2026-03-18
## Author: Alpha Qwen-1 (CRON_FREE Operations Worker)

---

## Executive Summary

This resources plan operationalizes the Gate 2 business case (£50k conservative revenue target, 3,247% ROI) through structured agent assignments, tooling infrastructure, and cost controls aligned to CRON_FREE tier economics. Total Year 1 investment: **£1,494** against £50k conservative revenue = **£48,506 net profit**.

---

## 1. Agent Assignments & Workflows

### Core Production Team (RecoveriTaskRouter Skill Routing)

| Role | Agent | Tier | Responsibility | Frequency | Time Allocation |
|------|-------|------|----------------|-----------|-----------------|
| Product Designer | Alpha (Qwen-2 legacy role) | CRON_FREE | Framework briefs, listing copy, SEO | Daily (M-F) | 2-4 hrs/day |
| Visual Generator | Data Agent | LOCAL_FREE | Mockups, PDF exports, Canva templates | As needed | 1-2 hrs/day |
| Shop Manager | Qwen-1 (me) | CRON_FREE | Listings publish, ads optimization, customer service | Daily | 2-3 hrs/day |
| Market Intelligence | Oracle (CC) | CONSULTANT | Competitor analysis, trend spotting | Monthly | 4 hrs/month |
| Financial Oversight | CRO-agent | C-LEVEL | Revenue tracking, ROI reporting, budget monitoring | Weekly | 1 hr/week |
| Strategic Direction | Optimus (CEO) | C-LEVEL | Milestone approvals, pivot decisions | Bi-weekly | 0.5 hrs/session |

### Workflow Orchestration

```
Product Creation Pipeline (per product):
┌─────────────────┐
│ Alpha generates │ (framework definition + use cases)
│ brief (15 min)  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Data creates    │ (mockup + PDF export + metadata)
│ visual assets   │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Qwen-1 publishes│ (Etsy listing with optimized tags)
│ listing         │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Oracle reviews  │ (monthly competitor gap check)
│ market fit      │
└─────────────────┘
```

### Capacity Planning

| Activity | Avg. Time/Product | Products/Wk | Total Wk | Total Hours | Agent Utilization |
|----------|-------------------|-------------|----------|-------------|-------------------|
| Brief creation | 15 min | 10 | 12 | 25 hrs | 4 hrs/day avg |
| Visual generation | 30 min | 10 | 12 | 50 hrs | 8 hrs/day avg |
| Listing copy + upload | 20 min | 10 | 12 | 33 hrs | 5 hrs/day avg |
| Customer service | 5 min/order | ~5/day | 12 | 35 hrs | 6 hrs/day avg |
| Admin (ads, SEO, reports) | - | - | 12 | 20 hrs | 3 hrs/day avg |
| **Total** | - | **120 products/year** | - | **~163 hrs** | **~1.5 hrs/product** |

*Note: Assumes 10 products/week pipeline as per Gate 2 approval. At this pace, all agents stay within CRON_FREE token limits.*

---

## 2. Tooling Infrastructure

### Required Tools (Total Cost: £156/year)

| Tool | Purpose | Cost | Notes |
|------|---------|------|-------|
| Canva Pro | Editable template creation | £12/mo = £144/yr | Enables Corjl-style customization |
| Etsy Listing Fees | 50 listings × £0.16 each | £8 per 4-month cycle | Auto-renews on sale |
| Optional Etsy Ads | Traffic acquisition | £50/mo test = £600/yr | Scale from profits only |
| Domain (optional) | Brand asset | £15/yr | recoveristudio.io redirect |
| Email Service | Mailchimp free tier | £0 | Up to 500 subscribers |
| **Total Fixed** | | **£159/yr** | Excluding ad spend |

### Free Tier Stack (Zero-Cost Production)

| Resource | Provider | Limit | Usage |
|----------|----------|-------|-------|
| LLM Tokens | Qwen Turbo | 1M/day | All copywriting, research, ops |
| Image Gen | Mac Mini LOCAL_FREE | Unlimited | Mockups via local Diffusion |
| Database | Local JSON files | N/A | Product catalog tracking |
| Analytics | Etsy dashboard + manual CSV | N/A | Sales data aggregation |
| Comms | Telegram API | Unlimited | Internal coordination |

### Integration Architecture

```
┌──────────────────────────────────────────────┐
│              RecoveriStudio                  │
│         Etsy Operations Hub                  │
├──────────────────────────────────────────────┤
│                                              │
│  [Canva] ←→ [Data Agent] ←→ [Alpha]         │
│     ↓            ↓              ↓            │
│  Templates    Mockups      Copywriting      │
│     ↓            ↓              ↓            │
│  ┌─────────────────────────────────┐        │
│  │   Qwen-1 Shop Manager           │        │
│  │   • Publish listings            │        │
│  │   • Manage ads                  │        │
│  │   • Handle CS                   │        │
│  └────────────────┬────────────────┘        │
│                   ▼                          │
│            Etsy Platform                     │
│                   │                          │
│          Revenue → Stripe/PayPal             │
│                   │                          │
│          Data → CRO-agent (weekly report)    │
└──────────────────────────────────────────────┘
```

---

## 3. Budget & Cost Controls

### Year 1 Budget Breakdown (Conservative £50k scenario)

| Category | One-time | Monthly | Annual | % of Revenue |
|----------|----------|---------|--------|--------------|
| Canva Pro | £0 | £12 | £144 | 0.29% |
| Etsy Fees (listings) | £150 | £50 | £750 | 1.50% |
| Etsy Ads (test) | £0 | £50 | £600 | 1.20% |
| Email Service | £0 | £0 | £0 | 0% |
| Payment Processing | Included | Included | Included | ~3.5% embedded |
| **Total Costs** | **£150** | **£112** | **£1,494** | **~2.99%** |

### Cash Flow Projection

| Month | Cumulative Spend | Cumulative Revenue (conservative) | Net Position |
|-------|------------------|-----------------------------------|--------------|
| 1 | £150 | £350 | +£200 ✅ |
| 2 | £262 | £1,050 | +£788 ✅ |
| 3 | £374 | £2,450 | +£2,076 ✅ |
| 4 | £486 | £5,250 | +£4,764 ✅ |
| 5 | £598 | £9,450 | +£8,852 ✅ |
| 6 | £710 | £15,050 | +£14,340 ✅ |
| 12 | £1,494 | £95,550 | +£94,056 ✅ |

*Break-even achieved Day 2 (after first 35-unit milestone). All months profitable under conservative assumptions.*

### Cost Control Measures

| Measure | Implementation | Trigger |
|---------|----------------|---------|
| Ad spend cap | Max £5/day auto-pause | Never exceed £150/mo without weekly review |
| Token usage monitor | Qwen daily usage check | Alert at 80% daily threshold |
| Monthly expense audit | CRO-agent invoice review | First Monday of each month |
| Listing renewal tracker | JSONL log of expiring listings | Auto-remind 7 days before expiry |
| Price elasticity testing | A/B price points (£5 vs £7 vs £9) | After 50 units sold per variant |

---

## 4. Risk Management

### Risk Register

| Risk | Probability | Impact | Mitigation Owner | Action Item |
|------|-------------|--------|------------------|-------------|
| Etsy policy change on AI content | Medium | High | Neo | Hybrid human-AI disclosure in listings; monitor Etsy blog weekly |
| Saturation in planner niche | High | Medium | Oracle | Differentiate with "AI productivity systems" branding; niche down to solopreneurs |
| Seasonality (Jan peak, Jul trough) | High | Medium | Qwen-1 | Build evergreen framework inventory beyond planners |
| Platform dependency (algorithm shift) | Medium | High | Optimus | Start email list Day 1; Shopify backup channel by Month 6 |
| Payment hold/ban | Low | High | CRO-agent | Maintain clean transaction records; compliant ToS usage |
| IP disputes on designs | Low | Medium | Qwen-1 | Document AI generation process; original prompts only |
| Agent cost escalation (free tier limits) | Low | Negligible | Qwen-1 | Migrate to Mac Mini LOCAL_FREE if needed |

### Kill Criterion (Gate 2 Condition)

**If Month 1 sales < 35 units**, despite:
- ≥ 100 unique visitors from organic traffic
- Conversion rate ≤ 2% industry benchmark
- Active £5/day ad spend

**Then:** Document learnings, pause operations, escalate to Boss for re-assessment or termination.

**Decision Date:** Day 30 post-launch.

---

## 5. Success Metrics Dashboard

### Primary KPIs (Tracked Weekly)

| Metric | Target (Month 1) | Target (Year 1) | Tracking Method |
|--------|------------------|-----------------|-----------------|
| Listings Live | 10 | 120 | Etsy dashboard |
| Units Sold | 35+ | 13,650 | Manual CSV export |
| Conversion Rate | 2%+ | 2.5% | Visits ÷ sales |
| Average Order Value | £7.00 | £7.50 | Revenue ÷ units |
| Net Profit Margin | 70%+ | 72% | Revenue − fees ÷ revenue |
| Email Subscribers | 0 | 500 | Mailchimp dashboard |
| Response Time (CS) | < 24 hrs | < 12 hrs | Telegram logs |

### Secondary KPIs (Tracked Monthly)

| Metric | Target | Owner |
|--------|--------|-------|
| Customer Satisfaction (review score) | 4.7/5+ | Qwen-1 |
| Return Customer Rate | 10%+ | CRO-agent |
| Top Seller Identification | 20% of revenue from top 5 SKUs | CRO-agent |
| SEO Ranking Improvement (target keywords) | +5 positions | Oracle |
| Ad ROAS (Return on Ad Spend) | 3:1+ | Qwen-1 |

---

## 6. Dependencies & Blockers

### External Dependencies

| Dependency | Provider | Lead Time | Status |
|------------|----------|-----------|--------|
| Etsy account verification | Etsy | 3-7 days | Pending Boss bank details |
| Canva Pro subscription | Canva.com | Instant | Ready to activate |
| Payment processing setup | Stripe/PayPal | 2-3 days | Tied to Etsy verification |
| Domain purchase (optional) | Namecheap/Gandi | Instant | Not critical path |

### Internal Dependencies

| Dependency | Owner | Required By | Blocked By |
|------------|-------|-------------|------------|
| Shop branding assets | Qwen-1 | Day 1 | Brand guide access |
| Bank account details | Boss | Day 1 | Boss response |
| Canva license payment | Qwen-1 | Day 1 | Budget unlock |
| Initial 20 listings | Alpha + Data + Qwen-1 | Week 2 | Shop verification complete |

---

## 7. Handoff Protocol (To Post-Launch Ops)

### Phase 1 → Phase 2 Transition Checkpoint (Week 4)

✅ **Goes to Phase 2 if:**
- 20+ listings live
- First 10 sales recorded
- No major policy violations
- Conversion rate ≥ 1%

❌ **Pause & Reassess if:**
- Zero sales after 30 days
- Major Etsy warning received
- Budget overage > 20% without offsetting revenue

### Documentation Requirements (Weekly)

| Document | Format | Location | Audience |
|----------|--------|----------|----------|
| Sales Report | CSV/Markdown | /shared-repository/reporting/sales/ | CRO-agent, Optimus |
| Expense Log | JSONL | /shared-repository/reporting/expenses/ | CRO-agent |
| Listing Performance | Markdown Table | /shared-repository/artefacts/venue-eval-etsy/gate-3/performance.md | All team |
| Customer Feedback | Bulleted List | Shared Google Doc (link in AGENTS.md) | Qwen-1, Alpha |

---

## Sign-off

| Role | Name | Status | Date |
|------|------|--------|------|
| Author | Alpha Qwen-1 | Draft | 2026-03-18 |
| Reviewer | Optimus (CEO) | Pending | - |
| Approver | Neo/Boss | Pending | - |

---

*Resources plan created per Gate 3 mandate. Aligned to STUDIOS strategic pillars. Based on Gate 2 budget (£1,494 investment) and production pipeline (10 products/week). Ready for execution upon Boss approval.*

— Alpha Qwen-1 (CRON_FREE Operations Worker)
