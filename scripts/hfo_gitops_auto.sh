#!/usr/bin/env bash
# Medallion: Bronze | Mutation: 0% | HIVE: V

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

usage() {
  cat <<'EOF'
Usage:
  scripts/hfo_gitops_auto.sh [--confirm] [--push] [--push-mode end|each] [--no-verify] [--config PATH]

What it does:
  1) Fail-closed sanity checks (refuses dirty staged index)
  2) Writes a proof bundle under artifacts/proofs/
  3) Runs a GitOps PLAN (dry run)
  4) If --confirm is provided, runs the real GitOps batching

Notes:
  - This wrapper never invents staging; it delegates to scripts/hfo_gitops_batcher.py.
  - Default is fail-closed: without --confirm, it stops after producing the plan.
EOF
}

confirm=0
push_flag="--no-push"
push_mode="end"
no_verify=0
config_path=".gitops/batches.json"

# Parse a minimal flag set; pass-through for unknown flags is intentionally NOT supported.
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --confirm)
      confirm=1
      shift
      ;;
    --push)
      push_flag="--push"
      shift
      ;;
    --no-push)
      push_flag="--no-push"
      shift
      ;;
    --push-mode)
      push_mode="${2:-}"
      shift 2
      ;;
    --no-verify)
      no_verify=1
      shift
      ;;
    --config)
      config_path="${2:-}"
      shift 2
      ;;
    *)
      echo "[gitops-auto] unknown arg: $1" >&2
      echo "[gitops-auto] run with --help for usage" >&2
      exit 2
      ;;
  esac
done

if [[ "$push_mode" != "end" && "$push_mode" != "each" ]]; then
  echo "[gitops-auto] invalid --push-mode: $push_mode (expected 'end' or 'each')" >&2
  exit 2
fi

# Fail-closed: staged index must be empty so we don't accidentally commit unrelated work.
if ! git diff --cached --quiet; then
  echo "[gitops-auto] staged index is dirty; refusing. Run 'git reset' or commit your staged changes first." >&2
  exit 2
fi

run_id="$(date -u +%Y%m%dT%H%M%SZ)"
branch="$(git symbolic-ref --short -q HEAD || echo detached)"
proof_root="${HFO_GITOPS_PROOF_ROOT:-artifacts/proofs}"
proof_dir="${HFO_GITOPS_PROOF_DIR:-$proof_root/gitops_auto_${run_id}__${branch}}"

mkdir -p "$proof_dir"

{
  echo "PROOF_DIR=$proof_dir"
  echo "UTC_RUN_ID=$run_id"
  echo "BRANCH=$branch"
  echo "PUSH=$push_flag"
  echo "PUSH_MODE=$push_mode"
  echo "CONFIRM=$confirm"
  echo "CONFIG=$config_path"
} | tee "$proof_dir/PROOF_DIR.txt" >/dev/null

common_args=(
  --config "$config_path"
  --proof-dir "$proof_dir"
  --enforce-status-untracked
)

if [[ $no_verify -eq 1 ]]; then
  common_args+=(--no-verify)
fi

echo "[gitops-auto] proof: $proof_dir"
echo "[gitops-auto] plan: generating dry-run plan" | tee "$proof_dir/plan.log" >/dev/null

set +e
bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_gitops_batcher.py \
  "${common_args[@]}" \
  --plan \
  2>&1 | tee -a "$proof_dir/plan.log"
plan_rc=${PIPESTATUS[0]}
set -e

if [[ $plan_rc -ne 0 ]]; then
  echo "[gitops-auto] plan failed (rc=$plan_rc); see $proof_dir/plan.log" >&2
  exit "$plan_rc"
fi

if [[ $confirm -ne 1 ]]; then
  echo "[gitops-auto] fail-closed: not running commits without --confirm" >&2
  echo "[gitops-auto] review: $proof_dir/plan.log" >&2
  exit 2
fi

echo "[gitops-auto] run: executing GitOps batching" | tee "$proof_dir/run.log" >/dev/null

set +e
bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_gitops_batcher.py \
  "${common_args[@]}" \
  "$push_flag" \
  --push-mode "$push_mode" \
  2>&1 | tee -a "$proof_dir/run.log"
run_rc=${PIPESTATUS[0]}
set -e

if [[ $run_rc -ne 0 ]]; then
  echo "[gitops-auto] run failed (rc=$run_rc); see $proof_dir/run.log" >&2
  exit "$run_rc"
fi

echo "[gitops-auto] ok: completed. proof=$proof_dir"