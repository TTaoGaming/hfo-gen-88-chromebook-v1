#!/usr/bin/env bash
# Medallion: Bronze | Mutation: 0% | HIVE: V
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PIDFILE="${HFO_SERVER_PIDFILE:-/tmp/hfo_threaded_server.pid}"
LOGFILE="${HFO_SERVER_LOGFILE:-/tmp/hfo_threaded_server.log}"
PORT="${HFO_SERVER_PORT:-8889}"
PYTHON_BIN="${HFO_SERVER_PYTHON:-python3}"

SERVER_CMD=("${PYTHON_BIN}" "${ROOT}/scripts/hfo_threaded_server.py")

usage() {
  cat <<EOF
Usage: $0 <start|ensure|stop|restart|status|tail>

Env overrides:
  HFO_SERVER_PIDFILE   (default: ${PIDFILE})
  HFO_SERVER_LOGFILE   (default: ${LOGFILE})
  HFO_SERVER_PORT      (default: ${PORT})
  HFO_SERVER_PYTHON    (default: ${PYTHON_BIN})
EOF
}

pid_running() {
  if [[ ! -f "${PIDFILE}" ]]; then
    return 1
  fi
  local pid
  pid="$(cat "${PIDFILE}" 2>/dev/null || true)"
  [[ -n "${pid}" ]] || return 1
  kill -0 "${pid}" 2>/dev/null
}

wait_for_listen() {
  local attempts="${1:-60}" # ~6s at 0.1s
  for _ in $(seq 1 "${attempts}"); do
    if curl -fsS "http://localhost:${PORT}/" >/dev/null 2>&1; then
      return 0
    fi
    sleep 0.1
  done
  return 1
}

start_server() {
  if pid_running; then
    echo "HFO Omega server already running (pid=$(cat "${PIDFILE}"))"
    return 0
  fi

  rm -f "${PIDFILE}"

  mkdir -p "$(dirname "${LOGFILE}")" >/dev/null 2>&1 || true

  nohup "${SERVER_CMD[@]}" >"${LOGFILE}" 2>&1 &
  echo $! >"${PIDFILE}"

  if wait_for_listen 80; then
    echo "HFO Omega server started (pid=$(cat "${PIDFILE}")) on :${PORT}"
    return 0
  fi

  echo "HFO Omega server failed to become ready on :${PORT}." >&2
  echo "Log tail: ${LOGFILE}" >&2
  tail -n 50 "${LOGFILE}" 2>/dev/null || true
  return 1
}

stop_server() {
  if ! [[ -f "${PIDFILE}" ]]; then
    echo "HFO Omega server not running (no pidfile: ${PIDFILE})"
    return 0
  fi

  local pid
  pid="$(cat "${PIDFILE}" 2>/dev/null || true)"
  if [[ -z "${pid}" ]]; then
    rm -f "${PIDFILE}"
    echo "HFO Omega server not running (empty pidfile)."
    return 0
  fi

  if ! kill -0 "${pid}" 2>/dev/null; then
    rm -f "${PIDFILE}"
    echo "HFO Omega server not running (stale pid=${pid})."
    return 0
  fi

  kill "${pid}" 2>/dev/null || true

  # Wait a bit for clean shutdown.
  for _ in $(seq 1 50); do
    if ! kill -0 "${pid}" 2>/dev/null; then
      rm -f "${PIDFILE}"
      echo "HFO Omega server stopped (pid=${pid})"
      return 0
    fi
    sleep 0.1
  done

  echo "HFO Omega server did not stop gracefully; sending SIGKILL (pid=${pid})" >&2
  kill -9 "${pid}" 2>/dev/null || true
  rm -f "${PIDFILE}"
  return 0
}

status_server() {
  if pid_running; then
    local pid
    pid="$(cat "${PIDFILE}")"
    local code
    code="$(curl -fsS -o /dev/null -w '%{http_code}' "http://localhost:${PORT}/" 2>/dev/null || true)"
    echo "HFO Omega server: RUNNING pid=${pid} port=${PORT} http=${code:-n/a}"
    return 0
  fi
  echo "HFO Omega server: STOPPED (pidfile=${PIDFILE})"
  return 0
}

tail_log() {
  if [[ -f "${LOGFILE}" ]]; then
    tail -n 80 "${LOGFILE}"
  else
    echo "No log file: ${LOGFILE}"
  fi
}

cmd="${1:-}"
case "${cmd}" in
  start)
    start_server
    ;;
  ensure)
    start_server
    ;;
  stop)
    stop_server
    ;;
  restart)
    stop_server
    start_server
    ;;
  status)
    status_server
    ;;
  tail)
    tail_log
    ;;
  -h|--help|help|"" )
    usage
    exit 0
    ;;
  *)
    echo "Unknown command: ${cmd}" >&2
    usage >&2
    exit 2
    ;;
esac
