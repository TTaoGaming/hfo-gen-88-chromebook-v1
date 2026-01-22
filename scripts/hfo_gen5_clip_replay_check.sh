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
SERVER_LOG="/tmp/hfo_gen5_clip_server.log"
TEST_OUTPUT="/tmp/hfo_playwright_gen5_clip"

BASE_PATH="hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/${FILE}"
BASE_FLAGS="flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true"

GEN5_URL="http://localhost:${PORT}/${BASE_PATH}?${BASE_FLAGS}"

# Default to the MP4-derived golden clip JSONL (meta.source points to the archived MP4).
CLIP_JSONL_DEFAULT="hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/replay/right-hand-idle-ready-commit-move-right-release-idle.from_clip.jsonl"
HFO_CLIP_JSONL=${HFO_CLIP_JSONL:-"$ROOT/$CLIP_JSONL_DEFAULT"}

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

HFO_GEN5_URL="$GEN5_URL" HFO_CLIP_JSONL="$HFO_CLIP_JSONL" npx playwright test \
  scripts/omega_clip_fsm_replay.spec.ts \
  --project=chromium \
  --output="$TEST_OUTPUT"
