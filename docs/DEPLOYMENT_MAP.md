# Recoveri Deployment Map — Repo → VPS

## How to Deploy from GitHub to VPS

```bash
cd /root/recoveri-openclaw
git pull origin main
```

## File → Workspace Mapping

| Repo File | VPS Destination(s) | Notes |
|-----------|-------------------|-------|
| config/openclaw.json | /root/.openclaw/openclaw.json | Main config — restart gateway after update |
| souls/ENTERPRISE_SOUL.md | /root/.openclaw/workspaces/*/shared/ENTERPRISE_SOUL.md | Deploy to ALL 6 workspaces |
| souls/SOUL_neo.md | /root/.openclaw/workspaces/main/SOUL.md | Neo (CoS) |
| souls/SOUL_optimus.md | /root/.openclaw/workspaces/ceo-agent/SOUL.md | Optimus (CEO) |
| souls/SOUL_data.md | /root/.openclaw/workspaces/cto-agent/SOUL.md | Data (CTO) |
| souls/SOUL_alpha.md | /root/.openclaw/workspaces/cro-agent/SOUL.md | Alpha (CRO) |
| souls/SOUL_kitt.md | /root/.openclaw/workspaces/coo-agent/SOUL.md | Kitt (COO) |
| souls/SOUL_oracle.md | /root/.openclaw/workspaces/consultant-agent/SOUL.md | Oracle (Consultant) |
| skills/{name}/SKILL.md | /root/.openclaw/workspaces/*/skills/{name}/SKILL.md | Deploy to all 6 + global |
| skills/{name}/SKILL.md | /root/.openclaw/skills/{name}/SKILL.md | Global copy |
| governance/AGENTS.md | /root/.openclaw/workspaces/*/AGENTS.md | Bootstrap file |
| governance/USER.md | /root/.openclaw/workspaces/*/USER.md | Bootstrap file |

## Post-Deployment Checklist

1. Verify files match: `md5sum` repo vs VPS
2. Send session resets to affected agents via Telegram (natural language, no `/new`)
3. Run smoke tests for any changed SOULs or skills
4. Log deployment in operations log with REQ reference
