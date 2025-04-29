from typing import Annotated

import twse
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
server = FastMCP("TWSE MCP Server", log_level="ERROR")


@server.tool()
async def get_stock_info(
    symbol: Annotated[
        str, Field(description="Stock symbols to query, can be a single symbol or a comma-separated list")
    ],
) -> str:
    """Get stock information from Taiwan Stock Exchange(TWSE)."""
    try:
        result = await twse.stock_info.async_get_stock_info(symbol.split(","))
        return result.model_dump_json()
    except Exception as e:
        return f"Error occurred while querying stock information: {str(e)}"


def main() -> None:
    server.run()
