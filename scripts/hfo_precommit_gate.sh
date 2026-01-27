#!/usr/bin/env bash
set -euo pipefail

if [[ "${SKIP_HFO_PRECOMMIT:-}" == "1" ]]; then
  echo "[hfo] Pre-commit: SKIP_HFO_PRECOMMIT=1; skipping."
  exit 0
fi

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

STAGED_FILES="$(git diff --cached --name-only)"

should_run_dino_classifier() {
  # Only run when staging changes likely to impact the Gen6 v9 Dino diagnostic path.
  # Intentionally avoid a bare "dino" match (e.g. Gen7 wrappers) to prevent false positives.
  # Also ignore reference assets (e.g. Gen7 reference images that include "omega_gen6" in filenames).
  echo "$STAGED_FILES" \
    | grep -Evi '/references/' \
    | grep -Eqi '(^|/)(gen6_v9|gen6_v10|omega_gen6_current|omega_gen6_v9|omega_gen6_v10|omega_gen6_v9_dino_diagnostics\.spec\.ts|hfo_gen6_v9_dino_classify\.sh)'
}

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

  echo "[hfo] Pre-commit: starting local server on :8889..."
  bash -c "$cmd" >/dev/null 2>&1 &
  SERVER_PID=$!

  for _ in {1..20}; do
    if is_port_open 8889; then
      return 0
    fi
    sleep 0.3
  done

  echo "[hfo] Pre-commit: server failed to start on :8889."
  return 1
}

cleanup() {
  if [[ -n "${SERVER_PID}" ]]; then
    kill "${SERVER_PID}" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

if ! should_run_dino_classifier; then
  echo "[hfo] Pre-commit: skipping Gen6 Dino classifier (no relevant staged files)."
  exit 0
fi

echo "[hfo] Pre-commit: running Gen6 Dino classifier (fail-closed)."
start_server_if_needed

export HFO_DIAG_REPEATS="${HFO_DIAG_REPEATS:-3}"
export HFO_DIAG_FAIL_CLOSED="${HFO_DIAG_FAIL_CLOSED:-true}"

npm run -s test:gen6:v9:dino:classify
