import anyio
import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import Server

from .twse import query_stock_info

app = Server("MCP Server TWSE")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="query_stock_info",
            description="Query stock information from TWSE",
            inputSchema={
                "type": "object",
                "required": ["symbol"],
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The Taiwan stock symbol to query. e.q. 2330",
                    }
                },
            },
        )
    ]


@app.call_tool()
async def query_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name != "query_stock_info":
        raise ValueError(f"Unknown tool: {name}")
    if "symbol" not in arguments:
        raise ValueError("Missing required argument 'symbol'")

    result = query_stock_info(arguments["symbol"]).pretty_repr()
    return [types.TextContent(type="text", text=result)]


async def run() -> None:
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def main() -> None:
    anyio.run(run)
