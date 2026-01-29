#!/usr/bin/env bash
set -euo pipefail

# Medallion: Bronze | Mutation: 0% | HIVE: V
# HFO Gen88 PSPS StrangeLoop (Preflight → Stigmergy → Postflight → Continuity)
# - Preflight: scripts/hfo_flight.sh preflight
# - Stigmergy: proof artifact + blackboard append
# - Postflight: scripts/hfo_flight.sh postflight
# - StrangeLoop: next preflight consumes previous postflight via continuity state

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/hfo_gen88_psps_strangeloop.sh \
    --scope <HFO|P6|P0.3.5.7.1> \
    --note "<objective (1 line)>" \
    --slug "<slug>" \
    --title "<title>" \
    --summary "<postflight summary (1-2 sentences)>" \
    [--outcome ok|partial|error] \
    [--sources a,b,c] \
    [--changes a,b,c] \
    [--max-attempts 1|2|3|...] \
    [--retry-sleep-sec 0|1|2|...] \
    [--no-strangeloop]

Notes:
  - Defaults to StrangeLoop ON: reads artifacts/flight/psps_continuity_latest.json if present.
  - Stigmergy blackboard path is pointer-resolved from hfo_pointers.json.
  - Fails closed if receipt ids cannot be extracted.
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
strangeloop="1"
max_attempts="3"
retry_sleep_sec="1"

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
    --max-attempts) max_attempts="${2:-}"; shift 2;;
    --retry-sleep-sec) retry_sleep_sec="${2:-}"; shift 2;;
    --no-strangeloop) strangeloop="0"; shift 1;;
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

if [[ ! "$max_attempts" =~ ^[0-9]+$ || "$max_attempts" -lt 1 ]]; then
  echo "Error: --max-attempts must be an integer >= 1" >&2
  exit 2
fi

if [[ ! "$retry_sleep_sec" =~ ^[0-9]+$ || "$retry_sleep_sec" -lt 0 ]]; then
  echo "Error: --retry-sleep-sec must be an integer >= 0" >&2
  exit 2
fi

ts_compact="$(date -u +%Y_%m_%dT%H%M%SZ)"
mkdir -p artifacts/flight

turn_id="$(python3 - <<'PY'
import uuid
print(uuid.uuid4().hex)
PY
)"

# Pointer-blessed hot obsidian blackboard path (required every turn)
blackboard_path="$(python3 - <<'PY'
import json
from pathlib import Path

p = Path('hfo_pointers.json')
data = json.loads(p.read_text(encoding='utf-8'))
paths = data.get('paths') or {}

# Prefer the hot-forge v4 blackboard, then the generic blackboard.
print((paths.get('blackboard_hot_forge') or paths.get('blackboard') or '').strip())
PY
)"

legacy_blackboard_path="$(python3 - <<'PY'
import json
from pathlib import Path

p = Path('hfo_pointers.json')
data = json.loads(p.read_text(encoding='utf-8'))
paths = data.get('paths') or {}
print((paths.get('blackboard_legacy') or '').strip())
PY
)"

if [[ -z "$blackboard_path" ]]; then
  echo "FAIL-CLOSED: could not resolve pointer-blessed hot obsidian blackboard path from hfo_pointers.json" >&2
  exit 1
fi

mkdir -p "$(dirname "$blackboard_path")"

# Ensure blackboards are writable (append-only JSONL requires write permission).
touch "$blackboard_path"
chmod u+w "$blackboard_path" 2>/dev/null || true
if [[ -n "$legacy_blackboard_path" ]]; then
  mkdir -p "$(dirname "$legacy_blackboard_path")"
  touch "$legacy_blackboard_path" 2>/dev/null || true
  chmod u+w "$legacy_blackboard_path" 2>/dev/null || true
fi

if [[ ! -w "$blackboard_path" ]]; then
  echo "FAIL-CLOSED: blackboard is not writable: $blackboard_path" >&2
  ls -l "$blackboard_path" >&2 || true
  exit 1
