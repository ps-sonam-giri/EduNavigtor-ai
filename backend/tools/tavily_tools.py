"""
Tavily Live Web Search Engine Tool.
Provides real-time web search capabilities for university rankings, tuition fees, application deadlines, and scholarships.
"""

import os
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field

from app.config import settings


class TavilySearchInput(BaseModel):
    query: str = Field(..., description="Web search query, e.g. 'top computer science universities in Germany tuition 2025'")
    search_depth: str = Field("advanced", description="Search depth: 'basic' or 'advanced'")
    max_results: int = Field(5, description="Maximum search results to return (1-10)")


async def search_tavily_web(
    query: str,
    search_depth: str = "advanced",
    max_results: int = 5,
    include_domains: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Perform a live web search via Tavily API.
    Returns direct answers, webpage titles, URLs, and relevant context snippets.
    """
    api_key = settings.tavily_api_key or os.environ.get("TAVILY_API_KEY", "").strip()

    if not api_key:
        return {
            "status": "disabled",
            "message": "TAVILY_API_KEY not configured in environment.",
            "query": query,
            "answer": None,
            "results": [],
        }

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": search_depth,
        "include_answer": True,
        "max_results": min(max(max_results, 1), 10),
    }

    if include_domains:
        payload["include_domains"] = include_domains

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                results = [
                    {
                        "title": item.get("title", "No Title"),
                        "url": item.get("url", ""),
                        "content": item.get("content", ""),
                        "score": item.get("score", 0.0),
                    }
                    for item in data.get("results", [])
                ]
                return {
                    "status": "success",
                    "query": query,
                    "answer": data.get("answer"),
                    "results": results,
                    "source": "Tavily Live Web Search",
                }
            else:
                return {
                    "status": "error",
                    "message": f"Tavily API returned HTTP {resp.status_code}: {resp.text}",
                    "query": query,
                    "answer": None,
                    "results": [],
                }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Tavily search request failed: {str(e)}",
            "query": query,
            "answer": None,
            "results": [],
        }
