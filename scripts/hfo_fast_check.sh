#!/usr/bin/env bash
set -euo pipefail

PORT=${HFO_FAST_PORT:-8889}
ROOT="/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
SERVER_LOG="/tmp/hfo_fast_server.log"
TEST_OUTPUT="/tmp/hfo_playwright_fast"

# The repo Playwright config uses a "chrome" project (system chrome).
# Allow override for other environments.
HFO_PLAYWRIGHT_PROJECT="${HFO_PLAYWRIGHT_PROJECT:-chrome}"

python3 "$ROOT/scripts/hfo_threaded_server.py" >"$SERVER_LOG" 2>&1 &
SERVER_PID=$!

cleanup() {
  kill "$SERVER_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

# Wait for server
server_ready=0
for _ in {1..20}; do
  if curl -fsS "http://localhost:${PORT}/active_hfo_omega_entrypoint.html" >/dev/null 2>&1; then
    server_ready=1
    break
  fi
  sleep 0.5
done

if [[ "$server_ready" != "1" ]]; then
  echo "[hfo-fast] server failed to become ready on :${PORT}"
  if [[ -f "$SERVER_LOG" ]]; then
    echo "[hfo-fast] server log tail:"
    tail -n 80 "$SERVER_LOG" || true
  fi
  exit 1
fi

PLAYWRIGHT_COMMON_ARGS=(
  --project="$HFO_PLAYWRIGHT_PROJECT"
  --workers=1
  --reporter=line
  --output="$TEST_OUTPUT"
  --timeout=15000
  --global-timeout=180000
)

npx playwright test \
  scripts/omega_gen5_readiness_drain.spec.ts \
  scripts/omega_gen5_excalidraw_ready.spec.ts \
  "${PLAYWRIGHT_COMMON_ARGS[@]}"
