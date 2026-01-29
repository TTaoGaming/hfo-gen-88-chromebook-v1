#!/usr/bin/env bash
set -euo pipefail

# Medallion: Bronze | Mutation: 0% | HIVE: V
# HFO Gen88 P3S StrangeLoop (Preflight → Payload(stigmergy) → Postflight → Handoff/Continuity)
#
# Design goals:
# - Fail-closed.
# - Pointer-blessed blackboard only.
# - Robust receipt_id extraction (parse from --out files, not stdout).
# - Payload bundle written to Hot Bronze.

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/hfo_gen88_p3s_strangeloop.sh \
    --scope <HFO|P6|P0.3.5.7.1> \
    --note "<objective (1 line)>" \
    --slug "<slug>" \
    --title "<title>" \
    --summary "<postflight summary (1-2 sentences)>" \
    [--outcome ok|partial|error] \
    [--payload-body-file <PATH.md>] \
    [--sources a,b,c] \
    [--changes a,b,c] \
    [--mode-id <id>] \
    [--event-prefix <prefix>] \
    [--event-source <source>] \
    [--handoff-stage <handoff|payoff|...>] \
    [--continuity-prefix <p3s|p4_basic|...>] \
    [--min-payload-md-chars <int>] \
    [--max-attempts 1|2|3|...] \
    [--retry-sleep-sec 0|1|2|...] \
    [--no-strangeloop]
USAGE
}

scope=""
note=""
slug=""
title=""
summary=""
outcome="ok"
payload_body_file=""
sources=""
changes=""
strangeloop="1"
mode_id="hfo-gen88-p3s-strangeloop"
event_prefix="hfo.gen88.p3s"
event_source="hfo://gen88/p3s"
handoff_stage="handoff"
continuity_prefix="p3s"
min_payload_md_chars="900"
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
    --payload-body-file) payload_body_file="${2:-}"; shift 2;;
    --sources) sources="${2:-}"; shift 2;;
    --changes) changes="${2:-}"; shift 2;;
    --mode-id) mode_id="${2:-}"; shift 2;;
    --event-prefix) event_prefix="${2:-}"; shift 2;;
    --event-source) event_source="${2:-}"; shift 2;;
    --handoff-stage) handoff_stage="${2:-}"; shift 2;;
    --continuity-prefix) continuity_prefix="${2:-}"; shift 2;;
    --min-payload-md-chars) min_payload_md_chars="${2:-}"; shift 2;;
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

if [[ -n "$payload_body_file" ]]; then
  if [[ ! -f "$payload_body_file" ]]; then
    echo "Error: --payload-body-file not found: $payload_body_file" >&2
    exit 2
  fi
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

if [[ ! "$min_payload_md_chars" =~ ^[0-9]+$ || "$min_payload_md_chars" -lt 0 ]]; then
  echo "Error: --min-payload-md-chars must be an integer >= 0" >&2
  exit 2
fi

if [[ -z "$mode_id" || -z "$event_prefix" || -z "$event_source" || -z "$handoff_stage" || -z "$continuity_prefix" ]]; then
  echo "Error: --mode-id, --event-prefix, --event-source, --handoff-stage, --continuity-prefix cannot be empty" >&2
  exit 2
fi

ts_compact="$(date -u +%Y_%m_%dT%H%M%SZ)"
turn_id="$(python3 - <<'PY'
import uuid
print(uuid.uuid4().hex)
PY
)"
turn_id="${turn_id//$'\n'/}"

mkdir -p artifacts/flight

continuity_latest="artifacts/flight/${continuity_prefix}_continuity_latest.json"
continuity_out="artifacts/flight/${continuity_prefix}_continuity_${scope}_${ts_compact}.json"

prev_block=""
prev_postflight_receipt_id=""
if [[ "$strangeloop" == "1" && -f "$continuity_latest" ]]; then
  prev_block="$(python3 - \
    "$continuity_latest" \
    "$continuity_prefix" <<'PY'
import json
import sys
from pathlib import Path

continuity_latest = sys.argv[1]
continuity_prefix = sys.argv[2]

p = Path(continuity_latest)
try:
  data = json.loads(p.read_text(encoding='utf-8'))
except Exception:
  data = {}

