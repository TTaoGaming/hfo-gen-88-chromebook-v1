#!/usr/bin/env bash
set -euo pipefail

# cache_cleanup_safe.sh
# Goal: reclaim disk safely by quarantining large *cache* directories.
# Strategy: rename/move within the same filesystem (fast + reversible).
# Default: dry-run. Use --apply to actually quarantine.

apply=0
if [[ "${1:-}" == "--apply" ]]; then
  apply=1
  shift
fi

home_dir="${HOME:-/home/tommytai3}"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
log_dir="$repo_root/artifacts/forensics"
mkdir -p "$log_dir"
ts="$(date -Iseconds | tr ':' '-')"
log_file="$log_dir/cache_cleanup_safe_${ts}.log"

# Carefully scoped to caches only. Avoid deleting user data by default.
# (We intentionally do NOT touch ~/.config/Code/User/globalStorage or workspaceStorage here.)
targets=(
  "$home_dir/.cache/pip"
  "$home_dir/.cache/uv"
  "$home_dir/.cache/ms-playwright"
  "$home_dir/.cache/puppeteer"
  "$home_dir/.npm/_cacache"
  "$home_dir/.local/share/Trash/files"
)

# VS Code caches (lower risk than User/globalStorage/workspaceStorage)
# These may be recreated automatically.
vs_code_caches=(
  "$home_dir/.config/Code/Cache"
  "$home_dir/.config/Code/CachedData"
  "$home_dir/.config/Code/CachedExtensionVSIXs"
)

archive_root_default="$home_dir/_archive_dev_2026_1_14"

# Default quarantine root:
# - Prefer an archive-root quarantine folder if it exists (your requested behavior)
# - Otherwise fall back to a home-folder quarantine.
quarantine_root_default="$home_dir/_quarantine_cache_cleanup"
if [[ -d "$archive_root_default" ]]; then
  quarantine_root_default="$archive_root_default/0_quarantine/cache_cleanup"
fi

quarantine_root="${HFO_QUARANTINE_ROOT:-$quarantine_root_default}"
quarantine_dir="$quarantine_root/$ts"

size_line() {
  local path="$1"
  if [[ -e "$path" ]]; then
    du -sh "$path" 2>/dev/null | awk '{print $1"\t"$2}'
  fi
}

move_to_quarantine() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    return 0
  fi
  mkdir -p "$quarantine_dir"
  local base
  base="$(basename "$path")"
  local parent
  parent="$(dirname "$path")"

  # Preserve context: quarantine under a folder named after the original parent.
  local parent_tag
  parent_tag="$(echo "$parent" | sed 's|^/||; s|/|__|g')"
  local dest_dir="$quarantine_dir/$parent_tag"
  mkdir -p "$dest_dir"
  local dest="$dest_dir/$base"

  if [[ $apply -eq 0 ]]; then
    echo "DRYRUN mv '$path' '$dest'"
    return 0
  fi

  echo "mv '$path' '$dest'"
  mv "$path" "$dest"
}

{
  echo "## cache_cleanup_safe $(date -Iseconds)"
  echo "apply=$apply"
  echo

  echo "### BEFORE df (/ and home)"
  df -hT / "$home_dir" 2>/dev/null || df -hT / || true

  echo
  echo "### Candidates (sizes)"
  for p in "${targets[@]}"; do size_line "$p" || true; done
  for p in "${vs_code_caches[@]}"; do size_line "$p" || true; done

  echo
  echo "### Actions"
  for p in "${targets[@]}"; do move_to_quarantine "$p"; done
  for p in "${vs_code_caches[@]}"; do move_to_quarantine "$p"; done

  echo
  echo "### AFTER df (/ and home)"
  df -hT / "$home_dir" 2>/dev/null || df -hT / || true

  echo
  echo "### Quarantine location"
  echo "$quarantine_dir"
  if [[ $apply -eq 1 ]]; then
    echo "To permanently delete later (optional): rm -rf '$quarantine_dir'"
    echo "To restore a quarantined dir: mv it back to its original path."
  fi

  echo
  echo "WROTE $log_file"
} | tee "$log_file"
