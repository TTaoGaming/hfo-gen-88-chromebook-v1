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
  4) No-op fast path: if nothing actionable exists, exits 0
  5) Scoped preflight gate: checks HOT provenance headers for files that would be committed
  6) If --confirm is provided and gates pass, runs the real GitOps batching

Notes:
  - This wrapper never invents staging; it delegates to scripts/hfo_gitops_batcher.py.
  - Default is fail-closed: without --confirm, it stops after producing the plan.
EOF
}

get_batches_json() {
  local config_path="$1"
  python3 - "$config_path" <<'PY'
import json
import sys

config_path = sys.argv[1]

with open(config_path, 'r', encoding='utf-8') as f:
  config = json.load(f)

batches = config.get('batches', [])
out = []
for b in batches:
  out.append({
    'id': b.get('id'),
    'type': b.get('type'),
    'paths': b.get('paths', []),
  })

json.dump(out, sys.stdout)
PY
}

scoped_preflight_provenance_gate() {
  local config_path="$1"
  local proof_dir="$2"

  # Only gate HOT docs that are about to be committed.
  # We intentionally do NOT scan the whole repo.
  local batches
  batches="$(get_batches_json "$config_path")"

  BATCHES_JSON="$batches" python3 - "$proof_dir" <<'PY'
import json
import os
import subprocess
import sys

proof_dir = sys.argv[1]

batches = json.loads(os.environ.get('BATCHES_JSON', '[]'))

def run(cmd):
  p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
  return [line.strip() for line in p.stdout.splitlines() if line.strip()]

def has_header(path):
  try:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
      head = f.read(8192)
    if not head:
      return False

    lines = head.splitlines()

    # Find the first non-empty line.
    first_nonempty_idx = None
    first_nonempty = ''
    for i, ln in enumerate(lines):
      s = ln.strip()
      if not s:
        continue
      first_nonempty_idx = i
      first_nonempty = s
      break

    if first_nonempty_idx is None:
      return False

    # Preferred provenance headers.
    if first_nonempty.startswith('# Medallion:') or first_nonempty.startswith('<!-- Medallion:'):
      return True

    # YAML front matter provenance (common in forge docs).
    # Accept if the file begins with '---' and includes a medallion key.
    if first_nonempty == '---':
      fm_lines = []
      for ln in lines[first_nonempty_idx + 1:]:
        if ln.strip() == '---':
          break
        fm_lines.append(ln)
      fm = '\n'.join(fm_lines)
      # Some forge docs keep the Medallion line as a YAML comment.
      if '# Medallion:' in fm:
        return True
      if 'medallion_layer:' in fm or '\nmedallion:' in ('\n' + fm):
        return True

    return False
  except OSError:
    return False

candidate_files = []
for b in batches:
  btype = b.get('type')
  paths = b.get('paths') or []
  if not paths:
    continue

  if btype == 'tracked':
    candidate_files += run(['git', 'diff', '--name-only', '--', *paths])
  elif btype == 'untracked':
    candidate_files += run(['git', 'ls-files', '--others', '--exclude-standard', '--', *paths])

candidate_files = sorted(set(candidate_files))

hot_exts = ('.md', '.html')
hot_prefixes = ('hfo_hot_obsidian/', 'hfo_hot_obsidian_forge/')

missing = []
for f in candidate_files:
  if not f.startswith(hot_prefixes):
    continue
  if not f.endswith(hot_exts):
    continue
  if not os.path.exists(f):
    continue
  if not has_header(f):
    missing.append(f)

out_path = os.path.join(proof_dir, 'preflight_scoped_provenance.json')
with open(out_path, 'w', encoding='utf-8') as out:
  json.dump({'missing_headers': missing, 'checked_count': len(candidate_files)}, out, indent=2)

if missing:
  sys.stderr.write('[gitops-auto] preflight fail: missing Medallion header in staged-to-commit HOT docs:\n')
  for f in missing[:50]:
    sys.stderr.write(f'  - {f}\n')
  if len(missing) > 50:
    sys.stderr.write(f'  ... and {len(missing) - 50} more\n')
  sys.stderr.write(f"[gitops-auto] details: {out_path}\n")
  sys.exit(3)

sys.exit(0)
PY
}

has_actionable_work() {
  local config_path="$1"
  local proof_dir="$2"

  local batches_json
  batches_json="$(get_batches_json "$config_path")"

  BATCHES_JSON="$batches_json" python3 - "$proof_dir" <<'PY'
import json
import os
import subprocess
import sys

proof_dir = sys.argv[1]
batches = json.loads(os.environ.get('BATCHES_JSON', '[]'))

def run(cmd):
  p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
  return [line.strip() for line in p.stdout.splitlines() if line.strip()]

any_files = []
for b in batches:
  btype = b.get('type')
  paths = b.get('paths') or []
  if not paths:
    continue
  if btype == 'tracked':
    any_files = run(['git', 'diff', '--name-only', '--', *paths])
  elif btype == 'untracked':
    any_files = run(['git', 'ls-files', '--others', '--exclude-standard', '--', *paths])
  if any_files:
    break

out_path = os.path.join(proof_dir, 'actionable_probe.json')
with open(out_path, 'w', encoding='utf-8') as out:
  json.dump({'has_actionable': bool(any_files), 'first_hit': any_files[:25]}, out, indent=2)

sys.exit(0 if any_files else 1)
PY
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

# Option 1: No-op fast path (safe to run on timers/CI).
if has_actionable_work "$config_path" "$proof_dir"; then
  :
else
  echo "[gitops-auto] no-op: nothing actionable under batch allowlists; exiting 0" | tee -a "$proof_dir/plan.log" >/dev/null
  exit 0
fi

if [[ $confirm -ne 1 ]]; then
  echo "[gitops-auto] fail-closed: not running commits without --confirm" >&2
  echo "[gitops-auto] review: $proof_dir/plan.log" >&2
  exit 2
fi

# Option 2: Scoped preflight gate before we invoke husky/pre-commit.
scoped_preflight_provenance_gate "$config_path" "$proof_dir"

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