prev = data.get('previous_postflight') or {}
prev_id = str(prev.get('receipt_id') or '').strip()
prev_scope = str(prev.get('scope') or '').strip()
prev_outcome = str(prev.get('outcome') or '').strip()
prev_payload_sha = str((data.get('previous_payload') or {}).get('payload_sha256') or '').strip()

if prev_id:
  block = f" prev_{continuity_prefix}={{id={prev_id} scope={prev_scope} outcome={prev_outcome} payload_sha256={prev_payload_sha}}}"
  print(block)
  print(prev_id)
PY
)"
  prev_postflight_receipt_id="$(echo "$prev_block" | tail -n 1 | tr -d '\n' || true)"
  prev_block="$(echo "$prev_block" | head -n 1 || true)"
fi

effective_note="$note$prev_block"

# Pointer-blessed blackboard paths
blackboard_path="$(python3 - <<'PY'
import json
from pathlib import Path

p = Path('hfo_pointers.json')
data = json.loads(p.read_text(encoding='utf-8'))
paths = data.get('paths') or {}
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
  echo "FAIL-CLOSED: cannot resolve pointer-blessed blackboard path (blackboard_hot_forge|blackboard)" >&2
  exit 1
fi

mkdir -p "$(dirname "$blackboard_path")"
: > /dev/null
if [[ ! -f "$blackboard_path" ]]; then
  : > "$blackboard_path"
fi
chmod u+w "$blackboard_path" 2>/dev/null || true

if [[ -n "$legacy_blackboard_path" ]]; then
  mkdir -p "$(dirname "$legacy_blackboard_path")"
  if [[ ! -f "$legacy_blackboard_path" ]]; then
    : > "$legacy_blackboard_path" || true
  fi
  chmod u+w "$legacy_blackboard_path" 2>/dev/null || true
fi

if [[ ! -w "$blackboard_path" ]]; then
  echo "FAIL-CLOSED: blackboard not writable: $blackboard_path" >&2
  ls -l "$blackboard_path" >&2 || true
  exit 1
fi

emit_stage() {
  local stage="$1"              # preflight|payload|postflight|handoff|payoff
  local attempt="$2"
  local preflight_receipt_id="${3:-}"
  local postflight_receipt_id="${4:-}"
  local payload_md_path="${5:-}"
  local payload_md_sha256="${6:-}"
  local payload_json_path="${7:-}"
  local payload_json_sha256="${8:-}"
  local continuity_latest_path="${9:-}"

  P3S_BLACKBOARD_PATH="$blackboard_path" \
  P3S_STAGE="$stage" \
  P3S_TURN_ID="$turn_id" \
  P3S_ATTEMPT="$attempt" \
  P3S_SCOPE="$scope" \
  P3S_NOTE="$note" \
  P3S_SLUG="$slug" \
  P3S_TITLE="$title" \
  P3S_PREV_POSTFLIGHT_RECEIPT_ID="$prev_postflight_receipt_id" \
  P3S_PREFLIGHT_RECEIPT_ID="$preflight_receipt_id" \
  P3S_POSTFLIGHT_RECEIPT_ID="$postflight_receipt_id" \
  P3S_PAYLOAD_MD_PATH="$payload_md_path" \
  P3S_PAYLOAD_MD_SHA256="$payload_md_sha256" \
  P3S_PAYLOAD_JSON_PATH="$payload_json_path" \
  P3S_PAYLOAD_JSON_SHA256="$payload_json_sha256" \
  P3S_CONTINUITY_LATEST_PATH="$continuity_latest_path" \
  P3S_OUTCOME="$outcome" \
  P3S_SUMMARY="$summary" \
  P3S_MODE_ID="$mode_id" \
  P3S_EVENT_PREFIX="$event_prefix" \
  P3S_EVENT_SOURCE="$event_source" \
  P3S_CONTINUITY_PREFIX="$continuity_prefix" \
  python3 - <<'PY'
import os
from pathlib import Path

import hfo_blackboard_events as bb

def env(k: str) -> str:
  return str(os.environ.get(k) or '').strip()

def maybe_int(s: str):
  try:
    return int(s)
  except Exception:
    return None

stage = env('P3S_STAGE')
event_type = f"{env('P3S_EVENT_PREFIX')}.{stage}"
turn_id = env('P3S_TURN_ID')
scope = env('P3S_SCOPE')

data = {
  'mode': env('P3S_MODE_ID'),
  'stage': stage,
  'turn_id': turn_id,
  'attempt': maybe_int(env('P3S_ATTEMPT')),
  'scope': scope,
}

for k, ek in [
  ('note', 'P3S_NOTE'),
  ('slug', 'P3S_SLUG'),
  ('title', 'P3S_TITLE'),
  ('prev_postflight_receipt_id', 'P3S_PREV_POSTFLIGHT_RECEIPT_ID'),
  ('preflight_receipt_id', 'P3S_PREFLIGHT_RECEIPT_ID'),
  ('postflight_receipt_id', 'P3S_POSTFLIGHT_RECEIPT_ID'),
  ('payload_md_path', 'P3S_PAYLOAD_MD_PATH'),
  ('payload_md_sha256', 'P3S_PAYLOAD_MD_SHA256'),
  ('payload_json_path', 'P3S_PAYLOAD_JSON_PATH'),
  ('payload_json_sha256', 'P3S_PAYLOAD_JSON_SHA256'),
  ('continuity_latest_path', 'P3S_CONTINUITY_LATEST_PATH'),
  ('outcome', 'P3S_OUTCOME'),
  ('summary', 'P3S_SUMMARY'),
]:
  v = env(ek)
  if v:
    data[k] = v

bb_path = Path(env('P3S_BLACKBOARD_PATH'))
bb.emit_cloudevent_to_blackboard(
  event_type=event_type,
  source=env('P3S_EVENT_SOURCE'),
  subject=f"{scope}:{turn_id}",
  data=data,
  blackboard_path=bb_path,
)
PY
}

