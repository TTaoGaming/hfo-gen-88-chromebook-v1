#!/usr/bin/env bash
set -euo pipefail

if [[ "${SKIP_HFO_PRECOMMIT:-}" == "1" ]]; then
  echo "[hfo] Pre-commit: SKIP_HFO_PRECOMMIT=1; skipping."
  exit 0
fi

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

STAGED_FILES="$(git diff --cached --name-only)"

should_run_hive8_cards_verifier() {
  # Run when staged changes touch Gen88 HIVE8 card mapping contracts or Gold views.
  echo "$STAGED_FILES" | grep -Eqi '(^|/)(contracts/hfo_mtg_port_card_mappings\.(v1|v2)\.json|contracts/hfo_legendary_commanders_invariants\.v1\.json|hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/|scripts/verify_hive8_mtg_card_mappings\.mjs)'
}

should_run_dino_classifier() {
  # Only run when staged changes impact the *executable* Gen6 v9 Dino diagnostic path.
  # IMPORTANT: do NOT trigger on docs/reports that merely *mention* gen6_v9/dino (migration batches).
  echo "$STAGED_FILES" \
    | grep -Evi '/references/' \
    | grep -Eqi '(^|/)(scripts/omega_gen6_v9_dino_diagnostics\.spec\.ts|scripts/hfo_gen6_v9_dino_classify\.sh|playwright\.config\.ts|hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/)'
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
  if should_run_hive8_cards_verifier; then
    echo "[hfo] Pre-commit: verifying Gen88 HIVE8 card mappings (fail-closed)."
    npm run -s verify:hive8:cards
  else
    echo "[hfo] Pre-commit: skipping Gen88 HIVE8 card verifier (no relevant staged files)."
  fi

  echo "[hfo] Pre-commit: skipping Gen6 Dino classifier (no relevant staged files)."
  exit 0
fi

if should_run_hive8_cards_verifier; then
  echo "[hfo] Pre-commit: verifying Gen88 HIVE8 card mappings (fail-closed)."
  npm run -s verify:hive8:cards
else
  echo "[hfo] Pre-commit: skipping Gen88 HIVE8 card verifier (no relevant staged files)."
fi

echo "[hfo] Pre-commit: running Gen6 Dino classifier (fail-closed)."
start_server_if_needed

export HFO_DIAG_REPEATS="${HFO_DIAG_REPEATS:-3}"
export HFO_DIAG_FAIL_CLOSED="${HFO_DIAG_FAIL_CLOSED:-true}"

# Applicability check: if the Gen6 runtime page is not present in this repo layout,
# do not run the Playwright suite (it will always 404/time out and blocks safe doc migrations).
#
# When the runtime exists, the classifier remains fail-closed.
GEN6_RUNTIME_CANDIDATES=(
  "$ROOT_DIR/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v10.html"
  "$ROOT_DIR/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v9.html"
  "$ROOT_DIR/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v10_1.html"
)

get_gen6_runtime_candidates_from_pointers() {
  local py="$ROOT_DIR/.venv/bin/python"
  if [[ ! -x "$py" ]]; then
    py="$(command -v python3 || true)"
  fi
  if [[ -z "$py" ]]; then
    return 1
  fi

  "$py" - <<'PY'
from hfo_pointers import get_pointer

cands = get_pointer("paths.gen6_runtime_html_candidates", None)
if isinstance(cands, list):
    for p in cands:
        if isinstance(p, str) and p.strip():
            print(p.strip())
PY
}

mapfile -t _GEN6_FROM_POINTERS < <(get_gen6_runtime_candidates_from_pointers 2>/dev/null || true)
if [[ ${#_GEN6_FROM_POINTERS[@]} -gt 0 ]]; then
  GEN6_RUNTIME_CANDIDATES=()
  for rel in "${_GEN6_FROM_POINTERS[@]}"; do
    if [[ "$rel" = /* ]]; then
      GEN6_RUNTIME_CANDIDATES+=("$rel")
    else
      GEN6_RUNTIME_CANDIDATES+=("$ROOT_DIR/$rel")
    fi
  done
fi

HAS_GEN6_RUNTIME=0
for p in "${GEN6_RUNTIME_CANDIDATES[@]}"; do
  if [[ -f "$p" ]]; then
    HAS_GEN6_RUNTIME=1
    break
  fi
done

if [[ "$HAS_GEN6_RUNTIME" != "1" ]]; then
  echo "[hfo] Pre-commit: skipping Gen6 Dino classifier (no Gen6 runtime HTML present in repo)."
  echo "[hfo] To enforce: add a runtime html (e.g. omega_gen6_v10.html) under omega_gen6_current or set HFO_GEN6_URL to a valid in-repo page and rerun manually."
  exit 0
fi

npm run -s test:gen6:v9:dino:classify
