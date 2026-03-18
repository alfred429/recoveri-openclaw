# Recoveri Shared Repository
# Version: 1.0
# Created: 18 March 2026
# Reference: Process-Native Workforce Architecture v1.1, Section 3.5

## Purpose
The shared repository is Recoveri's institutional memory. Every sub-agent reads from it. Every execution writes to it. The repository grows smarter every cycle.

## Structure
shared-repository/
├── skills/                  Versioned skill definitions (master copies)
├── process-blueprints/      Versioned process definitions + gate specifications
├── artefacts/               Deliverables produced at each gate, organised by process_id
│   └── {process_id}/gate-{N}/
├── execution-logs/          Process-level execution records (what ran, cost, path)
├── lessons-learned/         Captured at Gate 8, feeds skill and process improvement
│   └── {process_id}/
└── qualification-standards/ Reference frameworks each skill is designed to match

## Relationship to Other Infrastructure
| System | Location | Purpose |
|--------|----------|---------|
| Operations logs | /root/operations-logs/ | Per-action JSONL |
| Request register | /root/request-register/ | REQ-ID lifecycle |
| Skill registry | /root/skill-registry/ | Deployed skill inventory |
| Error register | /root/error-register/ | Error tracking |
| Cost tracking | /root/cost-tracking/ | Token economics |
| **Shared repository** | /root/shared-repository/ | **Process-level memory** |

## Rules
1. **Process blueprints are versioned.** Never overwrite — create new version.
2. **Artefacts are immutable.** Once a gate produces an artefact, it stays.
3. **Lessons learned are curated.** Only high-signal insights. Not raw logs.
4. **Skills are master copies.** Deployed copies live in workspaces. Masters live here.
5. **Qualification standards are reference only.** They define what good looks like.
