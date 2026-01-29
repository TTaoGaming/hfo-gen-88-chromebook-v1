#!/usr/bin/env bash
set -euo pipefail

# Medallion: Bronze | Mutation: 0% | HIVE: V
# Smoke+verify for HFO Gen88 P4 Basic 4-beat wrapper.
# Verifies:
# - wrapper runs and returns parseable JSON
# - >=1 artifact: payload markdown + json exist
# - payload markdown is executive-summary-ish (min chars) 
# - exactly 4 stigmergy events for the turn_id are appended to the pointer-blessed blackboard

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/test_p4_basic_4beat.sh \
    [--slug <slug>] \
    [--min-payload-md-chars <int>]

Notes:
- Uses scripts/hfo_p4_basic_4beat.sh
- Uses pointer-blessed blackboard path returned by the wrapper.
USAGE
}

slug="p4_basic_test"
min_payload_md_chars="900"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --slug) slug="${2:-}"; shift 2;;
    --min-payload-md-chars) min_payload_md_chars="${2:-}"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2;;
  esac
done

if [[ -z "$slug" ]]; then
  echo "Error: --slug cannot be empty" >&2
  exit 2
fi

if [[ ! "$min_payload_md_chars" =~ ^[0-9]+$ || "$min_payload_md_chars" -lt 0 ]]; then
  echo "Error: --min-payload-md-chars must be an integer >= 0" >&2
  exit 2
fi

tmp_json="/tmp/p4_basic_test_last_run.json"

bash scripts/hfo_p4_basic_4beat.sh \
  --note "p4 basic agent test" \
  --slug "$slug" \
  --title "P4 Basic Agent Test" \
  --summary "validated 4-beat wrapper" \
  --outcome ok \
  | tee "$tmp_json" >/dev/null

python3 - "$tmp_json" "$min_payload_md_chars" <<'PY'
import json
import sys
from pathlib import Path

run_path = Path(sys.argv[1])
min_chars = int(sys.argv[2])

d = json.loads(run_path.read_text(encoding='utf-8'))
turn_id = d['turn_id']
scope = d['scope']
subject = f"{scope}:{turn_id}"

payload_md = Path(d['payload_md'])
payload_json = Path(d['payload_json'])
continuity_latest = Path(d['continuity_latest'])
blackboard_path = Path(d['blackboard_path'])

errors = []

def require_exists(p: Path, label: str):
  if not p.exists():
    errors.append(f"missing {label}: {p}")

require_exists(payload_md, 'payload_md')
require_exists(payload_json, 'payload_json')
require_exists(continuity_latest, 'continuity_latest')
require_exists(blackboard_path, 'blackboard_path')

if payload_md.exists() and min_chars > 0:
  size = payload_md.stat().st_size
  if size < min_chars:
    errors.append(f"payload_md too small: {size} < {min_chars} bytes")
  text = payload_md.read_text(encoding='utf-8', errors='replace')
  if 'Executive Summary' not in text:
    errors.append("payload_md missing 'Executive Summary' heading")

# Count stigmergy events.
required_types = [
  'hfo.gen88.p4.basic.preflight',
  'hfo.gen88.p4.basic.payload',
  'hfo.gen88.p4.basic.postflight',
  'hfo.gen88.p4.basic.payoff',
]
seen = {t: 0 for t in required_types}

if blackboard_path.exists():
  with blackboard_path.open('r', encoding='utf-8', errors='replace') as f:
    for line in f:
      line = line.strip()
      if not line:
        continue
      try:
        ev = json.loads(line)
      except Exception:
        continue
      if ev.get('subject') != subject:
        continue
      t = str(ev.get('type') or '')
      if t in seen:
        seen[t] += 1

missing = [t for t, c in seen.items() if c == 0]
total = sum(seen.values())

if missing:
  errors.append(f"missing event types: {missing}")

if total != 4:
  errors.append(f"expected exactly 4 events for subject={subject}, saw {total} ({seen})")

if errors:
  print("FAIL")
  for e in errors:
    print("-", e)
  print("\nRun summary:")
  print(json.dumps({
    'turn_id': turn_id,
    'subject': subject,
    'blackboard_path': str(blackboard_path),
    'payload_md': str(payload_md),
    'payload_json': str(payload_json),
    'continuity_latest': str(continuity_latest),
    'seen_events': seen,
  }, indent=2))
  raise SystemExit(1)

print("PASS")
print(json.dumps({
  'turn_id': turn_id,
  'subject': subject,
  'blackboard_path': str(blackboard_path),
  'payload_md': str(payload_md),
  'payload_json': str(payload_json),
  'continuity_latest': str(continuity_latest),
  'seen_events': seen,
}, indent=2))
PY