extract_receipt_id_from_file() {
  local path="$1"
  python3 - "$path" <<'PY'
import json
import sys

p = sys.argv[1]
try:
  text = open(p, 'r', encoding='utf-8').read()
except Exception:
  print('')
  raise SystemExit(0)

decoder = json.JSONDecoder()
for i, ch in enumerate(text):
  if ch != '{':
    continue
  try:
    obj, _ = decoder.raw_decode(text, i)
  except Exception:
    continue
  if isinstance(obj, dict) and obj.get('receipt_id'):
    print(str(obj.get('receipt_id') or '').strip())
    raise SystemExit(0)
print('')
PY
}

pre_out="artifacts/flight/preflight_${scope}_${ts_compact}.json"
post_out="artifacts/flight/postflight_${scope}_${ts_compact}.json"

# 1) Preflight (receipt via file)
preflight_stdout="$(bash scripts/hfo_flight.sh preflight --scope "$scope" --note "$effective_note" --out "$pre_out" 2>&1)" || {
  echo "$preflight_stdout" >&2
  echo "FAIL-CLOSED: preflight failed" >&2
  exit 1
}

preflight_receipt_id="$(extract_receipt_id_from_file "$pre_out")"
if [[ -z "$preflight_receipt_id" || ${#preflight_receipt_id} -lt 6 ]]; then
  echo "FAIL-CLOSED: could not extract preflight receipt_id from $pre_out" >&2
  echo "$preflight_stdout" >&2
  exit 1
fi

emit_stage "preflight" "1" "$preflight_receipt_id" "" "" "" "" "" ""

# 2) Payload (stigmergy) (Hot Bronze)
payload_root="$(python3 - <<'PY'
import json
from pathlib import Path

p = Path('hfo_pointers.json')
data = json.loads(p.read_text(encoding='utf-8'))
paths = data.get('paths') or {}
print((paths.get('p3s_payload_root') or 'hfo_hot_obsidian/bronze/3_resources/p3s_payloads').strip())
PY
)"
mkdir -p "$payload_root"

payload_base="${ts_compact}__${scope}__${slug}__${turn_id}"
payload_md="${payload_root}/${payload_base}.md"
payload_json="${payload_root}/${payload_base}.json"

cat >"$payload_md" <<MD
# Executive Summary (Payload)

## Snapshot

- ts_utc: ${ts_compact}
- scope: ${scope}
- turn_id: ${turn_id}
- preflight_receipt_id: ${preflight_receipt_id}
- note: ${note}

## Executive Summary

This payload is the canonical, durable artifact for this turn.
It is written before postflight, and it anchors stigmergy coordination.

## Objective

- Primary objective: ${note}
- Success criteria:
  - Preflight receipt exists and is referenced here.
  - Payload artifacts exist (this markdown + JSON manifest).
  - Postflight closes with a receipt_id.
  - Final beat emits a payoff/handoff event + continuity is refreshed.

## Scope + Constraints

- Scope: ${scope}
- Fail-closed: if any beat or event emission fails, stop.
- Blackboard must be pointer-blessed (no ad-hoc paths).

## Pointers (resolved)

- p3s_payload_root: ${payload_root}
- blackboard: ${blackboard_path}

## Plan (operator-facing)

1) Confirm preflight receipt_id
2) Review this payload for clarity and intent
3) Execute work (outside the payload artifact)
4) Close with postflight and payoff/handoff

