#!/usr/bin/env bash
set -euo pipefail

# Medallion: Bronze | Mutation: 0% | HIVE: V
# HFO P4 Basic 4-beat wrapper: Preflight → Payload → Postflight → Payoff
# Authority: Port 4 (Red Regnant)

usage() {
  cat <<'USAGE'
Usage:
  bash scripts/hfo_p4_basic_4beat.sh \
    --note "<objective (1 line)>" \
    --slug "<slug>" \
    --title "<title>" \
    --summary "<postflight summary (1-2 sentences)>" \
    [--outcome ok|partial|error] \
    [--sources a,b,c] \
    [--changes a,b,c] \
    [--max-attempts 1|2|3|...] \
    [--retry-sleep-sec 0|1|2|...]
USAGE
}

note=""
slug=""
title=""
summary=""
outcome="ok"
sources=""
changes=""
max_attempts="3"
retry_sleep_sec="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --note) note="${2:-}"; shift 2;;
    --slug) slug="${2:-}"; shift 2;;
    --title) title="${2:-}"; shift 2;;
    --summary) summary="${2:-}"; shift 2;;
    --outcome) outcome="${2:-}"; shift 2;;
    --sources) sources="${2:-}"; shift 2;;
    --changes) changes="${2:-}"; shift 2;;
    --max-attempts) max_attempts="${2:-}"; shift 2;;
    --retry-sleep-sec) retry_sleep_sec="${2:-}"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2;;
  esac
done

if [[ -z "$note" || -z "$slug" || -z "$title" || -z "$summary" ]]; then
  echo "Error: --note, --slug, --title, --summary are required" >&2
  usage
  exit 2
fi

bash scripts/hfo_gen88_p3s_strangeloop.sh \
  --scope P4 \
  --note "$note" \
  --slug "$slug" \
  --title "$title" \
  --summary "$summary" \
  --outcome "$outcome" \
  --sources "$sources" \
  --changes "$changes" \
  --max-attempts "$max_attempts" \
  --retry-sleep-sec "$retry_sleep_sec" \
  --mode-id "hfo-p4-basic-4beat" \
  --event-prefix "hfo.gen88.p4.basic" \
  --event-source "hfo://gen88/p4/basic" \
  --handoff-stage "payoff" \
  --continuity-prefix "p4_basic"
