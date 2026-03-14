#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

mkdir -p .githooks
git config core.hooksPath .githooks

echo "[OK] Git hooks path set to .githooks"