## Risks / Notes

- If postflight fails, retries are bounded and the run is fail-closed.
- If blackboard is not writable, the run must fail-closed.

## Evidence (to be populated post-run)

- payload_md_sha256: (computed by wrapper)
- payload_json_sha256: (computed by wrapper)
- postflight_receipt_id: (written after postflight)

---

## Payload Body (operator-provided)

(Optional) Append additional detail below.
MD

if [[ -n "$payload_body_file" ]]; then
  {
    echo ""
    echo "---"
    echo ""
    echo "## Payload Body (operator-provided)"
    echo ""
    cat "$payload_body_file"
    echo ""
  } >>"$payload_md"
fi

if [[ "$min_payload_md_chars" -gt 0 ]]; then
  payload_md_chars="$(wc -c <"$payload_md" | tr -d ' ')"
  if [[ ! "$payload_md_chars" =~ ^[0-9]+$ ]]; then
    echo "FAIL-CLOSED: could not compute payload markdown size" >&2
    exit 1
  fi
  if [[ "$payload_md_chars" -lt "$min_payload_md_chars" ]]; then
    echo "FAIL-CLOSED: payload markdown too small (${payload_md_chars} chars < ${min_payload_md_chars}); refusing to proceed" >&2
    echo "payload_md=$payload_md" >&2
    exit 1
  fi
fi

python3 - \
  "$mode_id" \
  "$ts_compact" \
  "$scope" \
  "$turn_id" \
  "$note" \
  "$preflight_receipt_id" \
  "$payload_root" \
  "$blackboard_path" \
  "$payload_md" \
  "$payload_json" <<'PY'
import json
import sys

mode_id = sys.argv[1]
ts_utc = sys.argv[2]
scope = sys.argv[3]
turn_id = sys.argv[4]
note = sys.argv[5]
preflight_receipt_id = sys.argv[6]
payload_root = sys.argv[7]
blackboard_path = sys.argv[8]
payload_md = sys.argv[9]
payload_json = sys.argv[10]

payload = {
  'ts_utc': ts_utc,
  'mode': mode_id,
  'scope': scope,
  'turn_id': turn_id,
  'note': note,
  'preflight_receipt_id': preflight_receipt_id,
  'pointers': {
    'p3s_payload_root': payload_root,
    'blackboard_path': blackboard_path,
  },
  'payload_md': payload_md,
  'payload_json': payload_json,
}

with open(payload_json, 'w', encoding='utf-8') as f:
  json.dump(payload, f, ensure_ascii=False, indent=2)
  f.write('\n')
PY

payload_md_sha256="$(sha256sum "$payload_md" | awk '{print $1}')"
payload_json_sha256="$(sha256sum "$payload_json" | awk '{print $1}')"
emit_stage "payload" "1" "$preflight_receipt_id" "" "$payload_md" "$payload_md_sha256" "$payload_json" "$payload_json_sha256" ""

# 3) Postflight gate (bounded retries)
attempt="1"
postflight_stdout=""
postflight_exit="0"
postflight_receipt_id=""

