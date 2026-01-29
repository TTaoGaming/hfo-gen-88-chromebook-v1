#!/usr/bin/env bash
set -euo pipefail

# Medallion: Bronze | Mutation: 0% | HIVE: V
# HFO Gen88 Preflight → Artifact → Postflight (ritual wrapper)
# - Uses existing flight runner + proof artifact writer
# - Writes auditable JSON receipts to artifacts/flight/

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/hfo_gen88_preflight_artifact_postflight.sh \
    --scope <HFO|P6|P0.3.5.7.1> \
    --note "<objective (1 line)>" \
    --slug "<slug>" \
    --title "<title>" \
    --summary "<postflight summary (1-2 sentences)>" \
    [--outcome ok|partial|error] \
    [--sources a,b,c] \
    [--changes a,b,c]

Notes:
  - Creates a timestamped proof artifact and appends stigmergy JSONL.
  - Fails closed if it cannot extract a preflight receipt id.
USAGE
}

scope=""
note=""
slug=""
title=""
summary=""
outcome="ok"
sources=""
changes=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope) scope="${2:-}"; shift 2;;
    --note) note="${2:-}"; shift 2;;
    --slug) slug="${2:-}"; shift 2;;
    --title) title="${2:-}"; shift 2;;
    --summary) summary="${2:-}"; shift 2;;
    --outcome) outcome="${2:-}"; shift 2;;
    --sources) sources="${2:-}"; shift 2;;
    --changes) changes="${2:-}"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2;;
  esac
done

if [[ -z "$scope" || -z "$note" || -z "$slug" || -z "$title" || -z "$summary" ]]; then
  echo "Error: --scope, --note, --slug, --title, --summary are required" >&2
  usage
  exit 2
fi

if [[ "$outcome" != "ok" && "$outcome" != "partial" && "$outcome" != "error" ]]; then
  echo "Error: --outcome must be ok|partial|error" >&2
  exit 2
fi

ts_compact="$(date -u +%Y_%m_%dT%H%M%SZ)"
mkdir -p artifacts/flight
pre_out="artifacts/flight/preflight_${scope}_${ts_compact}.json"
post_out="artifacts/flight/postflight_${scope}_${ts_compact}.json"

# 1) Preflight
preflight_stdout="$(bash scripts/hfo_flight.sh preflight --scope "$scope" --note "$note" --out "$pre_out" 2>&1)" || {
  echo "$preflight_stdout" >&2
  echo "FAIL-CLOSED: preflight failed" >&2
  exit 1
}

preflight_receipt_id="$(python3 - <<PY
import json
import sys

def parse_multi_json(text: str):
    decoder = json.JSONDecoder()
    idx = 0
    out = []
    while idx < len(text):
        while idx < len(text) and text[idx].isspace():
            idx += 1
        if idx >= len(text):
            break
        obj, next_idx = decoder.raw_decode(text, idx)
        out.append(obj)
        idx = next_idx
    return out

text = open(0, 'r', encoding='utf-8').read()
objs = []
try:
    objs = parse_multi_json(text)
except Exception:
    # Ignore; will fallback to file.
    pass

receipt_id = ''
for obj in objs:
    if isinstance(obj, dict) and obj.get('receipt_id'):
        receipt_id = str(obj.get('receipt_id') or '').strip()

if not receipt_id:
    try:
        data = json.load(open('${pre_out}', 'r', encoding='utf-8'))
        receipt_id = str(data.get('receipt_id') or '').strip()
    except Exception:
        receipt_id = ''

print(receipt_id)
PY
<<<"$preflight_stdout")"

if [[ -z "$preflight_receipt_id" || ${#preflight_receipt_id} -lt 6 ]]; then
  echo "FAIL-CLOSED: could not extract preflight_receipt_id" >&2
  echo "preflight stdout follows:" >&2
  echo "$preflight_stdout" >&2
  exit 1
fi

# 2) Proof artifact
artifact_path="$(python3 scripts/hfo_make_turn_artifact.py --mode hfo-gen88-preflight-artifact-postflight --slug "$slug" --title "$title")"

# Ensure the artifact contains receipts/proof links immediately.
{
  echo
  echo "## Proof Bundle"
  echo
  echo "- scope: $scope"
  echo "- preflight_receipt_id: $preflight_receipt_id"
  echo "- preflight_json_path: $pre_out"
  echo "- artifact_path: $artifact_path"
  echo
  echo "## Postflight (pending)"
  echo
  echo "- postflight_json_path: $post_out"
  echo "- summary: $summary"
  echo "- outcome: $outcome"
  if [[ -n "$sources" ]]; then
    echo "- sources: $sources"
  fi
  if [[ -n "$changes" ]]; then
    echo "- changes: $changes"
  fi
} >>"$artifact_path"

# 3) Postflight
postflight_stdout="$(bash scripts/hfo_flight.sh postflight --scope "$scope" --preflight-receipt-id "$preflight_receipt_id" --summary "$summary" --outcome "$outcome" --sources "$sources" --changes "$changes" --out "$post_out" 2>&1)" || {
  echo "$postflight_stdout" >&2
  echo "FAIL-CLOSED: postflight failed" >&2
  exit 1
}

# Append postflight stdout as proof.
{
  echo
  echo "## Postflight Output (proof)"
  echo
  echo "\`\`\`"
  echo "$postflight_stdout"
  echo "\`\`\`"
} >>"$artifact_path"

# Emit a compact summary for chaining.
python3 - <<PY
import json
print(json.dumps({
  'scope': ${scope!r},
  'preflight_receipt_id': ${preflight_receipt_id!r},
  'preflight_json_path': ${pre_out!r},
  'postflight_json_path': ${post_out!r},
  'artifact_path': ${artifact_path!r},
}, ensure_ascii=False))
PY
