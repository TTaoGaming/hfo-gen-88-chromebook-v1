#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

if [[ "${HFO_PRECOMMIT_FAST_SUITE_FORCE:-}" == "1" ]]; then
  echo "[hfo] Pre-commit: forcing fast suite (HFO_PRECOMMIT_FAST_SUITE_FORCE=1)."
  exec npm run -s test:fast
fi

STAGED_FILES="$(git diff --cached --name-only)"
if [[ -z "$STAGED_FILES" ]]; then
  echo "[hfo] Pre-commit: no staged files; skipping fast suite."
  exit 0
fi

# Only run the expensive browser-based fast suite when staged changes could affect runtime behavior.
# Keep this conservative on low-RAM Chromebooks: prefer CI tripwires for broad browser coverage.

HEAVY_REGEX='^(
  active_.*\.(html|json)$
| playwright\.config\.ts$
| package\.json$
| tests/
| contracts/
| hfo_hub\.py$
| hfo_mcp_gateway_hub\.py$
| hfo_pointers\.(py|json)$
| hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/
| hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/
| scripts/.*\.spec\.ts$
| scripts/hfo_fast_check\.sh$
)'

if echo "$STAGED_FILES" | grep -Eqi "$HEAVY_REGEX"; then
  echo "[hfo] Pre-commit: running HFO fast suite (runtime-relevant staged files detected)."
  exec npm run -s test:fast
fi

echo "[hfo] Pre-commit: skipping HFO fast suite (no runtime-relevant staged files)."
exit 0
