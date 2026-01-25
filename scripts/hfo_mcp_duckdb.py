# Medallion: Bronze | Mutation: 0% | HIVE: I
import asyncio
import duckdb
import json
import os
from mcp.server.models import InitializationOptions
from mcp.server import Notification, Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# Database path
DB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"

server = Server("hfo-duckdb-mcp")


def _ensure_db_initialized() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = duckdb.connect(database=DB_PATH)
    try:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS actor_states (
                actor_id VARCHAR PRIMARY KEY,
                mission_thread VARCHAR,
                state_json JSON,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                version INTEGER DEFAULT 1
            );
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS mission_journal (
                event_id UUID DEFAULT gen_random_uuid(),
                actor_id VARCHAR,
                event_type VARCHAR,
                payload JSON,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
    finally:
        con.close()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="query_journal",
            description="Query the HFO mission journal for events.",
            inputSchema={
                "type": "object",
                "properties": {
                    "actor_id": {"type": "string", "description": "Optional actor ID filter"},
                    "limit": {"type": "integer", "description": "Number of records to return", "default": 10},
                    "event_type": {"type": "string", "description": "Optional event type filter"}
                }
            }
        ),
        types.Tool(
            name="get_actor_state",
            description="Retrieve the persistent state of a specific actor.",
            inputSchema={
                "type": "object",
                "properties": {
                    "actor_id": {"type": "string", "description": "The ID of the actor"}
                },
                "required": ["actor_id"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    _ensure_db_initialized()
    if name == "query_journal":
        actor_id = arguments.get("actor_id")
        limit = arguments.get("limit", 10)
        event_type = arguments.get("event_type")

        query = "SELECT * FROM mission_journal"
        params = []
        conditions = []

        if actor_id:
            conditions.append("actor_id = ?")
            params.append(actor_id)
        if event_type:
            conditions.append("event_type = ?")
            params.append(event_type)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        try:
            con = duckdb.connect(database=DB_PATH)
            df = con.execute(query, params).fetch_df()
            con.close()
            return [types.TextContent(type="text", text=df.to_json(orient="records", indent=2))]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error querying journal: {str(e)}")]

    elif name == "get_actor_state":
        actor_id = arguments.get("actor_id")
        try:
            con = duckdb.connect(database=DB_PATH)
            result = con.execute("SELECT state_json FROM actor_states WHERE actor_id = ?", (actor_id,)).fetchone()
            con.close()
            if result:
                return [types.TextContent(type="text", text=result[0])]
            else:
                return [types.TextContent(type="text", text=f"Actor {actor_id} not found.")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error retrieving actor state: {str(e)}")]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hfo-duckdb-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=Notification(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
