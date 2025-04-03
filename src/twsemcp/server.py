from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from .twse import query_stock_info

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
server = FastMCP("MCP Server TWSE", log_level="ERROR")


@server.tool()
async def query_stock_info_from_twse(
    symbol: Annotated[str, Field(description="The Taiwan stock symbol to query. e.q. 2330")],
) -> str:
    """Query stock information from TWSE."""
    try:
        result = query_stock_info(symbol)
        return result.pretty_repr()
    except Exception as e:
        return f"Error occurred while querying stock information: {str(e)}"


def main() -> None:
    server.run()
