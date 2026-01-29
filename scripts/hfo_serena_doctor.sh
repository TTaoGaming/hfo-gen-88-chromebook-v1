#!/usr/bin/env bash
set -euo pipefail

# Medallion: Bronze | Mutation: 0% | HIVE: V
# Serena Doctor (Alpha/Omega): quick, deterministic diagnostics for the
# "No active project" hardgate + multi-mission (Alpha/Omega) setup gaps.

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/hfo_serena_doctor.sh [--write] [--out <path>] [--json] [--fail-on-missing]

Options:
  --write            Write a JSON report (default path under artifacts/)
  --out <path>       Write report to a specific workspace-relative path
  --json             Print JSON to stdout (even without --write)
  --fail-on-missing  Exit non-zero if key expectations are missing

Notes:
- This script does NOT modify Serena config.
- It only provides deterministic evidence + next actions.
USAGE
}

want_write=0
out_path=""
want_json=0
fail_on_missing=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --write) want_write=1; shift 1;;
    --out) out_path="${2:-}"; shift 2;;
    --json) want_json=1; shift 1;;
    --fail-on-missing) fail_on_missing=1; shift 1;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2;;
  esac
done

workspace_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

default_out="artifacts/reports/serena_doctor_latest.json"
if [[ -z "$out_path" ]]; then
  out_path="$default_out"
fi

alpha_root="$workspace_root"

get_pointer_path() {
  local key="$1"
  python3 - <<PY
import json
from pathlib import Path
p = Path("$workspace_root") / "hfo_pointers.json"
obj = json.loads(p.read_text(encoding="utf-8"))
print(obj.get("paths", {}).get("$key", ""))
PY
}

omega_rel="$(get_pointer_path omega_gen7_current_project_root || true)"
omega_root=""
if [[ -n "$omega_rel" ]]; then
  omega_root="$workspace_root/$omega_rel"
fi

serena_local_project_yml="$workspace_root/.serena/project.yml"
local_project_name=""
if [[ -f "$serena_local_project_yml" ]]; then
  local_project_name="$(python3 - <<PY
from pathlib import Path
p = Path("$serena_local_project_yml")
text = p.read_text(encoding="utf-8", errors="replace")
# minimal YAML extraction: look for "project_name:"
for line in text.splitlines():
  if line.strip().startswith("project_name:"):
    print(line.split(":", 1)[1].strip().strip('"\''))
    break
PY
)"
fi

home_serena_cfg="$HOME/.serena/serena_config.yml"
home_cfg_exists=0
if [[ -f "$home_serena_cfg" ]]; then
  home_cfg_exists=1
fi

home_cfg_mentions_alpha=0
home_cfg_mentions_omega=0
if [[ $home_cfg_exists -eq 1 ]]; then
  if rg -F -q "$alpha_root" "$home_serena_cfg" 2>/dev/null; then home_cfg_mentions_alpha=1; fi
  if [[ -n "$omega_root" ]] && rg -F -q "$omega_root" "$home_serena_cfg" 2>/dev/null; then home_cfg_mentions_omega=1; fi
fi

omega_dir_exists=0
if [[ -n "$omega_root" ]] && [[ -d "$omega_root" ]]; then
  omega_dir_exists=1
fi

missing=()
if [[ ! -f "$serena_local_project_yml" ]]; then
  missing+=("missing:.serena/project.yml")
fi
if [[ -z "$local_project_name" ]]; then
  missing+=("missing:local_project_name")
fi
if [[ $home_cfg_exists -eq 0 ]]; then
  missing+=("missing:$HOME/.serena/serena_config.yml")
fi
if [[ $home_cfg_exists -eq 1 && $home_cfg_mentions_alpha -eq 0 ]]; then
  missing+=("missing:home_serena_config_mentions_alpha_root")
fi
if [[ $omega_dir_exists -eq 1 && $home_cfg_exists -eq 1 && $home_cfg_mentions_omega -eq 0 ]]; then
  missing+=("missing:home_serena_config_mentions_omega_root")
fi

status="ok"
if [[ ${#missing[@]} -gt 0 ]]; then
  status="needs_attention"
fi

# Build JSON (stable schema-ish)
missing_lines="$(printf '%s\n' "${missing[@]}")"

json="$(HFO_SERENA_MISSING="$missing_lines" python3 - <<PY
import json
import os

missing = [line for line in os.environ.get("HFO_SERENA_MISSING", "").splitlines() if line.strip()]

obj = {
  "schema_id": "hfo.tools.serena_doctor",
  "schema_version": 1,
  "workspace_root": "$workspace_root",
  "alpha_root": "$alpha_root",
  "omega_root": "$omega_root",
  "omega_dir_exists": bool($omega_dir_exists),
  "local_serena_project_yml": "$serena_local_project_yml",
  "local_project_name": "$local_project_name",
  "home_serena_config": "$home_serena_cfg",
  "home_config_exists": bool($home_cfg_exists),
  "home_config_mentions_alpha_root": bool($home_cfg_mentions_alpha),
  "home_config_mentions_omega_root": bool($home_cfg_mentions_omega),
  "status": "$status",
  "missing": missing,
  "next_actions": [
    "If you see 'No active project' in Serena: activate the Alpha project '$local_project_name' (workspace root).",
    "Register both missions in Serena: ensure '$alpha_root' (Alpha) and '$omega_root' (Omega) are present in $HOME/.serena/serena_config.yml (projects list).",
    "Make the gate deterministic: prefer an auto-select behavior when only one matching project exists (HFO recommendation)."
  ],
}

print(json.dumps(obj, indent=2, sort_keys=True))
PY
)"

if [[ $want_json -eq 1 || $want_write -eq 0 ]]; then
  echo "$json"
fi

if [[ $want_write -eq 1 ]]; then
  mkdir -p "$(dirname "$workspace_root/$out_path")"
  printf "%s\n" "$json" > "$workspace_root/$out_path"
fi

if [[ $fail_on_missing -eq 1 && $status != "ok" ]]; then
  echo "serena_doctor: status=$status missing=${missing[*]}" >&2
  exit 3
fi
