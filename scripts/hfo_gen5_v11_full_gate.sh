#!/usr/bin/env bash
set -euo pipefail

# Medallion: Bronze | Mutation: 0% | HIVE: V

FILE=${1:-omega_gen5_v11.html}
PORT=${HFO_FAST_PORT:-8889}
ROOT="/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
SERVER_LOG="/tmp/hfo_gen5_v11_full_gate_server.log"
TEST_OUTPUT="/tmp/hfo_playwright_gen5_v11_full_gate"

BASE_PATH="hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/${FILE}"
BASE_FLAGS="flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true"

GEN5_URL="http://localhost:${PORT}/${BASE_PATH}?${BASE_FLAGS}"
GEN5_EXCALIDRAW_URL="${GEN5_URL}&flag-ui-excalidraw=true"
ENTRYPOINT_URL="http://localhost:${PORT}/active_hfo_omega_entrypoint.html?${BASE_FLAGS}"

CLIP_JSONL_DEFAULT="hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/replay/right-hand-idle-ready-commit-move-right-release-idle.from_clip.jsonl"
HFO_CLIP_JSONL=${HFO_CLIP_JSONL:-"$ROOT/$CLIP_JSONL_DEFAULT"}

SERVER_STARTED=false
SERVER_PID=""

cleanup() {
  if [[ "$SERVER_STARTED" == "true" ]] && [[ -n "$SERVER_PID" ]]; then
    kill "$SERVER_PID" >/dev/null 2>&1 || true
  fi
}

if curl -fsS "http://localhost:${PORT}/${BASE_PATH}" >/dev/null 2>&1; then
  echo "[gate] Server already running on :${PORT}"
else
  echo "[gate] Starting Gen5 server on :${PORT}"
  python3 "$ROOT/scripts/hfo_threaded_server.py" >"$SERVER_LOG" 2>&1 &
  SERVER_PID=$!
  SERVER_STARTED=true
  trap cleanup EXIT

  for _ in {1..30}; do
    if curl -fsS "http://localhost:${PORT}/${BASE_PATH}" >/dev/null 2>&1; then
      break
    fi
    sleep 0.5
  done
fi

echo "[gate] Entrypoint smoke"
HFO_ENTRYPOINT_URL="$ENTRYPOINT_URL" npx playwright test \
  scripts/omega_gen5_entrypoint_smoke.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

echo "[gate] Strict hex boot (v11)"
HFO_ENTRYPOINT_URL="$ENTRYPOINT_URL" npx playwright test \
  scripts/omega_gen5_v11_strict_hex.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

echo "[gate] Stigmergy surface (v11)"
HFO_GEN5_URL="$GEN5_URL" npx playwright test \
  scripts/omega_gen5_v11_stigmergy.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

echo "[gate] Readiness drain"
HFO_GEN5_URL="$GEN5_URL" npx playwright test \
  scripts/omega_gen5_readiness_drain.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

echo "[gate] Excalidraw ready"
HFO_GEN5_URL="$GEN5_EXCALIDRAW_URL" npx playwright test \
  scripts/omega_gen5_excalidraw_ready.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

echo "[gate] P1 ports smoke"
HFO_GEN5_URL="$GEN5_URL" npx playwright test \
  scripts/omega_gen5_p1_ports_smoke.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

echo "[gate] P7 navigate smoke"
HFO_GEN5_URL="$GEN5_URL" npx playwright test \
  scripts/omega_gen5_p7_navigate_smoke.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

echo "[gate] P4 disrupt smoke"
HFO_GEN5_URL="$GEN5_URL" npx playwright test \
  scripts/omega_gen5_p4_disrupt_smoke.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

echo "[gate] Clip replay"
HFO_GEN5_URL="$GEN5_URL" HFO_CLIP_JSONL="$HFO_CLIP_JSONL" npx playwright test \
  scripts/omega_clip_fsm_replay.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"

echo "[gate] PASS: Gen5 v11 full gate"