while [[ "$attempt" -le "$max_attempts" ]]; do
  set +e
  postflight_stdout="$(bash scripts/hfo_flight.sh postflight --scope "$scope" --preflight-receipt-id "$preflight_receipt_id" --summary "$summary" --outcome "$outcome" --sources "$sources" --changes "$changes" --out "$post_out" 2>&1)"
  postflight_exit="$?"
  set -e

  postflight_receipt_id="$(extract_receipt_id_from_file "$post_out")"

  if [[ "$postflight_exit" -eq 0 && -n "$postflight_receipt_id" && ${#postflight_receipt_id} -ge 6 ]]; then
    break
  fi

  emit_stage "postflight" "$attempt" "$preflight_receipt_id" "$postflight_receipt_id" "$payload_md" "$payload_md_sha256" "$payload_json" "$payload_json_sha256" ""

  if [[ "$attempt" -ge "$max_attempts" ]]; then
    echo "$postflight_stdout" >&2
    echo "FAIL-CLOSED: postflight failed after ${max_attempts} attempt(s)" >&2
    exit 1
  fi

  sleep "$retry_sleep_sec"
  attempt="$((attempt + 1))"
done

emit_stage "postflight" "$attempt" "$preflight_receipt_id" "$postflight_receipt_id" "$payload_md" "$payload_md_sha256" "$payload_json" "$payload_json_sha256" ""

# 4) StrangeLoop continuity
python3 - \
  "$mode_id" \
  "$turn_id" \
  "$blackboard_path" \
  "$payload_json" \
  "$payload_md" \
  "$payload_json_sha256" \
  "$postflight_receipt_id" \
  "$scope" \
  "$outcome" \
  "$summary" \
  "$preflight_receipt_id" \
  "$post_out" \
  "$continuity_out" \
  "$continuity_latest" <<'PY'
import json
import sys
from datetime import datetime, timezone

mode_id = sys.argv[1]
turn_id = sys.argv[2]
blackboard_path = sys.argv[3]
payload_json = sys.argv[4]
payload_md = sys.argv[5]
payload_json_sha256 = sys.argv[6]
postflight_receipt_id = sys.argv[7]
scope = sys.argv[8]
outcome = sys.argv[9]
summary = sys.argv[10]
preflight_receipt_id = sys.argv[11]
post_out = sys.argv[12]
continuity_out = sys.argv[13]
continuity_latest = sys.argv[14]

continuity = {
  'ts_utc': datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
  'mode': mode_id,
  'turn_id': turn_id,
  'blackboard_path': blackboard_path,
  'previous_payload': {
    'payload_json_path': payload_json,
    'payload_md_path': payload_md,
    'payload_sha256': payload_json_sha256,
  },
  'previous_postflight': {
    'receipt_id': postflight_receipt_id,
    'scope': scope,
    'outcome': outcome,
    'summary': summary,
    'preflight_receipt_id': preflight_receipt_id,
    'postflight_json_path': post_out,
  }
}

for path in (continuity_out, continuity_latest):
  with open(path, 'w', encoding='utf-8') as f:
    json.dump(continuity, f, ensure_ascii=False, indent=2)
    f.write('\n')
PY

emit_stage "$handoff_stage" "1" "$preflight_receipt_id" "$postflight_receipt_id" "$payload_md" "$payload_md_sha256" "$payload_json" "$payload_json_sha256" "$continuity_latest"

# Emit compact JSON summary for chaining
python3 - \
  "$mode_id" \
  "$scope" \
  "$turn_id" \
  "$preflight_receipt_id" \
  "$postflight_receipt_id" \
  "$payload_json" \
  "$payload_md" \
  "$payload_md_sha256" \
  "$payload_json_sha256" \
  "$blackboard_path" \
  "$continuity_latest" <<'PY'
import json
import sys

mode_id = sys.argv[1]
scope = sys.argv[2]
turn_id = sys.argv[3]
preflight_receipt_id = sys.argv[4]
postflight_receipt_id = sys.argv[5]
payload_json = sys.argv[6]
payload_md = sys.argv[7]
payload_md_sha256 = sys.argv[8]
payload_json_sha256 = sys.argv[9]
blackboard_path = sys.argv[10]
continuity_latest = sys.argv[11]

print(json.dumps({
  'mode': mode_id,
  'scope': scope,
  'turn_id': turn_id,
  'preflight_receipt_id': preflight_receipt_id,
  'postflight_receipt_id': postflight_receipt_id,
  'payload_json': payload_json,
  'payload_md': payload_md,
  'payload_md_sha256': payload_md_sha256,
  'payload_json_sha256': payload_json_sha256,
  'blackboard_path': blackboard_path,
  'continuity_latest': continuity_latest,
}, ensure_ascii=False))
PY
