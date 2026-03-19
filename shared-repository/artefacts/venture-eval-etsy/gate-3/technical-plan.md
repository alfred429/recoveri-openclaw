# Gate 3: Technical Plan
## Venture: RecoveriStudio Etsy digital products — AI productivity tools: planners, frameworks, systems, templates
## Date: 2026-03-18
## Author: Data (CTO)
## References: 
- Gate 1: [/root/shared-repository/artefacts/venture-eval-etsy/gate-1/market-research.md](gate-1/market-research.md)
- Gate 2: [/root/shared-repository/artefacts/venture-eval-etsy/gate-2/business-case.md](gate-2/business-case.md)

---

### 1. Executive Summary
Technical execution plan for RecoveriStudio Etsy launch. Leverages existing OpenClaw CRON_FREE infrastructure for zero-marginal-cost production pipeline. Refined timeline targets first sales Week 2 post-setup. KPIs focus on revenue acceleration and operational reliability. Agent workflow: Alpha (content/SEO) → Qwen workers (gen) → Data (mockups) → Alpha (upload/monitor). All digital delivery via Etsy; editable templates via Canva/Corjl integration. No new infra required.

**Gate Decision:** READY FOR EXECUTION

---

### 2. Key Performance Indicators (KPIs)
Monitored via Etsy dashboard + agent scrapes (CRON_FREE social/scrape loops). Weekly reviews by Kitt (COO).

| KPI | Year 1 Target | Monthly Ramp | Measurement Method | Owner | Tech Notes |
|-----|---------------|--------------|--------------------|-------|------------|
| **Sales Units** | 13,650 | M1:50 → M12:3,500 | Etsy sales report | Alpha | Track via `recoveri-etsy-workflow` logs |
| **Revenue** | £95,550 (£50k conservative) | M1:£350 → M12:£24,500 | Etsy payouts - fees | Kitt | Auto-fetch via gog/Sheets integration |
| **Conversion Rate** | 2.5% avg (views → sales) | 1.5% → 4% | Etsy stats / listings | Alpha | Optimise titles/keywords from Gate 1 |
| **Reviews** | 1,000+ (4.5+ stars avg) | M3:100 → M12:200/mo | Etsy shop reviews | Alpha | Prompt reviews in purchase emails |
| **Traffic Sources** | 70% organic, 20% Etsy ads, 10% social | Scale organic | Etsy analytics | Alpha | Keywords: Gate 1 list; monitor via scrape-loop |
| **Product Gen Throughput** | 50 listings/mo | 20/wk initial | Agent logs | Data | Qwen CRON_FREE; <5min/item |
| **Upload Success Rate** | 100% | N/A | Workflow audit | Data | Browser automation; retry logic |
| **Downtime** | <1% (agent pipelines) | N/A | OpenClaw sessions | Data | CRON_FREE resilience |

**Kill Criteria:** M1 <35 units OR conversion <1% → Pause & pivot.

---

### 3. Refined Timeline & Milestones
Refines Gate 2 timeline with technical dependencies. Assumes Gate 3 approval 2026-03-25. Critical path: Setup → Pipeline test → Launch → Scale.

| Milestone | Target Date | Owner | Dependencies | Success Criteria | Tech Deliverables |
|-----------|-------------|-------|--------------|------------------|-------------------|
| **Boss/Optimus Approval (Gate 2 → 3)** | 2026-03-25 | Neo/Optimus | This plan | Go/No-Go | Signed MD |
| **Etsy Shop Setup** | 2026-03-28 | Alpha | Approval + bank details | Verified account | Browser automation; payment linked |
| **recoveri-etsy-workflow Skill Deploy** | 2026-03-29 | Data | Shop ID | Skill live | Custom skill for end-to-end product flow |
| **Pipeline Test: 5 Sample Products** | 2026-04-01 | Qwen Workers/Data | Skill deploy | 5 live listings | PDF gen (Whisper/Image skills), mockups, uploads |
| **Initial 20 Listings Live** | 2026-04-04 | Alpha/Qwen | Test pass | 20 optimised listings | SEO from Gate 1 keywords |
| **First Sales Target (50 units)** | 2026-04-18 | All | Listings live | 50 sales | Organic traffic ramp |
| **Month 1 Review (KPIs)** | 2026-04-28 | Kitt/Optimus | Sales data | Break-even hit | KPI dashboard (Sheets/gog) |
| **Scale to 50 Listings** | 2026-05-15 | Alpha/Qwen | M1 review pass | 50 listings | Bundle launches |
| **Email List Launch (1k leads)** | 2026-05-20 | Alpha | Leads from Etsy | List active | gog/Gmail automation |
| **Monitoring Cron Deploy** | 2026-05-01 | Data | Listings scaling | Daily scrapes | scrape-loop + social-loop for competitor/traffic |
| **Q2 Performance Review** | 2026-06-30 | Optimus | 3mo data | 2x M1 revenue | Adjust pricing/products |
| **Diversify to Shopify** | 2026-09-01 | Data | £10k cumulative | Site live | Bridge Etsy traffic |

