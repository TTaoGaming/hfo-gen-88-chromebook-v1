#!/usr/bin/env bash
set -euo pipefail

# Medallion: Bronze | Mutation: 0% | HIVE: V

FILE=${1:-}
if [[ -z "$FILE" ]]; then
  echo "Usage: $0 <omega_gen5_file.html>" >&2
  exit 2
fi

PORT=${HFO_FAST_PORT:-8889}
ROOT="/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
SERVER_LOG="/tmp/hfo_gen5_smoke_server.log"
TEST_OUTPUT="/tmp/hfo_playwright_gen5_smoke"

BASE_PATH="hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/${FILE}"
BASE_FLAGS="flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true"

READINESS_URL="http://localhost:${PORT}/${BASE_PATH}?${BASE_FLAGS}"
EXCALIDRAW_URL="${READINESS_URL}&flag-ui-excalidraw=true"

RUN_P1_PORTS_SMOKE=${HFO_GEN5_RUN_P1_PORTS_SMOKE:-false}
RUN_P7_NAV_SMOKE=${HFO_GEN5_RUN_P7_NAV_SMOKE:-false}
RUN_P4_DISRUPT_SMOKE=${HFO_GEN5_RUN_P4_DISRUPT_SMOKE:-false}

python3 "$ROOT/scripts/hfo_threaded_server.py" >"$SERVER_LOG" 2>&1 &
SERVER_PID=$!

cleanup() {
  kill "$SERVER_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

# Wait for server (probe the requested Gen5 artifact path)
for _ in {1..20}; do
  if curl -fsS "http://localhost:${PORT}/${BASE_PATH}" >/dev/null 2>&1; then
    break
  fi
  sleep 0.5
done

HFO_GEN5_URL="$READINESS_URL" npx playwright test \
  scripts/omega_gen5_readiness_drain.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

HFO_GEN5_URL="$EXCALIDRAW_URL" npx playwright test \
  scripts/omega_gen5_excalidraw_ready.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

if [[ "$RUN_P1_PORTS_SMOKE" == "true" ]]; then
  P1_PORTS_URL="${READINESS_URL}&flag-p1-ports=true"
  HFO_GEN5_URL="$P1_PORTS_URL" npx playwright test \
    scripts/omega_gen5_p1_ports_smoke.spec.ts \
    --project=chromium \
    --output="$TEST_OUTPUT"
fi

if [[ "$RUN_P7_NAV_SMOKE" == "true" ]]; then
  HFO_GEN5_URL="$READINESS_URL" npx playwright test \
    scripts/omega_gen5_p7_navigate_smoke.spec.ts \
    --project=chromium \
    --output="$TEST_OUTPUT"
fi

if [[ "$RUN_P4_DISRUPT_SMOKE" == "true" ]]; then
  P4_URL="${READINESS_URL}&flag-p4-disrupt=true"
  HFO_GEN5_URL="$P4_URL" npx playwright test \
    scripts/omega_gen5_p4_disrupt_smoke.spec.ts \
    --project=chromium \
    --output="$TEST_OUTPUT"
fi
