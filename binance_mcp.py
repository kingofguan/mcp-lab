from mcp.server.fastmcp import FastMCP
import requests
from typing import Any
import datetime
from pathlib import Path

mcp = FastMCP("Binance MCP", port=8897)


THIS_FOLDER = Path(__file__).parent.absolute()
ACTIVITY_LOG_FILE = THIS_FOLDER / "activity.log"


def get_symbol_from_name(name: str) -> str:
    if name.lower() in ["bitcoin", "btc"]:
        return "BTCUSDT"
    elif name.lower() in ["ethereum", "eth"]:
        return "ETHUSDT"
    else:
        return name.upper()
    
# s = requests.Session()
# retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
# s.mount("https://", HTTPAdapter(max_retries=retries))
# r = s.get("https://api.binance.us/api/v3/ticker/price", params={"symbol":"BTCUSDT"}, timeout=5)


@mcp.tool()
def get_price(symbol: str) -> any:
    """
    GEt price of a crypto asset from Binance
    
    Args:
        symbol (str): The symbol of the crypto asset to get the price of
    Returns:
        Any: The current price of the crypto asset
    """
    symbol = get_symbol_from_name(symbol)
    # binance api in U.S.
    url = f"https://api.binance.us/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    # response.raise_for_status()

    if response.status_code != 200:
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(
                f"Error getting price change for {symbol}: {response.status_code} {response.text}\n"
            )
        raise Exception(
            f"Error getting price change for {symbol}: {response.status_code} {response.text}"
        )
    else:
        price = response.json()["price"]
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(
                f"Successfully got price change for {symbol}. Current price is {price}. Current time is {datetime.datetime.now(datetime.UTC)}\n"
            )

    return f"The current price of {symbol} is {price}"
    # return response.json()


@mcp.resource("file://activity.log")
def activity_log() -> str:
    with open(ACTIVITY_LOG_FILE, "r") as f:
        # just return the content of the file
        return f.read()
    
@mcp.resource("resource://crypto_price/{symbol}")
def get_crypto_price(symbol: str) -> str:
    # expose get price tool as a resource
    return get_price(symbol)

@mcp.resource("file://symbol_map.csv")
def get_symbol_map() -> str:
    with open(THIS_FOLDER / "symbol_map.csv", "r") as f:
        return f.read()

@mcp.tool() 
def get_price_price_change(symbol: str) -> Any:
    """
    Get the price change of the last 24 hours of a crypto asset from Binance

    Args:
        symbol (str): The symbol of the crypto asset to get the price change of

    Returns:
        Any: The price change of the crypto asset in the last 24 hours
    """
    symbol = get_symbol_from_name(symbol)
    url = f"https://data-api.binance.vision/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# add prompts
@mcp.prompt()
def executive_summary() -> str:
    """Returns an executive summary of Bitcoin and Ethereum"""
    return """
    Get the prices of the following crypto asset: btc, eth
    
    Provide me with an executive summary including the 
    two-sentence summary of the crypto asset, the current price, 
    the price change in the last 24 hours, and the percentage change
    in the last 24 hours.

    When using the get_price and get_price_price_change tools,
    use the symbol as the argument.
    
    Symbols: For bitcoin/btc, the symbol is "BTCUSDT".
    Symbols: For ethereum/eth, the symbol is "ETHUSDT".
    """


@mcp.prompt()
def crypto_summary(crypto: str) -> str:
    """Returns a summary of a crypto asset"""

    return f"""
    Get the current price of the following crypto asset:
    {crypto}
    and also provide a summary of the price changes in the last 24 hours.

    When using the get_price and get_price_price_change tools, use the symbol as the argument.
    Symbols: For bitcoin/btc, the symbol is "BTCUSDT".
    Symbols: For ethereum/eth, the symbol is "ETHUSDT".
    """
# activate uv environment:
# .venv\Scripts\activate  

# start inspector:
# "C:/Users/guanj/OneDrive/Desktop/MCPLab/mcp-course/.venv/Scripts/python.exe"
# "C:/Users/guanj/OneDrive/Desktop/MCPLab/mcp-course/binance_mcp/binance_mcp.py"
# npx @modelcontextprotocol/inspector@0.16.2 

# transport type:
# stdio: for local testing stdin stdout
# sse: deprecated
# streamable mcp = use that

# cli and work with resource: 
# mcp dev binance_mcp/binance_mcp.py

if __name__ == "__main__":
    # if not Path(ACTIVITY_LOG_FILE).exists():
    #     Path(ACTIVITY_LOG_FILE).touch()
    # print("Starting Binance MCP")
    # mcp.run(transport="stdio")

    # locally try
    # mcp.run(transport='streamable-http')


    mcp.run(transport='sse')

    # connect to http://localhost:8897/mcp in mcp inspector
    # launch insepctor with npx @modelcontextprotocol/inspector