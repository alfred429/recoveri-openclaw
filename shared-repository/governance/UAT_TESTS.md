# UAT Test Pack
# Date: 2026-03-29
# Purpose: Verify fixes and governance integrity before proceeding

---

## TEST 1: Gateway Service Health (Fix 1)

### T1.1 — Gateway service running
```bash
systemctl is-active openclaw-gateway.service
```
**Expected:** `active`

### T1.2 — Port 18789 owned by gateway
```bash
ss -tlnp | grep 18789
```
**Expected:** Shows openclaw-gateway process

### T1.3 — Port 18802 owned by gog
```bash
ss -tlnp | grep 18802
```
**Expected:** Shows gog process, NOT gmail-watcher

### T1.4 — gmail-watcher not running
```bash
systemctl list-units --type=service --all | grep gmail-watcher
```
**Expected:** No active service found (inactive/dead is OK, absent is better)

### T1.5 — Gateway responds to health check
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:18789/health
```
**Expected:** `200`

---

## TEST 2: L1 Smoke Test (Fix 2 — previously unverified)

### T2.1 — Ollama service running
```bash
systemctl is-active ollama.service 2>/dev/null || curl -s http://localhost:11434/api/tags | head -5
```
**Expected:** Service active OR API responds with model list

### T2.2 — Local model available
```bash
curl -s http://localhost:11434/api/tags | python3 -c "import sys,json; tags=json.load(sys.stdin); print([m['name'] for m in tags.get('models',[])])"
```
**Expected:** Lists available local models (e.g. qwen2.5:7b, qwen2.5:3b)

### T2.3 — L1 smoke test (basic completion)
```bash
curl -s http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:7b","messages":[{"role":"user","content":"Reply with exactly: SMOKE TEST PASS"}],"max_tokens":20}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('choices',[{}])[0].get('message',{}).get('content','FAIL'))"
```
**Expected:** Response containing `SMOKE TEST PASS` (or similar coherent response)

---

## TEST 3: Manifest Cleanup (Fix 3)

### T3.1 — No ENTERPRISE_SOUL references in manifest
```bash
grep -i "ENTERPRISE_SOUL" /root/.openclaw/manifest.json 2>/dev/null | grep -v "^[[:space:]]*#" | grep -v "^[[:space:]]*\/\/"
```
**Expected:** No output (no non-comment references)

### T3.2 — No SHARED_SOUL references in manifest
```bash
grep -i "SHARED_SOUL" /root/.openclaw/manifest.json 2>/dev/null | grep -v "^[[:space:]]*#" | grep -v "^[[:space:]]*\/\/"
```
**Expected:** No output

### T3.3 — No tier-map references in manifest
```bash
grep -i "tier-map" /root/.openclaw/manifest.json 2>/dev/null | grep -v "^[[:space:]]*#" | grep -v "^[[:space:]]*\/\/"
```
**Expected:** No output

### T3.4 — Manifest line count
```bash
wc -l /root/.openclaw/manifest.json
```
**Expected:** ~290 lines

---

## TEST 4: AGENTS.md Hash Consistency

### T4.1 — All 10 active agents share same AGENTS.md
```bash
for agent in main ceo-agent cto-agent cro-agent coo-agent consultant-agent qwen-1 qwen-2 qwen-3 qwen-4; do
  f="/root/.openclaw/workspaces/${agent}/AGENTS.md"
  if [ -f "$f" ]; then
    hash=$(md5sum "$f" | awk '{print $1}')
    printf "%-25s %s\n" "$agent" "$hash"
  else
    printf "%-25s MISSING\n" "$agent"
  fi
