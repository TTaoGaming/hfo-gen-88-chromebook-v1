#!/usr/bin/env bash
set -euo pipefail

# Low-impact ledger footprint snapshot.
# Focuses on known directories + known extensions and writes proof logs.

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"

log_dir="$root_dir/artifacts/forensics"
mkdir -p "$log_dir"
ts="$(date -Iseconds | tr ':' '-')"
log_file="$log_dir/ledger_audit_light_${ts}.log"

scan_dirs=(
  "."
  "./hfo_hot_obsidian"
  "./hfo_cold_obsidian"
  "./hfo_gen_88_cb_v2"
  "./artifacts"
)

{
  echo "## ledger_audit_light $(date -Iseconds)";
  echo;
  echo "### targets";
  printf '%s\n' "${scan_dirs[@]}" | sed 's/^/- /';

  echo;
  echo "### largest *.duckdb (top 25)";
  find "${scan_dirs[@]}" -type f -name '*.duckdb' -printf '%s\t%p\n' 2>/dev/null \
    | sort -nr | head -n 25 \
    | awk '{ sz=$1; $1=""; sub(/^\t/,"",$0); printf("%10.2f MiB\t%s\n", sz/1024/1024, $0) }' || true;

  echo;
  echo "### largest *.jsonl (top 40)";
  find "${scan_dirs[@]}" -type f -name '*.jsonl' -printf '%s\t%p\n' 2>/dev/null \
    | sort -nr | head -n 40 \
    | awk '{ sz=$1; $1=""; sub(/^\t/,"",$0); printf("%10.2f MiB\t%s\n", sz/1024/1024, $0) }' || true;

  echo;
  echo "### totals (duckdb/jsonl only)";
  duckdb_total=$(find "${scan_dirs[@]}" -type f -name '*.duckdb' -printf '%s\n' 2>/dev/null | awk '{s+=$1} END{print s+0}')
  jsonl_total=$(find "${scan_dirs[@]}" -type f -name '*.jsonl' -printf '%s\n' 2>/dev/null | awk '{s+=$1} END{print s+0}')
  printf 'duckdb_total_mib\t%.2f\n' "$(awk -v s="$duckdb_total" 'BEGIN{print s/1024/1024}')"
  printf 'jsonl_total_mib\t%.2f\n' "$(awk -v s="$jsonl_total" 'BEGIN{print s/1024/1024}')"

  echo;
  echo "WROTE $log_file";
} | tee "$log_file"
