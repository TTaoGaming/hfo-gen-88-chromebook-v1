#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

is_port_open() {
  local port="$1"
  if command -v nc >/dev/null 2>&1; then
    nc -z localhost "$port" >/dev/null 2>&1
  else
    (echo > /dev/tcp/127.0.0.1/"$port") >/dev/null 2>&1
  fi
}

SERVER_PID=""
start_server_if_needed() {
  if is_port_open 8889; then
    return 0
  fi

  local py="$ROOT_DIR/.venv/bin/python"
  local cmd="$py $ROOT_DIR/scripts/hfo_threaded_server.py"

  echo "[hfo] Starting local server on :8889 for Gen6 v9 Dino classifier..."
  bash -c "$cmd" >/dev/null 2>&1 &
  SERVER_PID=$!

  for _ in {1..20}; do
    if is_port_open 8889; then
      return 0
    fi
    sleep 0.3
  done

  echo "[hfo] Server failed to start on :8889."
  return 1
}

cleanup() {
  if [[ -n "${SERVER_PID}" ]]; then
    kill "${SERVER_PID}" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

start_server_if_needed

export HFO_DIAG_REPEATS="${HFO_DIAG_REPEATS:-3}"
export HFO_DIAG_FAIL_CLOSED="${HFO_DIAG_FAIL_CLOSED:-true}"

resolve_pointer() {
  local dotted_key="$1"
  local py="$ROOT_DIR/.venv/bin/python"
  if [[ ! -x "$py" ]]; then
    py="$(command -v python3 || true)"
  fi
  if [[ -z "$py" ]]; then
    return 1
  fi
  "$py" - <<PY
from hfo_pointers import get_pointer

val = get_pointer("$dotted_key", "")
if isinstance(val, str):
    print(val)
PY
}

GEN6_REL_PATH="${HFO_GEN6_REL_PATH:-$(resolve_pointer paths.gen6_runtime_html_default 2>/dev/null || true)}"
GEN6_REL_PATH="${GEN6_REL_PATH#/}"

# Default to pointer-resolved runtime (env override supported via HFO_GEN6_URL).
if [[ -n "$GEN6_REL_PATH" ]]; then
  export HFO_GEN6_URL="${HFO_GEN6_URL:-http://localhost:8889/${GEN6_REL_PATH}?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&flag-p3-dino-ready-edge=true&mode=dev}"
else
  export HFO_GEN6_URL="${HFO_GEN6_URL:-http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v10.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&flag-p3-dino-ready-edge=true&mode=dev}"
fi

HFO_PLAYWRIGHT_PROJECT="${HFO_PLAYWRIGHT_PROJECT:-chrome}"

npx playwright test scripts/omega_gen6_v9_dino_diagnostics.spec.ts --project="$HFO_PLAYWRIGHT_PROJECT" --workers=1 --grep "wrapper emits hfo:nematocyst:ack|replay seq01 correlates fsm_edge|stress seq01 correlation"
