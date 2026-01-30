# MCP Stack Recommendation (2026-01-18)

## Goal
Monthly rollups (Port 6 Kraken Keeper) for Mission Threads Alpha/Omega.

## Enable (minimum viable)
- filesystem
- memory
- sequential-thinking
- time
- tavily
- brave-search

## Optional (only if needed)
- microsoft/playwright-mcp (UI testing)
- web fetch (if not using tavily/brave)

## Disable (not required for monthly rollups)
- context7
- microsoft/markitdown
- DBCode - Database Management
- Jupyter
- Copilot Container Tools

## Notes
- Ensure Tavily/Brave MCP servers are enabled after reload.
- Current MCP config in .vscode/mcp.json is aligned with minimum stack + tavily/brave.
