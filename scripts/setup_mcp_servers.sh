#!/bin/bash
# Medallion: Bronze | Mutation: 0% | HIVE: I
# 🕸️ Setup script for HFO MCP Tooling (Standard Servers)

echo "Initializing HFO MCP Tooling Setup..."

# Sequential Thinking Server (Anthropic)
echo "Installing Sequential Thinking MCP Server..."
# We use npx to run it, but we can pre-cache it.
npx -y @modelcontextprotocol/server-sequential-thinking --help > /dev/null

echo "MCP Servers cached and ready."

# Instructions for VS Code Configuration
echo "------------------------------------------------"
echo "To enable these tools in your VS Code / Claude Desktop:"
echo "Add the following to your mcpSettings.json:"
echo ""
echo '  "sequential-thinking": {'
echo '    "command": "npx",'
echo '    "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]'
echo '  }'
echo "------------------------------------------------"
