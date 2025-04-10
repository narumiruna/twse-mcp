import pytest
from mcp import ClientSession
from mcp import StdioServerParameters
from mcp import stdio_client
from mcp.types import TextContent
from twse.stock_info import StockInfoResponse


@pytest.fixture
def server_params() -> StdioServerParameters:
    return StdioServerParameters(command="twsemcp")


@pytest.mark.asyncio
async def test_get_stock_info(server_params: StdioServerParameters) -> None:
    async with stdio_client(server_params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        assert len(tools.tools) > 0
        assert tools.tools[0].name == "get_stock_info"

        symbols = ["2330"]
        result = await session.call_tool("get_stock_info", {"symbols": symbols, "full_info": True})

        json_data = "\n".join([t.text for t in result.content if isinstance(t, TextContent)])
        data = StockInfoResponse.model_validate_json(json_data, by_name=True)
        assert data.msg_array[0].symbol == symbols[0]
