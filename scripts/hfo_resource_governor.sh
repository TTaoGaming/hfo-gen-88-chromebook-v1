#!/usr/bin/env bash
# Medallion: Bronze | Mutation: 0% | HIVE: V
# Resource governance helper for crash-prone environments.
#
# Goals:
# - Stop/trim known background daemons that can destabilize VS Code + Playwright.
# - Kill stray Playwright/Chromium processes after runs.
# - Keep behavior explicit and fail-soft (never blocks your workflow by default).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

MODE="${1:-status}"

# Profiles control what gets stopped.
# - crash_safe: stop nonessential daemons and browsers
# - full_stop: additionally stop omega server
PROFILE="${HFO_GOV_PROFILE:-crash_safe}"

DRY_RUN=0
if [[ "${MODE}" == "--dry-run" ]]; then
  DRY_RUN=1
  MODE="status"
fi

say() { echo "[governor] $*"; }

run() {
  if [[ "${DRY_RUN}" == "1" ]]; then
    say "DRY_RUN: $*"
    return 0
  fi
  # shellcheck disable=SC2068
  "$@" || true
}

show_status() {
  say "profile=${PROFILE}"
  say "uptime: $(uptime || true)"
  say "mem:"; (free -h || true) | sed 's/^/[governor] /'
  say "top cpu:"; (ps -eo pid,ppid,cmd,%cpu,%mem --sort=-%cpu | head -n 12 || true) | sed 's/^/[governor] /'

  say "matching processes (non-fatal):"
  (ps -ef | grep -E "scripts/(p5_sentinel_daemon|hfo_stigmergy_anchor|hfo_resource_shepherd_daemon|hfo_gitops_batcher|hfo_threaded_server)\.py|playwright|chromium|chrome" | grep -v grep || true) | sed 's/^/[governor] /'
}

dedupe_daemons() {
  # If VS Code tasks re-spawn or terminals are reopened, we can end up with duplicated daemons.
  # This reduces the pile-up without requiring perfect task orchestration.
  say "deduping known daemons (keep at most 1 instance each)"

  local patterns=(
    "scripts/p5_sentinel_daemon.py"
    "scripts/hfo_stigmergy_anchor.py"
    "scripts/hfo_resource_shepherd_daemon.py"
  )

  for pat in "${patterns[@]}"; do
    local pids
    pids="$(pgrep -f "${pat}" || true)"
    if [[ -z "${pids}" ]]; then
      continue
    fi

    # Keep the lowest PID (oldest process) and terminate the rest.
    local keep
    keep="$(echo "${pids}" | tr ' ' '\n' | sort -n | head -n 1)"
    local kill_list
    kill_list="$(echo "${pids}" | tr ' ' '\n' | sort -n | tail -n +2)"
    if [[ -n "${kill_list}" ]]; then
      say "keeping ${pat} pid=${keep}; terminating duplicates: $(echo "${kill_list}" | tr '\n' ' ')"
      while read -r pid; do
        [[ -n "${pid}" ]] || continue
        run kill "${pid}"
      done <<< "${kill_list}"
    fi
  done
}

kill_browsers() {
  say "stopping stray browsers/playwright"

  # Be careful with `pkill -f chromium`: our own test runner often includes
  # `--project=chromium` in argv, which would self-terminate. Prefer exact
  # process-name matches and targeted Playwright cache-path matches.
  run pkill -x playwright || true
  run pkill -x chromium || true
  run pkill -f "chromium-browser" || true
  run pkill -x chrome || true
  run pkill -x headless_shell || true

  # Playwright-bundled browser binaries typically live under ms-playwright.
  run pkill -f "ms-playwright" || true
}

stop_background_daemons() {
  say "stopping known HFO background daemons"
  run pkill -f scripts/p5_sentinel_daemon.py
  run pkill -f scripts/hfo_stigmergy_anchor.py
  run pkill -f scripts/hfo_resource_shepherd_daemon.py
  run pkill -f scripts/hfo_gitops_batcher.py
}

stop_omega_server() {
  say "stopping omega server (if running)"
  run bash "${ROOT}/scripts/hfo_omega_server_ctl.sh" stop
  run pkill -f scripts/hfo_threaded_server.py
}

case "${MODE}" in
  status)
    show_status
    ;;

  dedupe)
    dedupe_daemons
    show_status
    ;;

  pretest)
    # Keep omega server up by default, but clear the noisy/background daemons.
    dedupe_daemons
    stop_background_daemons
    kill_browsers
    show_status
    ;;

  posttest)
    # After Playwright runs, browsers are the most common leak.
    kill_browsers
    show_status
    ;;

  emergency)
    stop_background_daemons
    kill_browsers
    if [[ "${PROFILE}" == "full_stop" ]]; then
      stop_omega_server
    fi
    show_status
    ;;

  help|-h|--help|"" )
    cat <<EOF
Usage: $0 <status|pretest|posttest|emergency>

Env:
  HFO_GOV_PROFILE=crash_safe|full_stop  (default: crash_safe)

Notes:
  - pretest: stops nonessential daemons + browsers.
  - posttest: cleans up browsers after runs.
  - emergency: also stops omega server when profile=full_stop.
EOF
    ;;

  *)
    say "unknown mode: ${MODE}"
    exit 2
    ;;
esac
