#!/usr/bin/env bash
set -euo pipefail

# Loads repo-root .env (if present) into environment, then execs the given command.
# - Does not print secrets.
# - Does not override already-nonempty environment variables.

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
env_file="${repo_root}/.env"

flag_name=""
if [[ "${1:-}" == "--if-enabled" ]]; then
  flag_name="${2:-}"
  if [[ -z "$flag_name" ]]; then
    echo "mcp_env_wrap.sh: --if-enabled requires a flag name" >&2
    exit 2
  fi
  shift 2
fi

load_env_file() {
  local file="$1"
  [[ -f "$file" ]] || return 0

  while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    # Trim leading/trailing whitespace
    local line
    line="${raw_line}"
    line="${line#${line%%[![:space:]]*}}"
    line="${line%${line##*[![:space:]]}}"

    [[ -z "$line" ]] && continue
    [[ "$line" == \#* ]] && continue

    if [[ "$line" == export\ * ]]; then
      line="${line#export }"
      line="${line#${line%%[![:space:]]*}}"
    fi

    [[ "$line" != *"="* ]] && continue

    local key="${line%%=*}"
    local val="${line#*=}"

    # Trim spaces
    key="${key#${key%%[![:space:]]*}}"
    key="${key%${key##*[![:space:]]}}"
    val="${val#${val%%[![:space:]]*}}"
    val="${val%${val##*[![:space:]]}}"

    [[ -z "$key" ]] && continue

    # Strip simple surrounding quotes
    if [[ "$val" == "\""*"\"" ]]; then
      val="${val#\"}"
      val="${val%\"}"
    elif [[ "$val" == "'"*"'" ]]; then
      val="${val#\'}"
      val="${val%\'}"
    fi

    # Only set if missing or empty in current environment
    if [[ -z "${!key:-}" ]]; then
      export "${key}=${val}"
    fi
  done < "$file"
}

load_env_file "$env_file"

if [[ -n "$flag_name" ]]; then
  flag_val="${!flag_name:-}"
  shopt -s nocasematch
  if [[ ! "$flag_val" =~ ^(1|true|yes|on)$ ]]; then
    echo "mcp_env_wrap.sh: skipping (flag not enabled): $flag_name" >&2
    exit 0
  fi
  shopt -u nocasematch
fi

exec "$@"
