#!/usr/bin/env bash
set -euo pipefail

# Phoenix-style regenerate for Shodh (derived mirror)
# - Stops Shodh container
# - Burns ONLY derived Shodh data (keeps model cache)
# - Starts Shodh
# - Waits for /health
# - Syncs SSOT -> Shodh (bounded by --limit unless you set --limit 0)
# - Runs a small recall sanity query

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Load repo .env if present
if [[ -f "$repo_root/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$repo_root/.env"
  set +a
fi

container_name="${SHODH_DOCKER_NAME:-hfo-shodh-memory}"
shodh_url="http://${SHODH_HOST:-127.0.0.1}:${SHODH_PORT:-3030}"
shodh_data_dir="${SHODH_MEMORY_PATH:-$repo_root/artifacts/shodh_memory/data}"
shodh_cache_dir="${SHODH_DOCKER_CACHE_DIR:-$repo_root/artifacts/shodh_memory/cache}"

write=0
limit=500
timeout_sec=30
health_timeout_sec=120
query="timeline of 2025"
retries=8
retry_backoff_sec=1
sleep_ms=25
max_content_chars=2000
sync_max_runtime_sec=1800
recall_max_runtime_sec=120

usage() {
  cat <<'EOF'
Usage: scripts/shodh_regenerate_from_ssot.sh [options]

Options:
  --write              Actually sync SSOT -> Shodh (default: dry-run)
  --limit N            Sync at most N rows (default: 500; 0 means no limit)
  --timeout-sec N      Hub->Shodh request timeout seconds (default: 30)
  --health-timeout N   Max seconds to wait for /health (default: 120)
  --retries N          Retry count for transient Shodh errors (default: 8)
  --retry-backoff-sec N  Backoff seconds between retries (default: 1)
  --sleep-ms N         Sleep between upserts to reduce load (default: 25)
  --max-content-chars N  Max chars per upsert payload (default: 12000)
  --sync-max-runtime-sec N   Max seconds allowed for SSOT->Shodh sync (default: 1800)
  --recall-max-runtime-sec N Max seconds allowed for recall sanity query (default: 120)
  --query TEXT         Recall sanity query (default: 'timeline of 2025')

Notes:
- This script burns ONLY Shodh derived data under artifacts/shodh_memory/data.
- It preserves the Shodh model cache under artifacts/shodh_memory/cache (configurable).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --write) write=1; shift ;;
    --limit) limit="$2"; shift 2 ;;
    --timeout-sec) timeout_sec="$2"; shift 2 ;;
    --health-timeout) health_timeout_sec="$2"; shift 2 ;;
    --retries) retries="$2"; shift 2 ;;
    --retry-backoff-sec) retry_backoff_sec="$2"; shift 2 ;;
    --sleep-ms) sleep_ms="$2"; shift 2 ;;
    --max-content-chars) max_content_chars="$2"; shift 2 ;;
    --sync-max-runtime-sec) sync_max_runtime_sec="$2"; shift 2 ;;
    --recall-max-runtime-sec) recall_max_runtime_sec="$2"; shift 2 ;;
    --query) query="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

run_nonfatal() {
  set +e
  "$@"
  local rc=$?
  set -e
  return $rc
}

run_tee_nonfatal() {
  local out="$1"
  shift

  local -a cmd=("$@")
  if command -v timeout >/dev/null 2>&1; then
    local max_runtime="${MAX_RUNTIME_SEC:-0}"
    if [[ -n "$max_runtime" ]] && [[ "$max_runtime" != "0" ]]; then
      cmd=(timeout --preserve-status -k 10 "${max_runtime}" "${cmd[@]}")
    fi
  fi

  set +e
  "${cmd[@]}" 2>&1 | tee "$out"
  local rc=${PIPESTATUS[0]}
  set -e
  return $rc
}

mkdir -p artifacts/proofs
proof_dir="artifacts/proofs/shodh_regen_$(date -u +%Y_%m_%dT%H%M%SZ)"
mkdir -p "$proof_dir"