done
```
**Expected:** All 10 show identical hash (da8ba9580639c5027c90eb6cbc506264)

### T4.2 — Mozart retired workspace is the only outlier
```bash
md5sum /root/.openclaw/workspaces/mozart-agent-retired*/AGENTS.md 2>/dev/null
```
**Expected:** Different hash from active agents, or file not found

---

## TEST 5: Legacy Skill-Sync Path (Nuance Flag)

### T5.1 — Check task-router copies in agent dirs
```bash
for agent in main ceo-agent cto-agent cro-agent coo-agent consultant-agent qwen-1 qwen-2 qwen-3 qwen-4; do
  f="/root/.openclaw/agents/${agent}/agent/skills/altior-task-router/SKILL.md"
  if [ -f "$f" ]; then
    hash=$(md5sum "$f" | awk '{print $1}')
    printf "%-25s %s EXISTS\n" "$agent" "$hash"
  else
    printf "%-25s NOT FOUND\n" "$agent"
  fi
done
```
**Expected:** Document which agents have copies. Note: this is a live behaviour-sync path, not just clutter.

### T5.2 — Compare agent-dir router vs workspace router
```bash
diff /root/.openclaw/agents/main/agent/skills/altior-task-router/SKILL.md \
     /root/.openclaw/workspaces/main/skills/altior-task-router/SKILL.md 2>/dev/null && echo "MATCH" || echo "DIFFER or missing"
```
**Expected:** Document whether they match. Divergence = drift risk.

---

## TEST 6: Governance Sync Map Readiness

### T6.1 — Sync map exists
```bash
[ -f /root/shared-repository/governance/GOVERNANCE_SYNC_MAP.md ] && echo "EXISTS" || echo "MISSING"
```
**Expected:** EXISTS

### T6.2 — Current SOUL sizes vs target
```bash
echo "Target: shared block + role block < 2500 chars per agent"
echo "Current sizes:"
for agent in main ceo-agent cto-agent cro-agent coo-agent consultant-agent qwen-1 qwen-2 qwen-3 qwen-4; do
  f="/root/.openclaw/workspaces/${agent}/SOUL.md"
  chars=$(wc -c < "$f" 2>/dev/null || echo "0")
  printf "  %-25s %6s chars\n" "$agent" "$chars"
done
```
**Expected:** Shows current sizes for comparison against 2,500 char target post-deployment.

---

## Run All Tests

```bash
# Quick runner — paste this block to run all tests sequentially
echo "=== T1: Gateway ===" && \
systemctl is-active openclaw-gateway.service && \
ss -tlnp | grep -E "18789|18802" && \
echo "=== T2: Ollama ===" && \
curl -s http://localhost:11434/api/tags | python3 -c "import sys,json; tags=json.load(sys.stdin); print([m['name'] for m in tags.get('models',[])])" 2>/dev/null || echo "Ollama not responding" && \
echo "=== T3: Manifest ===" && \
echo "ENTERPRISE_SOUL refs: $(grep -ci 'ENTERPRISE_SOUL' /root/.openclaw/manifest.json 2>/dev/null || echo 0)" && \
echo "SHARED_SOUL refs: $(grep -ci 'SHARED_SOUL' /root/.openclaw/manifest.json 2>/dev/null || echo 0)" && \
echo "Manifest lines: $(wc -l < /root/.openclaw/manifest.json 2>/dev/null || echo 0)" && \
echo "=== T4: AGENTS.md ===" && \
for a in main ceo-agent cto-agent cro-agent coo-agent consultant-agent qwen-1 qwen-2 qwen-3 qwen-4; do printf "%-25s %s\n" "$a" "$(md5sum /root/.openclaw/workspaces/$a/AGENTS.md 2>/dev/null | awk '{print $1}')"; done && \
echo "=== DONE ==="
```

---

## Pass Criteria

| Test | Pass |
|------|------|
| T1 (Gateway) | All 5 sub-tests pass |
| T2 (Smoke) | Ollama responds, model listed, completion returns |
| T3 (Manifest) | Zero non-comment references to stale docs |
| T4 (AGENTS.md) | All 10 hashes identical |
| T5 (Skill-sync) | Documented — not blocking but tracked |
| T6 (Sync map) | File exists, current sizes documented |

**All T1-T4 must pass before governance deployment proceeds.**