fi

append_signal() {
  local phase="$1"
  local attempt="$2"

  PSPS_BLACKBOARD_PATH="$blackboard_path" \
  PSPS_TURN_ID="$turn_id" \
  PSPS_PHASE="$phase" \
  PSPS_ATTEMPT="$attempt" \
  PSPS_SCOPE="$scope" \
  PSPS_MODE="hfo-gen88-psps-strangeloop" \
  PSPS_PREV_POSTFLIGHT_RECEIPT_ID="$prev_postflight_receipt_id" \
  PSPS_PREFLIGHT_RECEIPT_ID="$preflight_receipt_id" \
  PSPS_POSTFLIGHT_RECEIPT_ID="$postflight_receipt_id" \
  PSPS_PREFLIGHT_JSON_PATH="$pre_out" \
  PSPS_POSTFLIGHT_JSON_PATH="$post_out" \
  PSPS_ARTIFACT_PATH="$artifact_path" \
  PSPS_ARTIFACT_SHA256_PRE="$artifact_sha256_pre" \
  PSPS_ARTIFACT_SHA256_FINAL="$artifact_sha256_final" \
  PSPS_OUTCOME="$outcome" \
  python3 - <<'PY'
import json
import os
from datetime import datetime, timezone

def _env(key: str) -> str:
  return str(os.environ.get(key) or '').strip()

def _maybe_int(s: str):
  s = (s or '').strip()
  if not s:
    return None
  try:
    return int(s)
  except Exception:
    return None

event = {
  'ts_utc': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
  'kind': 'psps_signal',
  'mode': _env('PSPS_MODE'),
  'turn_id': _env('PSPS_TURN_ID'),
  'phase': _env('PSPS_PHASE'),
  'attempt': _maybe_int(_env('PSPS_ATTEMPT')),
  'scope': _env('PSPS_SCOPE'),
}

for k, env_key in [
  ('prev_postflight_receipt_id', 'PSPS_PREV_POSTFLIGHT_RECEIPT_ID'),
  ('preflight_receipt_id', 'PSPS_PREFLIGHT_RECEIPT_ID'),
  ('postflight_receipt_id', 'PSPS_POSTFLIGHT_RECEIPT_ID'),
  ('preflight_json_path', 'PSPS_PREFLIGHT_JSON_PATH'),
  ('postflight_json_path', 'PSPS_POSTFLIGHT_JSON_PATH'),
  ('artifact_path', 'PSPS_ARTIFACT_PATH'),
  ('artifact_sha256_pre', 'PSPS_ARTIFACT_SHA256_PRE'),
  ('artifact_sha256_final', 'PSPS_ARTIFACT_SHA256_FINAL'),
  ('outcome', 'PSPS_OUTCOME'),
]:
  v = _env(env_key)
  if v:
    event[k] = v

bb = _env('PSPS_BLACKBOARD_PATH')
if not bb:
  raise SystemExit('missing PSPS_BLACKBOARD_PATH')

with open(bb, 'a', encoding='utf-8') as f:
  f.write(json.dumps(event, ensure_ascii=False) + '\n')
PY
}

continuity_latest="artifacts/flight/psps_continuity_latest.json"
continuity_out="artifacts/flight/psps_continuity_${scope}_${ts_compact}.json"

prev_block=""
prev_postflight_receipt_id=""
if [[ "$strangeloop" == "1" && -f "$continuity_latest" ]]; then
  prev_block="$(python3 - <<'PY'
import json
import sys
from pathlib import Path

p = Path(sys.argv[1])
try:
  data = json.loads(p.read_text(encoding='utf-8'))
except Exception:
  data = {}

prev = data.get('previous_postflight') or {}
prev_id = str(prev.get('receipt_id') or '').strip()
prev_scope = str(prev.get('scope') or '').strip()
prev_outcome = str(prev.get('outcome') or '').strip()
prev_summary = str(prev.get('summary') or '').strip()
prev_artifact = str(prev.get('artifact_path') or '').strip()

