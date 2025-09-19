import asyncio
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

ROOT_FOLDER = Path(__file__).parent.absolute()
MCP_PATH = "C:/Users/guanj/OneDrive/Desktop/MCPLab/mcp-course/binance_mcp/binance_mcp.py"
# str(ROOT_FOLDER / "binance_mcp" / "binance_mcp.py")

print(MCP_PATH)

mcp_config = {
    "binance": {
        "command": "python",
        "args": [MCP_PATH],
        "transport": "stdio",
    }
    # # npx NCP exmaple
    # ,"shopify": {
    #     "command": "npx",
    #     "args": ["-y", "@shopify/dev-mcp@latest"],
    #     "transport": "stdio",
    # },
}

async def get_crypto_prices():
    client = MultiServerMCPClient(mcp_config)
    async with client.session("binance") as session:
        tools = await client.get_tools()

        agent = create_react_agent(model, tools)

        query = "What are the current prices of Bitcoin and Ethereum?"
        message = HumanMessage(content=query)

        response = await agent.ainvoke({"messages": [message]})

        answer = response["messages"][-1].content

        return answer
    # test
    # message = HumanMessage(content="What is 2+2?")

    # response = await model.ainvoke([message])

    # return response.content

if __name__ == "__main__":
    # Run the main async function
    response = asyncio.run(get_crypto_prices())
    print(response)