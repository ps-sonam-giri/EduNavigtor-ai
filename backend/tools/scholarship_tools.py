"""
Scholarship Matching Tool.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings
from app.models.scholarship import Scholarship


class ScholarshipSearchInput(BaseModel):
    country: Optional[str] = Field(None, description="Target country or 'All'")
    cgpa: Optional[float] = Field(None, description="Student's CGPA score out of 10")
    nationality: str = Field("India", description="Student's nationality")
    limit: int = Field(5, description="Maximum scholarships to return")


async def search_scholarships_tool(
    country: Optional[str] = None,
    cgpa: Optional[float] = None,
    nationality: str = "India",
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search scholarships matching student eligibility and country via Tavily Live Web Search.
    """
    from tools.tavily_tools import search_tavily_web

    target_country = country or "Germany"
    query = f"scholarships for {nationality} students in {target_country} 2025 2026 eligibility application deadline"
    res = await search_tavily_web(query=query, max_results=min(limit, 10))

    if res.get("status") == "success":
        results = []
        for r in res.get("results", []):
            results.append({
                "name": r.get("title", "Scholarship Result"),
                "country": target_country,
                "content_snippet": r.get("content", "")[:300],
                "url": r.get("url"),
                "source": "Tavily Live Web Engine",
            })
        return results

    return [{"error": "Tavily scholarship search failed"}]