def compact(s: str, max_len: int) -> str:
  s = ' '.join((s or '').split())
  return (s[: max_len - 1] + '…') if len(s) > max_len else s

if prev_id:
  # One-line compact block safe for flight preflight note.
  block = f" prev_postflight={{id={prev_id} scope={prev_scope} outcome={prev_outcome} summary='{compact(prev_summary,120)}' artifact='{compact(prev_artifact,120)}'}}"
  print(block)
  print(prev_id, file=sys.stderr)
PY
"$continuity_latest" 2>"/tmp/psps_prev_id_${ts_compact}.txt" || true)"
  if [[ -f "/tmp/psps_prev_id_${ts_compact}.txt" ]]; then
    prev_postflight_receipt_id="$(tr -d '\n' </tmp/psps_prev_id_${ts_compact}.txt | tail -c 32 || true)"
  fi
fi

effective_note="$note$prev_block"

pre_out="artifacts/flight/preflight_${scope}_${ts_compact}.json"
post_out="artifacts/flight/postflight_${scope}_${ts_compact}.json"

artifact_path=""
artifact_sha256_pre=""
artifact_sha256_final=""
postflight_receipt_id=""

# 1) Preflight
preflight_stdout="$(bash scripts/hfo_flight.sh preflight --scope "$scope" --note "$effective_note" --out "$pre_out" 2>&1)" || {
  echo "$preflight_stdout" >&2
  echo "FAIL-CLOSED: preflight failed" >&2
  exit 1
}

preflight_receipt_id="$(python3 - <<PY
import json

text = open(0, 'r', encoding='utf-8').read()
receipt_id = ''
try:
  decoder = json.JSONDecoder()
  for i, ch in enumerate(text):
    if ch != '{':
      continue
    try:
      obj, _ = decoder.raw_decode(text, i)
    except Exception:
      continue
    if isinstance(obj, dict) and obj.get('receipt_id'):
      receipt_id = str(obj.get('receipt_id') or '').strip()
      break
except Exception:
    pass

if not receipt_id:
  try:
    file_text = open('${pre_out}', 'r', encoding='utf-8').read()
    decoder = json.JSONDecoder()
    for i, ch in enumerate(file_text):
      if ch != '{':
        continue
      try:
        obj, _ = decoder.raw_decode(file_text, i)
      except Exception:
        continue
      if isinstance(obj, dict) and obj.get('receipt_id'):
        receipt_id = str(obj.get('receipt_id') or '').strip()
        break
  except Exception:
    receipt_id = ''

print(receipt_id)
PY
<<<"$preflight_stdout")"

