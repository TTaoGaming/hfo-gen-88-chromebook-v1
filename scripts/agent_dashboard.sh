#!/usr/bin/env bash
set -euo pipefail

# Lightweight "central dashboard" snapshot for Gen88.
# Prints: time, load/mem, top suspects, listening ports, and where autostarts are configured.

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"

echo "## agent_dashboard $(date -Iseconds)"

echo
echo "### load/memory"
uptime || true
free -h || true

echo
echo "### disk"
df -hT | head -n 30 || true

echo
echo "### listening ports (first 80 lines)"
ss -lptun 2>/dev/null | head -n 80 || true

echo
echo "### always-on suspects (top 200 matches)"
ps aux | egrep -i 'ollama|playwright|mcp|node .*mcp|npm exec .*mcp|code --|pylance|python .*daemon|resource_shepherd|stigmergy_anchor|sentinel' | head -n 200 || true

echo
echo "### MCP configuration (workspace)"
if [[ -f .vscode/mcp.json ]]; then
  sed -n '1,120p' .vscode/mcp.json
else
  echo "(no .vscode/mcp.json)"
fi

echo
echo "### VS Code tasks autostart check (folderOpen)"
if [[ -f .vscode/tasks.json ]]; then
  if grep -q '"runOn": "folderOpen"' .vscode/tasks.json; then
    echo "WARNING: tasks.json still contains runOn=folderOpen"
    grep -n '"runOn": "folderOpen"' .vscode/tasks.json || true
  else
    echo "OK: no runOn=folderOpen found in .vscode/tasks.json"
  fi
else
  echo "(no .vscode/tasks.json)"
fi

echo
echo "### flags (.env)"
if [[ -f .env ]]; then
  echo "(showing only HFO_* lines)"
  grep -n '^HFO_' .env || true
else
  echo "(no .env; see feature_flags.env.example)"
fi
