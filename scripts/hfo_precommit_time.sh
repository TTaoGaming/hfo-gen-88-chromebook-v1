#!/usr/bin/env bash
set -euo pipefail

label="${1:-hook}"
shift || true

echo "[pre-commit][${label}] starting..."
# Use shell builtin time for portability
TIMEFORMAT='[pre-commit]['"$label"'] elapsed %3R s'
{ time "$@"; }
