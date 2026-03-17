# Recoveri Token Cost Tracking — Schema
# Version: 1.0
# Milestone: FM8 (Token Economics & Model Intelligence)
# Owner: Kitt (COO) + Data (CTO)

## Overview

Cost tracking extracts token usage from operations-logs and calculates daily spend per agent, per model, per pillar. This feeds the Boss Dashboard (FM10) cost section and Kitt OS Review efficiency dimensions.

## Daily Cost Summary Script

Run daily (ideally as part of Kitt OS Review):

```bash
bash /root/cost-tracking/daily_cost_summary.sh [YYYY-MM-DD]
```

## Cost Estimation (reference rates — read from config, NOT hardcoded)

Cost rates are maintained in `/root/cost-tracking/rates.json`. Update when models or pricing change. The daily cost summary script reads rates from this config file — never hardcode prices in scripts.

## Budget Constraints

- Monthly ceiling: read from rates.json `budget.monthly_ceiling_gbp`
- Monthly target: read from rates.json `budget.monthly_target_gbp`
- Oracle ceiling: read from rates.json `budget.oracle_ceiling_usd`
- Free tier: Qwen 1M tokens/day — maximise usage to reduce paid model spend
