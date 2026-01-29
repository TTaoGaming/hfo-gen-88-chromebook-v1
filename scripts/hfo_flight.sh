#!/usr/bin/env bash
set -euo pipefail

# HFO Flight Runner (Bronze)
# - Minimal wrapper for ANY agent to do: preflight -> work -> postflight -> retry/handoff
# - Runs via scripts/mcp_env_wrap.sh to avoid env drift
# - Calls the gateway tool handler directly (no MCP wiring required)

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/hfo_flight.sh preflight  --scope <HFO|P6|P0.3.5.7.1> [--role agent] [--note "..."] [--write-memory true|false] [--out path]
  bash scripts/hfo_flight.sh postflight --scope <HFO|P6|P0.3.5.7.1> --preflight-receipt-id <id> --summary "..." [--outcome ok|partial|error] [--sources a,b,c] [--changes a,b] [--write-memory true|false] [--out path]

Notes:
  - scope supports fractal addressing: P<port>[.<digit>...]
  - preflight prints JSON including receipt_id and capsule
  - postflight prints JSON including receipt_id
USAGE
}

cmd="${1:-}"
shift || true

scope=""
role="agent"
note=""
preflight_receipt_id=""
summary=""
outcome="ok"
sources=""
changes=""
write_memory="false"
out_path=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope) scope="${2:-}"; shift 2;;
    --role) role="${2:-}"; shift 2;;
    --note) note="${2:-}"; shift 2;;
    --preflight-receipt-id) preflight_receipt_id="${2:-}"; shift 2;;
    --summary) summary="${2:-}"; shift 2;;
    --outcome) outcome="${2:-}"; shift 2;;
    --sources) sources="${2:-}"; shift 2;;
    --changes) changes="${2:-}"; shift 2;;
    --write-memory) write_memory="${2:-}"; shift 2;;
    --out) out_path="${2:-}"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 2;;
  esac
done

# Policy: JSONL MCP memory ledger writes are banned; SSOT sqlite is the only write path.
# We keep the flag for backwards compatibility, but force-disable it.
if [[ "${write_memory,,}" == "true" || "${write_memory,,}" == "1" || "${write_memory,,}" == "yes" ]]; then
  echo "[hfo_flight] warn: --write-memory requested but is disabled by policy (SSOT sqlite only). For persistence, ingest to SSOT via scripts/hfo_memory_ingest_*." >&2
  write_memory="false"
fi

if [[ -z "$cmd" || -z "$scope" ]]; then
  usage
  exit 2
fi

# Convert scope like P0.3.5.7.1 -> port=0 subshard_path=[3,5,7,1]
port_tool=""
port_num=""
subshard_json="null"

if [[ "$scope" == "HFO" ]]; then
  port_tool="hfo"
elif [[ "$scope" =~ ^P([0-7])(\..+)?$ ]]; then
  port_tool="port"
  port_num="${BASH_REMATCH[1]}"
  suffix="${BASH_REMATCH[2]:-}"
  if [[ -n "$suffix" ]]; then
    suffix="${suffix#.}"
    IFS='.' read -r -a parts <<< "$suffix"
    # Build a JSON array like [3,5,7,1]
    subshard_json="["
    for i in "${!parts[@]}"; do
      d="${parts[$i]}"
      if [[ ! "$d" =~ ^[0-9]+$ ]]; then
        echo "Invalid scope digit in subshard path: $d" >&2
        exit 2
      fi
      if [[ $i -gt 0 ]]; then subshard_json+=","; fi
      subshard_json+="$d"
    done
    subshard_json+="]"
  fi
else
  echo "Invalid --scope: $scope" >&2
  usage
  exit 2
fi

