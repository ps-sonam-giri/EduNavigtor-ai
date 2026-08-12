"""
University Database Search Tool.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.config import settings
from app.models.university import University
from app.models.country import Country


class UniversitySearchInput(BaseModel):
    country: Optional[str] = Field(None, description="Target country name, e.g., 'Germany', 'USA', 'UK', 'Canada'")
    max_tuition_usd: Optional[float] = Field(None, description="Maximum tuition budget in USD per year")
    min_cgpa: Optional[float] = Field(None, description="Student's CGPA out of 10.0 scale")
    course_interest: Optional[str] = Field(None, description="Field of study or program interest, e.g., 'Computer Science'")
    limit: int = Field(5, description="Number of results to return (max 10)")


async def search_universities_tool(
    country: Optional[str] = None,
    max_tuition_usd: Optional[float] = None,
    min_cgpa: Optional[float] = None,
    course_interest: Optional[str] = None,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search universities matching country, budget, and academic criteria via Tavily Live Web Search.
    """
    from tools.tavily_tools import search_tavily_web

    target_country = country or "Germany"
    query = f"top universities for {course_interest or 'Computer Science'} in {target_country} QS rank tuition fees 2025 2026"
    if max_tuition_usd:
        query += f" tuition under {max_tuition_usd} USD"

    res = await search_tavily_web(query=query, max_results=min(limit, 10))

    if res.get("status") == "success":
        results = []
        for r in res.get("results", []):
            results.append({
                "name": r.get("title", "University Result"),
                "country": target_country,
                "content_snippet": r.get("content", "")[:300],
                "url": r.get("url"),
                "source": "Tavily Live Web Engine",
            })
        return results

    return [{"error": "Tavily live search failed"}]
