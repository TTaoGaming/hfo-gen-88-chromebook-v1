#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
SERVER_CMD="$PYTHON_BIN $ROOT_DIR/scripts/hfo_threaded_server.py"
SERVER_PID=""

is_port_open() {
  local port="$1"
  if command -v nc >/dev/null 2>&1; then
    nc -z localhost "$port" >/dev/null 2>&1
  else
    (echo > /dev/tcp/127.0.0.1/"$port") >/dev/null 2>&1
  fi
}

start_server_if_needed() {
  if is_port_open 8889; then
    return 0
  fi

  echo "[hfo] Starting local server on :8889 for regression..."
  bash -c "$SERVER_CMD" >/dev/null 2>&1 &
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

cd "$ROOT_DIR"

npm run test:omega:fast
