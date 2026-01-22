#!/usr/bin/env bash
set -euo pipefail

PORT=${HFO_FAST_PORT:-8889}
ROOT="/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
SERVER_LOG="/tmp/hfo_fast_server.log"
TEST_OUTPUT="/tmp/hfo_playwright_fast"

python3 "$ROOT/scripts/hfo_threaded_server.py" >"$SERVER_LOG" 2>&1 &
SERVER_PID=$!

cleanup() {
  kill "$SERVER_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

# Wait for server
for _ in {1..20}; do
  if curl -fsS "http://localhost:${PORT}/active_hfo_omega_entrypoint.html" >/dev/null 2>&1; then
    break
  fi
  sleep 0.5
done

npx playwright test \
  scripts/omega_gen5_readiness_drain.spec.ts \
  scripts/omega_gen5_excalidraw_ready.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"
