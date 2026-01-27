#!/usr/bin/env bash
set -euo pipefail

# Minimal-impact status snapshot: targeted pgrep + a single port check.
# Designed for low-resource Chromebook/Crostini environments.

echo "## agent_status_light $(date -Iseconds)"

echo "### Playwright test-server"
pgrep -fa '@playwright/test/cli.js test-server' || echo 'NONE'

echo "### MCP (npx/uvx)"
pgrep -fa 'mcp-server-|tavily-mcp|context7-mcp|@modelcontextprotocol/server-|@upstash/context7-mcp' || echo 'NONE'

echo "### Ollama"
pgrep -fa 'ollama serve' || echo 'NONE'

echo "### Port 11434 (ollama)"
ss -lptn 'sport = :11434' 2>/dev/null || echo 'NO LISTENER'
