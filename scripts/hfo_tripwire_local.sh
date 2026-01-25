#!/usr/bin/env bash
set -euo pipefail

# Medallion: Bronze | Mutation: 0% | HIVE: V
# Local tripwire: keep this lightweight to avoid Chromebook OOM.
# CI runs the heavier browser tripwires when relevant.

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

echo "[tripwire] Local lightweight checks"
python3 -V
npm -v

# Strict health + preflight without Playwright.
npm run -s hfo:health:strict
npm run -s p5:preflight

echo "[tripwire] OK"
