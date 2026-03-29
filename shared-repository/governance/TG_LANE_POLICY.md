# Telegram Lane Policy
# Source: G, Boss-approved
# Date: 2026-03-29
# Status: APPROVED — ready for implementation

---

## Lane Map

| Topic | Lane | Bound Agent | Instruction Source | Who May Post | Result Path | requireMention |
|---|---|---|---|---|---|---|
| 1 | Neo intake | Neo | Boss | Boss, Neo | Neo -> Optimus or direct reply if trivial | false |
| 2 | Reports | Optimus | Boss, Neo, directors | Optimus, directors | final synthesis / board reporting | true |
| 3 | TECH working | Data | Boss, Neo, Optimus | Boss, Data | Data -> Boss/Optimus, Data -> Bolt via 625 | false |
| 6 | CSM working | Alpha | Boss, Neo, Optimus | Boss, Alpha | Alpha -> Boss/Optimus, Alpha -> Pixel via 627 | false |
| 8 | OPS working | Kitt | Boss, Neo, Optimus | Boss, Kitt | Kitt -> Boss/Optimus, Kitt -> Scout via 12 | false |
| 10 | R&D working | Oracle | Boss, Neo, Optimus | Boss, Oracle | Oracle -> Boss/Optimus, Oracle -> Sage via 14 | false |
| 625 | TECH worker | Bolt | Data, Boss | Data, Bolt, Boss | Bolt -> Data first, direct post only if explicitly delegated | true |
| 627 | CSM worker | Pixel | Alpha, Boss | Alpha, Pixel, Boss | Pixel -> Alpha first, direct post only if explicitly delegated | true |
| 12 | OPS worker | Scout | Kitt, Boss | Kitt, Scout, Boss | Scout -> Kitt first, direct post only if explicitly delegated | true |
| 14 | R&D worker | Sage | Oracle, Boss | Oracle, Sage, Boss | Sage -> Oracle first, direct post only if explicitly delegated | true |

---

## Rules

- Directors own decisions and board-facing communication.
- Workers own execution, not independent decision-making.
- Worker lanes are execution lanes, not open discussion lanes.
- Workers only act on instructions from their supervisor or Boss.
- Default worker return path is back to supervisor.
- Direct worker posting is exception-based, not normal mode.
- Reports lane is for synthesis and final reporting, not task intake.

---

## Topic Prompt Intent

For worker lanes (625/627/12/14), the topic prompt should say:

- Supervisor-mediated execution lane
- Act only on instructions from supervisor or Boss
- Ignore unrelated chatter
- Return results to supervisor unless explicitly asked to post final output here

---

## Config Recommendation

| Lane type | requireMention |
|-----------|---------------|
| Working lanes (1/3/6/8/10) | false |
| Worker lanes (625/627/12/14) | true |
| Reports lane (2) | true |

---

## Implementation Targets

This policy needs to be reflected in:

1. `openclaw.json` — topic bindings, requireMention per topic
2. `AGENTS.md` — per-agent lane ownership and posting rules
3. Router skill — lane-aware routing guidance
4. Topic prompts in `openclaw.json` — worker lane prompt text
