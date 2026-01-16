# Medallion: Bronze | Mutation: 0% | HIVE: I
import asyncio
from mcp.server import Server
from mcp.server.models import Tool
import mcp.types as types

# Initialize MCP Server (System 1 - Senses)
app = Server("hfo-sense-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="sense_file",
            description="Read a file from the HFO workspace",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                },
                "required": ["path"],
            },
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "sense_file":
        path = arguments.get("path")
        try:
            with open(path, "r") as f:
                content = f.read()
            return [types.TextContent(type="text", text=content)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error reading file: {str(e)}")]
    raise ValueError(f"Tool {name} not found")

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    asyncio.run(main())
