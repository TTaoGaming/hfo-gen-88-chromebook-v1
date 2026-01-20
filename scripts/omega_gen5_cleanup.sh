#!/usr/bin/env bash
# Medallion: Bronze | Mutation: 0% | HIVE: V
# Omega Gen5 cleanup utility (local)
set -euo pipefail

PROJECT_ROOT="/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
LOG_FILE="/tmp/hfo_threaded_server.log"

stop_server() {
  if pgrep -f "scripts/hfo_threaded_server.py" >/dev/null 2>&1; then
    echo "[cleanup] Stopping HFO threaded server"
    pkill -f "scripts/hfo_threaded_server.py" || true
  fi
}

cleanup_logs() {
  if [[ -f "${LOG_FILE}" ]]; then
    echo "[cleanup] Removing ${LOG_FILE}"
    rm -f "${LOG_FILE}"
  fi
}

cleanup_test_results() {
  local results_dir="${PROJECT_ROOT}/test-results"
  if [[ -d "${results_dir}" ]]; then
    echo "[cleanup] Removing omega-related test results"
    find "${results_dir}" -maxdepth 1 -type d -name "omega_*" -prune -exec rm -rf {} +
  fi

  if [[ "${CLEAN_ALL:-0}" == "1" ]]; then
    echo "[cleanup] Removing playwright-report"
    rm -rf "${PROJECT_ROOT}/playwright-report"
  fi
}

stop_server
cleanup_logs
cleanup_test_results

echo "[cleanup] Done"
