"""
Unit test script for Tavily search tool.
"""
import asyncio
import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.tavily_tools import search_tavily_web
from tools.registry import execute_tool


async def main():
    print("Testing search_tavily_web directly...")
    result = await search_tavily_web(
        query="top computer science universities in Germany 2025",
        max_results=3
    )
    print("Direct search result status:", result.get("status"))
    print("Direct search result message/answer:", result.get("message") or result.get("answer"))

    print("\nTesting execute_tool('tavily_search')...")
    registry_result = await execute_tool(
        "tavily_search",
        {"query": "DAAD scholarships for Indian students 2025", "max_results": 3}
    )
    print("Registry execution status:", registry_result.get("observation", {}).get("status"))


if __name__ == "__main__":
    asyncio.run(main())
