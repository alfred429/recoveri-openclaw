# Skill: recoveri-localisation-gemma
## Version: 1.0
## Model: gemma3:4b (Ollama local)
## Tier: CRON_FREE
## Owner: Qwen 3 (Content) / Alpha (CRO)

## Purpose
Translate and localise Recoveri documents, product listings, and customer-facing content across all target markets using Gemma 3 4B.

## Target Markets
- en-GB (source)
- en-US (US English localisation)
- fr (French)
- de (German)
- es (Spanish)
- nl (Dutch)
- it (Italian)

## Invocation
```bash
python3 /root/shared-repository/scripts/localise.py --doc <path> --lang <code>
python3 /root/shared-repository/scripts/localise.py --doc <path> --lang all
```

## Quality Standards
- Professional commercial tone appropriate to target market
- Legal/policy language compliant with target country regulations
- Currency symbols localised
- Brand names preserved (RecoveriStudio, Recoveri)
- Markdown formatting preserved
- Output verified by word count comparison (80-120% of source)

## Output Location
/root/shared-repository/data/localisation/

## Logging
Every translation logged to localisation-log.jsonl.
