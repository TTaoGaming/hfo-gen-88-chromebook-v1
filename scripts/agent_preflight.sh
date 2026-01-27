#!/usr/bin/env bash
set -euo pipefail

# agent_preflight.sh
# Manual guardrail: quick checks before starting heavy workflows.
# Nondestructive: only prints status and returns nonzero if thresholds are not met.

min_free_gib="${HFO_PREFLIGHT_MIN_FREE_GIB:-8}"
max_mem_used_pct="${HFO_PREFLIGHT_MAX_MEM_USED_PCT:-85}"

fail=0

printf '## agent_preflight %s\n' "$(date -Iseconds)"

echo
echo "### offenders (should be NONE)"
./scripts/agent_status_light.sh || true

echo
echo "### disk free check (/, min ${min_free_gib}GiB)"
free_gib=$(df -BG --output=avail / | tail -n 1 | tr -dc '0-9')
echo "free_gib=$free_gib"
if [[ -n "$free_gib" ]] && (( free_gib < min_free_gib )); then
  echo "FAIL: free disk is below threshold"
  fail=1
else
  echo "OK"
fi

echo
echo "### memory pressure check (max used ${max_mem_used_pct}%)"
# used% = (total - available) / total
mem_used_pct=$(free -m | awk 'NR==2 { if ($2>0) printf("%.0f", ( ($2-$7) / $2 ) * 100 ); }')
echo "mem_used_pct=$mem_used_pct"
if [[ -n "$mem_used_pct" ]] && (( mem_used_pct > max_mem_used_pct )); then
  echo "FAIL: memory pressure is above threshold"
  fail=1
else
  echo "OK"
fi

echo
if (( fail == 1 )); then
  echo "RESULT: FAIL (preflight)"
  echo "Tip: stop offenders with ./scripts/agent_stop.sh, then reduce disk usage or move cold data out of the hot workspace."
  exit 2
fi

echo "RESULT: OK (preflight)"
