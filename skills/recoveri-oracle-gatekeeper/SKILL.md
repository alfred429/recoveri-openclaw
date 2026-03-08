# Oracle Gatekeeper -- Cost Control Rules

Read this skill BEFORE routing any task to Oracle (Consultant).

## Why This Exists
Oracle runs on Claude Opus 4.6 at approximately $5/$25 per million tokens (input/output).
Other board agents run on DeepSeek at $0.28/$0.42 -- roughly 60x cheaper on output.
Oracle accounts for approximately 70% of total API spend.

## Mandatory Checklist (all must be YES to use Oracle)

1. Can Data, Alpha, or Kitt handle this on DeepSeek? -- If YES, route to them instead.
2. Does this require synthesis across 3+ independent data sources? -- If NO, do not use Oracle.
3. Does getting this wrong have significant financial consequences? -- If NO, do not use Oracle.
4. Has Boss or Optimus explicitly requested Oracle? -- If NO, use a cheaper agent.

If ANY answer is NO -- do not use Oracle. Route to the appropriate DeepSeek agent.

## Approved Oracle Tasks
- Etsy market research requiring trend analysis across multiple platforms and data sources
- Polymarket probability assessments requiring complex multi-factor reasoning
- UK regulatory analysis (FCA, GDPR) with financial risk implications
- Strategic decisions where the cost of a bad answer exceeds Oracle's token cost (~$0.50-2.00 per deep analysis)

## Never Use Oracle For
- Simple web searches or fact lookups (use Data or Alpha)
- Content drafting or copywriting (use Alpha)
- Operational questions or status checks (use Kitt)
- Code writing or reviews (use Data)
- Anything answerable in under 200 tokens (use any DeepSeek agent)
- Summarising single documents (use any DeepSeek agent)

## Two-Pass Research Pattern
For complex research, use this cheaper approach:
1. First pass: Route to a DeepSeek agent (Data or Alpha) for initial research and data gathering
2. Second pass: Only if synthesis is genuinely needed, route to Oracle with the gathered data
This typically saves 40-60% vs giving Oracle the raw research task.

## Cost Monitoring
- Oracle's target: under $27/month (roughly 1M output tokens)
- Each deep analysis costs approximately $0.50-2.00
- Kitt (acting CFO) tracks daily API spend
- If Oracle exceeds $1.00 in a single day, flag to Optimus
