from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT_FOLDER = Path(__file__).parent.absolute()
MCP_FOLDER = ROOT_FOLDER / "binance_mcp"

server_params = StdioServerParameters(
    command="python",  # Executable
    args=[str(MCP_FOLDER / "binance_mcp.py")],
    env=None,
)


async def run():
    # open connection to mcp and create client:
    # to allow send and return messages 
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:
            
            # open session
            await session.initialize()

            # display tools:
            # tools = await session.list_tools()
            # print("Available tools:", tools)
    
            result = await session.call_tool(
                "get_price", arguments={"symbol": "BTCUSDT"}
            )
            print(result)

            # result = await session.call_tool(
            #     "get_price_price_change", arguments={"symbol": "BTCUSDT"}
            # )
            # print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())