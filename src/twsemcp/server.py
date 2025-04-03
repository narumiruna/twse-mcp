from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from twsemcp.twse import StockInfoRequest

# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
server = FastMCP("TWSE MCP Server", log_level="ERROR")


@server.tool()
async def get_stock_info(
    symbols: Annotated[list[str], Field(description="List of stock symbols to query, e.g., ['2330', '2317']")],
    full_info: Annotated[bool, Field(description="Whether to return full information or not.")] = True,
) -> str:
    """Get stock information from TWSE."""
    try:
        result = await StockInfoRequest(symbols=symbols).do()
        if full_info:
            return result.model_dump_json()
        else:
            return result.pretty_repr()
    except Exception as e:
        return f"Error occurred while querying stock information: {str(e)}"


def main() -> None:
    server.run()