{
  echo "=== date ==="; date -Is
  echo
  echo "=== config ==="
  echo "container_name=$container_name"
  echo "shodh_url=$shodh_url"
  echo "shodh_data_dir=$shodh_data_dir"
  echo "shodh_cache_dir=$shodh_cache_dir"
  echo "write=$write limit=$limit timeout_sec=$timeout_sec health_timeout_sec=$health_timeout_sec retries=$retries retry_backoff_sec=$retry_backoff_sec sleep_ms=$sleep_ms max_content_chars=$max_content_chars sync_max_runtime_sec=$sync_max_runtime_sec recall_max_runtime_sec=$recall_max_runtime_sec"
  echo
  echo "=== stop shodh container (if running) ==="
  bash scripts/shodh_memory_stop.sh || true

  if command -v docker >/dev/null 2>&1; then
    if docker ps -a --format '{{.Names}}' | grep -qx "$container_name"; then
      echo "Removing container: $container_name"
      docker rm -f "$container_name" >/dev/null || true
    fi
  else
    echo "docker not found; cannot regenerate docker-based shodh" >&2
    exit 2
  fi

  echo
  echo "=== burn derived data (keep cache) ==="
  mkdir -p "$shodh_data_dir"
  mkdir -p "$shodh_cache_dir"
  rm -rf "$shodh_data_dir"/*

  echo
  echo "=== start shodh (docker) ==="
  HFO_SHODH_RUN_MODE=docker bash scripts/shodh_memory_server.sh

  echo
  echo "=== wait for /health ==="
  start_ts=$(date +%s)
  while true; do
    if curl -sS -m 2 "$shodh_url/health" >/dev/null 2>&1; then
      echo "HEALTH_OK"
      break
    fi
    now=$(date +%s)
    if (( now - start_ts > health_timeout_sec )); then
      echo "ERROR: health check timed out after ${health_timeout_sec}s" >&2
      echo "docker logs tail:" >&2
      docker logs --tail 120 "$container_name" >&2 || true
      exit 1
    fi
    sleep 2
  done

  echo
  echo "=== /health (proof) ==="
  health_proof_file="$proof_dir/health_initial.txt"
  run_nonfatal curl -sS -m 5 -D - "$shodh_url/health" >"$health_proof_file" 2>&1
  echo "EXIT=$?"
  head -n 80 "$health_proof_file" || true

  echo
  echo "=== memory overview (saved) ==="
  run_nonfatal bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py memory:overview --json >"$proof_dir/memory_overview.json"
  echo "EXIT=$?"
  head -n 120 "$proof_dir/memory_overview.json" || true

  echo
  sync_rc=0
  if (( write == 1 )); then
    echo "=== ssot -> shodh sync (WRITE, retryable) ==="
    sync_rc=0
    MAX_RUNTIME_SEC="$sync_max_runtime_sec" run_tee_nonfatal "$proof_dir/ssot_sync_shodh.txt" \
      bash scripts/mcp_env_wrap.sh env PYTHONUNBUFFERED=1 ./.venv/bin/python scripts/shodh_sync_from_doobidoo_ssot.py \
        --timeout-sec "$timeout_sec" \
        --limit "$limit" \
        --retries "$retries" \
        --retry-backoff-sec "$retry_backoff_sec" \
        --sleep-ms "$sleep_ms" \
        --max-content-chars "$max_content_chars" \
      || sync_rc=$?
    echo "EXIT=$sync_rc"
    echo "WROTE=$proof_dir/ssot_sync_shodh.txt"

    echo
    echo "=== ssot recall-shodh (sanity) ==="
    recall_rc=0
    MAX_RUNTIME_SEC="$recall_max_runtime_sec" run_tee_nonfatal "$proof_dir/ssot_recall_shodh.txt" \
      bash scripts/mcp_env_wrap.sh env PYTHONUNBUFFERED=1 ./.venv/bin/python hfo_hub.py ssot recall-shodh --query "$query" --limit 5 \
      || recall_rc=$?
    echo "EXIT=$recall_rc"
    echo "WROTE=$proof_dir/ssot_recall_shodh.txt"
  else
    echo "=== ssot -> shodh sync (dry-run) ==="
    run_nonfatal bash scripts/mcp_env_wrap.sh env PYTHONUNBUFFERED=1 ./.venv/bin/python scripts/shodh_sync_from_doobidoo_ssot.py \
      --dry-run \
      --timeout-sec "$timeout_sec" \
      --limit "$limit" \
      --max-content-chars "$max_content_chars" \
      >"$proof_dir/ssot_sync_shodh_dry_run.txt" 2>&1
    sync_rc=$?
    echo "EXIT=$sync_rc"
    echo "WROTE=$proof_dir/ssot_sync_shodh_dry_run.txt"
    head -n 80 "$proof_dir/ssot_sync_shodh_dry_run.txt" || true

    echo
    echo "=== ssot search (works even if shodh empty) ==="
    run_nonfatal bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot search --query "$query" --limit 5
    echo "EXIT=$?"
  fi

  echo
  echo "=== /health after sync ==="
  health_after_file="$proof_dir/health_after_sync.txt"
  run_nonfatal curl -sS -m 5 -D - "$shodh_url/health" >"$health_after_file" 2>&1
  echo "EXIT=$?"
  head -n 80 "$health_after_file" || true

  echo
  echo "=== docker inspect limits (proof) ==="
  docker inspect "$container_name" --format 'Memory={{.HostConfig.Memory}} MemorySwap={{.HostConfig.MemorySwap}} NanoCpus={{.HostConfig.NanoCpus}} PidsLimit={{.HostConfig.PidsLimit}} RestartPolicy={{.HostConfig.RestartPolicy.Name}} RestartCount={{.RestartCount}} OOMKilled={{.State.OOMKilled}} ExitCode={{.State.ExitCode}} Health={{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}'

  echo
  echo "PROOF_DIR=$proof_dir"
} | tee "$proof_dir/proof.txt"

# Always capture recent logs as separate proof artifact
(docker logs --tail 200 "$container_name" 2>&1 || true) >"$proof_dir/docker_logs_tail.txt"

if [[ "${sync_rc:-0}" != "0" ]]; then
  echo "Sync failed (exit=$sync_rc). Proof still written to: $proof_dir" >&2
  exit "$sync_rc"
fi

echo "Wrote proof to: $proof_dir"