if [[ -z "$preflight_receipt_id" || ${#preflight_receipt_id} -lt 6 ]]; then
  echo "FAIL-CLOSED: could not extract preflight_receipt_id" >&2
  echo "$preflight_stdout" >&2
  exit 1
fi

# Signal 1/3 (minimum): preflight
append_signal "preflight_ok" "1"

# 2) Stigmergy (artifact) — must be Markdown in hot bronze for now
artifact_path="$(python3 scripts/hfo_make_turn_artifact.py \
  --mode hfo-gen88-psps-strangeloop \
  --slug "$slug" \
  --title "$title" \
  --out-root hfo_hot_obsidian/bronze/3_resources/proofs \
  --no-stigmergy)"

{
  echo
  echo "## PSPS Proof Bundle"
  echo
  echo "- scope: $scope"
  echo "- note: $note"
  if [[ -n "$prev_postflight_receipt_id" ]]; then
    echo "- prev_postflight_receipt_id: $prev_postflight_receipt_id"
  fi
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

artifact_sha256_pre="$(sha256sum "$artifact_path" | awk '{print $1}')"

# Signal 2/3 (minimum): stigmergy
append_signal "stigmergy_ok" "1"

# 3) Postflight gate (bounded retries)
attempt="1"
postflight_stdout=""
postflight_exit="0"

while [[ "$attempt" -le "$max_attempts" ]]; do
  set +e
  postflight_stdout="$(bash scripts/hfo_flight.sh postflight --scope "$scope" --preflight-receipt-id "$preflight_receipt_id" --summary "$summary" --outcome "$outcome" --sources "$sources" --changes "$changes" --out "$post_out" 2>&1)"
  postflight_exit="$?"
  set -e

  postflight_receipt_id="$(python3 - <<PY
import json
  try:
    text = open('${post_out}', 'r', encoding='utf-8').read()
    decoder = json.JSONDecoder()
    receipt_id = ''
    for i, ch in enumerate(text):
      if ch != '{':
        continue
      try:
        obj, _ = decoder.raw_decode(text, i)
      except Exception:
        continue
      if isinstance(obj, dict) and obj.get('receipt_id'):
        receipt_id = str(obj.get('receipt_id') or '').strip()
        break
    print(receipt_id)
  except Exception:
    print('')
PY
)"

  if [[ "$postflight_exit" -eq 0 && -n "$postflight_receipt_id" && ${#postflight_receipt_id} -ge 6 ]]; then
    break
  fi

  # Emit failure signal (counts toward proof; still fail-closed if we exhaust attempts)
  append_signal "postflight_failed" "$attempt"

  if [[ "$attempt" -ge "$max_attempts" ]]; then
    echo "$postflight_stdout" >&2
    echo "FAIL-CLOSED: postflight failed after ${max_attempts} attempt(s)" >&2
    exit 1
  fi

  sleep "$retry_sleep_sec"
  attempt="$((attempt + 1))"
done

if [[ -z "$postflight_receipt_id" || ${#postflight_receipt_id} -lt 6 ]]; then
  echo "FAIL-CLOSED: could not extract postflight_receipt_id" >&2
  echo "$postflight_stdout" >&2
  exit 1
fi

{
  echo
  echo "## Postflight Output (proof)"
  echo
  echo "\`\`\`"
  echo "$postflight_stdout"
  echo "\`\`\`"
} >>"$artifact_path"

artifact_sha256_final="$(sha256sum "$artifact_path" | awk '{print $1}')"

# Signal 3/3 (minimum): postflight
append_signal "postflight_ok" "$attempt"

# 4) StrangeLoop continuity state (for next preflight)
python3 - <<PY
import json
from datetime import datetime, timezone

continuity = {
  "ts_utc": datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
  "mode": "hfo-gen88-psps-strangeloop",
  "turn_id": ${turn_id!r},
  "blackboard_path": ${blackboard_path!r},
  "previous_postflight": {
    "receipt_id": ${postflight_receipt_id!r},
    "scope": ${scope!r},
    "outcome": ${outcome!r},
    "summary": ${summary!r},
    "artifact_path": ${artifact_path!r},
    "artifact_sha256_final": ${artifact_sha256_final!r},
    "postflight_json_path": ${post_out!r},
    "preflight_receipt_id": ${preflight_receipt_id!r},
    "preflight_json_path": ${pre_out!r},
  }
}

for path in (${continuity_out!r}, ${continuity_latest!r}):
  with open(path, 'w', encoding='utf-8') as f:
    json.dump(continuity, f, ensure_ascii=False, indent=2)
    f.write('\n')
PY

# Emit a compact summary for chaining.
python3 - <<PY
import json
print(json.dumps({
  'mode': 'hfo-gen88-psps-strangeloop',
  'scope': ${scope!r},
  'turn_id': ${turn_id!r},
  'preflight_receipt_id': ${preflight_receipt_id!r},
  'postflight_receipt_id': ${postflight_receipt_id!r},
  'artifact_path': ${artifact_path!r},
  'blackboard_path': ${blackboard_path!r},
  'continuity_latest': ${continuity_latest!r},
}, ensure_ascii=False))
PY