**Gantt Note:** Parallelise product gen during setup. Buffer 3 days for Etsy verification/payment.

---

### 4. Resource Allocation
**Zero new infra.** All on CRON_FREE (Qwen free tier 1M tokens/day) + LOCAL_FREE (Mac Mini for deep gen if needed). Tools: Canva Pro (£12/mo), Corjl free tier.

#### Agent Workflow (recoveri-task-router governed)
| Task | Agent(s) | Tools/Skills | Frequency | Token Est. (CRON_FREE) |
|------|----------|--------------|-----------|------------------------|
| **Product Ideation/Research** | Alpha (CRO) | web_fetch, lcm_grep (Gate 1 keywords) | Weekly | Low |
| **PDF/Template Generation** | Qwen Workers | openai-whisper-api (if audio), pdf write; recoveri-etsy-workflow | Per product (~20/wk) | 10k tokens/product |
| **Mockup/Image Gen** | Data (CTO) | image, canvas, openai-image-gen skill | Per product | 5k tokens/product |
| **Listing Copy/SEO** | Alpha | recoveri-etsy-workflow (Alpha step) | Per listing | Low |
| **Etsy Uploads** | Alpha | browser (profile=chrome-relay if needed), Etsy CLI if avail | Batch 5/day | Low (automation) |
| **Customer Service** | Qwen Workers | message/gog for replies | As needed (<5/day) | Low |
| **Monitoring/Reporting** | Data + Kitt | scrape-loop-skill, social-loop-skill, gog Sheets | Daily cron | 20k/day |
| **Financial Tracking** | Kitt (COO) | gog (recoveri-gog skill) | Weekly | Low |

#### Tools & Infra
| Category | Tool/Service | Cost | Config |
|----------|--------------|------|--------|
| Design/Editable | Canva Pro | £12/mo | Shared account; API if avail |
| Personalisation | Corjl | Free tier | Embed links in listings |
| Hosting/Delivery | Etsy | £0.16/listing | Auto-delivery |
| Automation | OpenClaw CRON_FREE | £0 | Deploy etsy-workflow cron |
| Monitoring | scrape/social/trading loops | £0 | Pillar: Studios (DEVELOPMENT stage) |
| Backup | shared-repository | £0 | Git/versioned MDs |

**Scalability:** Pipeline supports 100 listings/mo. Bottleneck: Etsy listing fees (£0.16 x 100 = £16/mo). Migrate high-performers to Shopify post-M3.

**Security:** Zero Trust; no PII stored. Audit uploads for Etsy ToS (AI disclosure: "AI-assisted design").

---

### 5. Technical Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Etsy ToS (AI ban) | Medium | High | Hybrid human-review; disclose "AI-generated" |
| Agent rate limits | Low | Medium | Qwen free tier ample; fallback Mac Mini |
| Upload failures | Low | Low | Browser retry + manual fallback (Alpha) |
| Traffic algo change | Medium | High | Diversify sources; weekly keyword refresh |

---

### 6. Next Steps
1. Optimus review/approval
2. Escalate to Boss via Neo
3. On Go: Deploy etsy-workflow skill → Test pipeline → Launch

**Recommendation: GO** — Technically feasible, cost=£0 infra, high automation.

---

**Gate Decision:** PASS — KPIs defined, timeline executable, resources allocated.

-- Data (CTO)