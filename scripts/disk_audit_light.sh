#!/usr/bin/env bash
set -euo pipefail

# Low-impact disk snapshot for Gen88/Crostini.
# Writes proof logs to artifacts/forensics/ and avoids deep scans.

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"

log_dir="$root_dir/artifacts/forensics"
mkdir -p "$log_dir"
ts="$(date -Iseconds | tr ':' '-')"
log_file="$log_dir/disk_audit_light_${ts}.log"

{
  echo "## disk_audit_light $(date -Iseconds)";
  echo;
  echo "### df (top)";
  df -hT | head -n 40 || true;

  echo;
  echo "### workspace root sizes (max-depth=2)";
  echo "(bounded; may take a moment)";
  du -xh --max-depth=2 \
    ./hfo_hot_obsidian \
    ./hfo_cold_obsidian \
    ./hfo_gen_88_cb_v2 \
    ./artifacts \
    ./.git \
    2>/dev/null | sort -h | tail -n 60 || true;

  echo;
  echo "### biggest files (workspace root only)";
  # Keep this shallow to avoid walking massive trees.
  find . -maxdepth 2 -type f -printf '%s\t%p\n' 2>/dev/null \
    | sort -nr | head -n 40 \
    | awk '{ sz=$1; $1=""; sub(/^\t/,"",$0); printf("%10.2f MiB\t%s\n", sz/1024/1024, $0) }' || true;

  echo;
  echo "WROTE $log_file";
} | tee "$log_file"
