# math_server.py
from mcp.server.fastmcp import FastMCP
from langchain_tavily import TavilySearch

mcp = FastMCP("Search Server")
search = TavilySearch(max_results=5)

@mcp.tool()
async def search_tool(query: str) -> str:
    """
    A simple search tool that returns the query as a response.
    In a real-world scenario, this would interface with a search engine.
    """
    search_results = await search.ainvoke(query)
    return str(search_results)


if __name__ == "__main__":
    mcp.run(transport="stdio")