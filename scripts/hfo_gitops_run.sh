#!/usr/bin/env bash
# Medallion: Bronze | Mutation: 0% | HIVE: V

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

run_id="$(date -u +%Y%m%dT%H%M%SZ)"
branch="$(git symbolic-ref --short -q HEAD || echo detached)"

proof_root="${HFO_GITOPS_PROOF_ROOT:-artifacts/proofs}"
proof_dir="${HFO_GITOPS_PROOF_DIR:-$proof_root/gitops_${run_id}__${branch}}"

mkdir -p "$proof_dir"

echo "PROOF_DIR=$proof_dir" | tee "$proof_dir/PROOF_DIR.txt" >/dev/null

# Always prefer human/agent-friendly git status output.
# Batcher itself avoids untracked enumeration for performance.

set +e
bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_gitops_batcher.py \
  --config .gitops/batches.json \
  --proof-dir "$proof_dir" \
  --enforce-status-untracked \
  "$@" \
  2>&1 | tee "$proof_dir/run.log"
rc=${PIPESTATUS[0]}
set -e

exit "$rc"
