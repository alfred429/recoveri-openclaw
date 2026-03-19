# RECOVERI Tier Map
# Maintained by Optimus via model-router-governance skill
# Updated as part of every model change execution protocol
# Last change: 2026-03-16 — initial setup
## Tier Definitions
| Tier | Label | Provider/Model | Notes |
|------|-------|---------------|-------|
| 0 | LOCAL_FREE | Mac Mini local (Claude Code, ChatGPT 5) | Zero API cost, managed by Oracle via bridge |
| 0 | CRON_FREE | qwen/qwen-turbo (1M tokens/day free) | Background/cron tasks only |
| 1 | PREMIUM | (not assigned — reserved for future budget) | |
| 1.5 | ELEVATED | (not assigned — reserved for future budget) | |
| 2 | OPERATIONAL | xai/grok-4-1-fast | Standard working tier, primary for all VPS agents |
| 3 | ECONOMY | deepseek/deepseek-chat | Fallback model, activates on primary failure |
## Agent Assignments
| Agent | Agent ID | Tier | Primary Model | Fallback | Notes |
|-------|----------|------|--------------|----------|-------|
| Neo (CoS) | main | OPERATIONAL | As per openclaw.json | ECONOMY | Intake + routing |
| Optimus (CEO) | ceo-agent | OPERATIONAL | As per openclaw.json | ECONOMY | Strategy + orchestration |
| Data (CTO) | cto-agent | OPERATIONAL | As per openclaw.json | ECONOMY | Technology + product |
| Alpha (CRO) | cro-agent | OPERATIONAL | As per openclaw.json | ECONOMY | Commercial + growth |
| Kitt (COO) | coo-agent | OPERATIONAL | As per openclaw.json | ECONOMY | Operations + enterprise services |
| Oracle (Consultant) | consultant-agent | OPERATIONAL | As per openclaw.json | ECONOMY | VPS side; also manages LOCAL_FREE via bridge |
## Free Tier Allocation
| Tier | Daily Limit | Used For | Managed By |
|------|-------------|----------|------------|
| LOCAL_FREE | Unlimited (Mac Mini compute) | Complex research, prototyping, code review | Oracle (bridge foreman) |
| CRON_FREE | 1M tokens/day (Qwen) | Daily OS Review, monitoring, background scans | Kitt (cron owner) + Data (config) |
## Budget Reference
Monthly target: check with Kitt for live figure
This file is updated by Optimus after every approved model change via the model-router-governance skill.
Source of truth for runtime config: openclaw.json
Source of truth for tier labels: this file
