#!/usr/bin/env bash
set -euo pipefail

# agent_stop.sh
# Stops common always-on offenders without killing VS Code itself.
# Default: stop Playwright + MCP. Use --ollama to also stop Ollama.

stop_ollama=0
if [[ "${1:-}" == "--ollama" ]]; then
  stop_ollama=1
  shift
fi

log_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../artifacts/forensics" && pwd)"
mkdir -p "$log_dir"
ts="$(date -Iseconds | tr ':' '-')"
log_file="$log_dir/agent_stop_${ts}.log"

{
  echo "## agent_stop $(date -Iseconds)";
  echo;
  echo "### BEFORE";
  ./scripts/agent_status_light.sh || true;

  echo;
  echo "### STOP (TERM)";
  pkill -TERM -f '@playwright/test/cli.js test-server' 2>/dev/null || true;
  pkill -TERM -f 'mcp-server-' 2>/dev/null || true;
  pkill -TERM -f 'tavily-mcp|context7-mcp|@modelcontextprotocol/server-|@upstash/context7-mcp' 2>/dev/null || true;
  if [[ $stop_ollama -eq 1 ]]; then
    pkill -TERM -f 'ollama serve' 2>/dev/null || true;
  fi
  sleep 2;

  echo;
  echo "### AFTER";
  ./scripts/agent_status_light.sh || true;

  echo;
  echo "WROTE $log_file";
} | tee "$log_file"
