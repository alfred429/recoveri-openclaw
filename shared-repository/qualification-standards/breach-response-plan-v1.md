# RECOVERI — Data Breach Response Plan v1.0
# GDPR Art. 33/34 Compliance
# Owner: Kitt (COO)
# Approved: 2026-03-18 (Boss via Cowork)
# Status: ACTIVE

## 1. Definition
A data breach is any security incident that leads to accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to personal data.

## 2. Detection
Breaches may be detected through:
- Error register alerts (error_type: security_breach or credential_leak)
- Kitt OS Review daily security dimension
- Agent self-reporting via escalation chain
- External notification (email, Etsy, Google)
- Boss observation

## 3. Response Timeline

| Step | Action | SLA | Owner |
|---|---|---|---|
| T+0 | Breach detected | Immediate | Any agent or Boss |
| T+15min | Contain: isolate affected system/credential | 15 minutes | Data (CTO) or nearest available agent |
| T+30min | Assess: determine scope, data affected, subjects impacted | 30 minutes | Kitt (COO) + Data (CTO) |
| T+1h | Notify Boss with: what happened, what data, how many subjects, containment status | 1 hour | Neo (CoS) via Telegram |
| T+4h | Document: full incident report in error register | 4 hours | Kitt (COO) |
| T+24h | Remediate: root cause fix deployed | 24 hours | Data (CTO) + Arthur |
| T+72h | Regulatory assessment: does ICO need notification? | 72 hours | Boss decision |
| T+72h | ICO notification if required (Art. 33) | 72 hours from detection | Boss |
| T+30d | Post-incident review: lessons learned via Gate 8 | 30 days | Kitt (COO) |

## 4. ICO Notification Criteria (Art. 33)
Notify ICO within 72 hours UNLESS the breach is unlikely to result in a risk to rights and freedoms. Notification required when:
- Personal data of external data subjects is exposed
- Financial or health data is involved
- Large volume of records affected
- Data could be used for identity fraud

Current assessment: LOW RISK — Recoveri currently processes primarily Boss's own data and public market data. No external client PII. ICO notification unlikely to be required at Wave 1.

## 5. Data Subject Notification (Art. 34)
Notify affected individuals without undue delay when breach is likely to result in HIGH risk to their rights and freedoms.

## 6. Incident Logging
All breaches logged in /root/error-register/ with:
- error_type: "security_breach" or "credential_leak"
- severity: "CRITICAL"
- Full incident details in message field
- Resolution steps and timeline

## 7. Previous Incidents
- 2026-03-18: Neo credential leak (GOG_KEYRING_PASSWORD in Telegram). Detected same session, contained within minutes, credential rotated, gog skill hardened (Rule 7). No personal data exposed. No ICO notification required.
- 2026-03-18: Anthropic API key exposure in openclaw.json defaults. Detected same session, key removed from defaults. No data breach — cost exposure only. No ICO notification required.

## 8. Review Schedule
This plan is reviewed:
- After every security incident
- Monthly as part of Kitt OS Review governance metrics
- At each Wave transition
