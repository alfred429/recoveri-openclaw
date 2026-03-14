#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "[1/5] Ensuring runtime directories exist"
mkdir -p credentials logs backups media telegram memory

echo "[2/5] Ensuring local workspace runtime dirs exist"
mkdir -p workspaces/main/.openclaw
find workspaces -maxdepth 2 -type d -name ".openclaw" >/dev/null 2>&1 || true

echo "[3/5] Installing local git hooks"
bash scripts/install-git-hooks.sh

echo "[4/5] Verifying core files"
test -f openclaw.json && echo "[OK] openclaw.json present" || echo "[WARN] openclaw.json missing"
test -f REPO_GOVERNANCE.md && echo "[OK] governance present" || echo "[WARN] governance missing"
test -f ARCHITECTURE.md && echo "[OK] architecture present" || echo "[WARN] architecture missing"

echo "[5/5] Bootstrap complete"
echo "Review .env, credentials/, and local runtime state before starting services."