python_code=$(cat <<'PY'
import argparse
import asyncio
import importlib.util
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--cmd', required=True)
parser.add_argument('--scope', required=True)
parser.add_argument('--role', default='agent')
parser.add_argument('--note', default='')
parser.add_argument('--write_memory', default='true')
parser.add_argument('--port_num')
parser.add_argument('--subshard_json', default='null')
parser.add_argument('--preflight_receipt_id', default='')
parser.add_argument('--outcome', default='ok')
parser.add_argument('--summary', default='')
parser.add_argument('--sources', default='')
parser.add_argument('--changes', default='')
args = parser.parse_args()

write_memory = str(args.write_memory).lower() not in ('0','false','no')

subshard_path = None
try:
    subshard_path = json.loads(args.subshard_json)
except Exception:
    subshard_path = None

def _csv(s: str):
    s = (s or '').strip()
    if not s:
        return []
    return [x.strip() for x in s.split(',') if x.strip()]

gateway_path = Path('hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py')
spec = importlib.util.spec_from_file_location('hfo_mcp_gateway_hub_impl', gateway_path)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

if args.cmd == 'preflight':
    if args.scope == 'HFO':
        tool = 'hfo_preflight'
        payload = {
            'role': args.role,
            'note': args.note,
            'scope': args.scope,
            'subshard_path': subshard_path,
            'write_memory': write_memory,
        }
    else:
        tool = 'port_preflight' if args.scope != 'P6' else 'port6_preflight'
        if tool == 'port6_preflight':
            payload = {
                'role': args.role,
                'note': args.note,
                'scope': args.scope,
                'subshard_path': subshard_path,
                'write_memory': write_memory,
            }
        else:
            payload = {
                'port': int(args.port_num),
                'role': args.role,
                'note': args.note,
                'scope': args.scope,
                'subshard_path': subshard_path,
                'write_memory': write_memory,
            }

    out = asyncio.run(mod.handle_call_tool(tool, payload))
    text = "\n".join([getattr(x, 'text', str(x)) for x in out]).strip()
    print(text)

elif args.cmd == 'postflight':
    if not args.summary:
        raise SystemExit('Error: --summary is required for postflight')

    if args.scope == 'HFO':
        tool = 'hfo_postflight'
        payload = {
            'preflight_receipt_id': args.preflight_receipt_id,
            'outcome': args.outcome,
            'summary': args.summary,
            'changes': _csv(args.changes),
            'sources': _csv(args.sources),
            'scope': args.scope,
            'subshard_path': subshard_path,
            'write_memory': write_memory,
        }
    else:
        tool = 'port_postflight' if args.scope != 'P6' else 'port6_postflight'
        if tool == 'port6_postflight':
            payload = {
                'preflight_receipt_id': args.preflight_receipt_id,
                'outcome': args.outcome,
                'summary': args.summary,
                'changes': _csv(args.changes),
                'sources': _csv(args.sources),
                'scope': args.scope,
                'subshard_path': subshard_path,
                'write_memory': write_memory,
            }
        else:
            payload = {
                'port': int(args.port_num),
                'preflight_receipt_id': args.preflight_receipt_id,
                'outcome': args.outcome,
                'summary': args.summary,
                'changes': _csv(args.changes),
                'sources': _csv(args.sources),
                'scope': args.scope,
                'subshard_path': subshard_path,
                'write_memory': write_memory,
            }

    out = asyncio.run(mod.handle_call_tool(tool, payload))
    text = "\n".join([getattr(x, 'text', str(x)) for x in out]).strip()
    print(text)

else:
    raise SystemExit('Error: cmd must be preflight or postflight')
PY
)

cmd_arg="$cmd"

# shellcheck disable=SC2086
out=$(
  bash scripts/mcp_env_wrap.sh ./.venv/bin/python - \
    --cmd "$cmd_arg" \
    --scope "$scope" \
    --role "$role" \
    --note "$note" \
    --write_memory "$write_memory" \
    ${port_num:+--port_num "$port_num"} \
    --subshard_json "$subshard_json" \
    --preflight_receipt_id "$preflight_receipt_id" \
    --outcome "$outcome" \
    --summary "$summary" \
    --sources "$sources" \
    --changes "$changes" \
    <<PY
$python_code
PY
)

if [[ -n "$out_path" ]]; then
  mkdir -p "$(dirname "$out_path")"
  printf '%s\n' "$out" > "$out_path"
fi

printf '%s\n' "$out"
