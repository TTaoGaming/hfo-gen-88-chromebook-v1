#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
# Medallion: Bronze | Mutation: 0% | HIVE: I
"""
🐝 HFO HEXAGONAL MCP HUB
Consolidated BMC2 Node for HFO Gen 88.
Integrates P0-P7 cognitive ports into a single Model Context Protocol gateway.

Pattern: Hexagonal Ports and Adapters
Hardware: Chromebook V-1 (Linux)
"""

import os
import sys
import json
import asyncio
import datetime
import hashlib
import sqlite3
import subprocess
import duckdb
from typing import Any, Dict, List, Optional
import mcp.server.stdio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types

# --- CONFIGURATION ---
BASE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
BLACKBOARD_PATH = os.path.join(BASE_PATH, "hfo_hot_obsidian/hot_obsidian_blackboard.jsonl")
DUCKDB_PATH = os.path.join(BASE_PATH, "hfo_gen_88_cb_v2/hfo_unified_v88.duckdb")

# --- UTILITIES ---

def log_to_blackboard(entry: Dict[str, Any]):
    """Append a cryptographically signed entry to the blackboard."""
    try:
        # Simple signature logic for Bronze (Matches resign_v2 rules)
        timestamp = entry.get("timestamp") or datetime.datetime.now(datetime.timezone.utc).isoformat()
        entry["timestamp"] = timestamp
        
        # Get last signature to chain if possible
        last_sig = "0" * 64
        if os.path.exists(BLACKBOARD_PATH):
            with open(BLACKBOARD_PATH, "rb") as f:
                f.seek(0, 2)
                pos = f.tell()
                if pos > 0:
                    f.seek(max(0, pos - 4096))
                    last_lines = f.read().decode('utf-8', errors='ignore').strip().split('\n')
                    if last_lines:
                        try:
                            last_entry = json.loads(last_lines[-1])
                            last_sig = last_entry.get("signature", "0" * 64)
                        except Exception:
                            last_sig = "0" * 64

        content_str = json.dumps({k: v for k, v in entry.items() if k != "signature"}, sort_keys=True)
        sig_base = f"{last_sig}{content_str}".encode()
        entry["signature"] = hashlib.sha256(sig_base).hexdigest()

        with open(BLACKBOARD_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        # Don't crash the server if logging fails, but print to stderr
        import sys
        print(f"Error logging to blackboard: {e}", file=sys.stderr)

# --- MCP SERVER INITIALIZATION ---

server = Server("hfo-hexagonal-hub")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available HFO tools across the 8 Ports."""
    return [
        types.Tool(
            name="think_octet",
            description="Execute the Generation 88 Thinking Octet (H-Phase). Anchors context to the blackboard and performs cross-port analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The mission query or problem to analyze."},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="query_journal",
            description="Query the HFO Mission Journal (DuckDB) for historical receipts and actor states.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "SQL query to execute against hfo_unified_v88.duckdb."},
                    "read_only": {"type": "boolean", "default": True}
                },
                "required": ["sql"],
            },
        ),
        types.Tool(
            name="p5_audit",
            description="Execute a Port 5 (DEFEND) Forensic Audit of the workspace and blackboard.",
            inputSchema={
                "type": "object",
                "properties": {
                    "repair": {"type": "boolean", "description": "Attempt to repair Chronos fractures if found.", "default": False},
                },
            },
        ),
        types.Tool(
            name="sequential_thinking",
            description="Advanced multi-step reasoning tool. Replaces the legacy Node.js sequential-thinking server.",
            inputSchema={
                "type": "object",
                "properties": {
                    "thought": {"type": "string", "description": "Current reasoning step."},
                    "thoughtNumber": {"type": "integer", "description": "Step index."},
                    "totalThoughts": {"type": "integer", "description": "Estimated total steps."},
                    "nextThoughtNeeded": {"type": "boolean", "description": "Whether more steps are required."},
                    "isRevision": {"type": "boolean", "description": "Is this a correction of previous logic?"}
                },
                "required": ["thought", "thoughtNumber", "totalThoughts", "nextThoughtNeeded"],
            },
        ),
        types.Tool(
            name="observe_search",
            description="P0 (OBSERVE) Wide-spectrum search via Tavily. Requires TAVILY_API_KEY.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search_survivors",
            description="P6 (STORE) Search for 'Logic Survivors' - elite code patterns that exist with high density or persist across renames.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 10},
                },
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution with integrated blackboard logging."""
    if not arguments:
        arguments = {}

    # Log tool attempt to blackboard (H-Phase start)
    log_to_blackboard({
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "phase": "I",
        "actor": "hexagonal_hub",
        "action": f"tool_call:{name}",
        "input": arguments
    })

    try:
        if name == "think_octet":
            query = arguments.get("query", "")
            # Execute legacy hub think to maintain parity
            cmd = [sys.executable, os.path.join(BASE_PATH, "hfo_hot_obsidian/bronze/2_areas/architecture/ports/hfo_orchestration_hub.py"), "think", query]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return [types.TextContent(type="text", text=result.stdout + result.stderr)]

        elif name == "query_journal":
            sql = arguments.get("sql", "")
            conn = duckdb.connect(DUCKDB_PATH)
            try:
                res = conn.execute(sql).fetchall()
                cols = [desc[0] for desc in conn.description]
                formatted = [dict(zip(cols, row)) for row in res]
                return [types.TextContent(type="text", text=json.dumps(formatted, indent=2, default=str))]
            finally:
                conn.close()

        elif name == "p5_audit":
            cmd = [sys.executable, os.path.join(BASE_PATH, "hfo_hot_obsidian/bronze/2_areas/architecture/ports/hfo_orchestration_hub.py"), "p5"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return [types.TextContent(type="text", text=result.stdout + result.stderr)]

        elif name == "sequential_thinking":
            # Simple relay of the thought process to the console/blackboard
            thought_data = {
                "thought": arguments.get("thought"),
                "step": f"{arguments.get('thoughtNumber')}/{arguments.get('totalThoughts')}",
                "is_revision": arguments.get("isRevision", False)
            }
            return [types.TextContent(type="text", text=f"Reasoning Step {thought_data['step']}: {thought_data['thought']}")]

        elif name == "observe_search":
            query = arguments.get("query", "")
            try:
                from tavily import TavilyClient
                api_key = os.environ.get("TAVILY_API_KEY")
                if not api_key:
                    return [types.TextContent(type="text", text="Error: TAVILY_API_KEY not found in environment.")]
                
                tavily = TavilyClient(api_key=api_key)
                response = tavily.search(query=query, search_depth="advanced")
                return [types.TextContent(type="text", text=json.dumps(response, indent=2))]
            except ImportError:
                return [types.TextContent(type="text", text="Error: tavily-python not installed.")]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Search failed: {e}")]

        elif name == "search_survivors":
            conn = duckdb.connect(DUCKDB_PATH)
            try:
                limit = arguments.get("limit", 10)
                density_query = f"""
                SELECT fs.path, fs.score, b.size, (fs.score * 1.0 / (b.size + 1)) * 1024 as density_index, fs.modified_at
                FROM file_system fs JOIN blobs b ON fs.hash = b.hash
                WHERE b.size > 100 AND b.size < 500000 ORDER BY density_index DESC LIMIT {limit};
                """
                immortality_query = f"""
                SELECT hash, count(*) as occurrences, list(path) as paths, max(modified_at) as last_seen
                FROM file_system GROUP BY hash HAVING occurrences > 1 ORDER BY occurrences DESC, last_seen DESC LIMIT {limit};
                """
                
                density_results = conn.execute(density_query).fetchall()
                immortality_results = conn.execute(immortality_query).fetchall()
                
                output = {
                    "top_density": [dict(zip(["path", "score", "size", "density", "modified"], r)) for r in density_results],
                    "immortals": [dict(zip(["hash", "occurrences", "paths", "last_seen"], r)) for r in immortality_results]
                }
                return [types.TextContent(type="text", text=json.dumps(output, indent=2, default=str))]
            except Exception as e:
                return [types.TextContent(type="text", text=f"Survivor search failed: {e}")]
            finally:
                conn.close()

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing {name}: {str(e)}")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hfo-hexagonal-hub",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
