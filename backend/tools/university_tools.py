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
    Search universities matching country, budget, and academic criteria.
    Returns verified database records with tuition, ranking, and requirements.
    """
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with async_session() as session:
            stmt = select(University).join(Country, University.country_id == Country.id)

            filters = []
            if country:
                filters.append(Country.name.ilike(f"%{country}%"))
            if max_tuition_usd:
                filters.append(University.avg_tuition_usd_per_year <= max_tuition_usd)
            if min_cgpa:
                filters.append(or_(University.min_cgpa == None, University.min_cgpa <= min_cgpa))

            if filters:
                stmt = stmt.where(*filters)

            stmt = stmt.order_by(University.qs_world_rank.asc().nullslast()).limit(min(limit, 10))

            result = await session.execute(stmt)
            rows = result.scalars().all()
            await engine.dispose()

            return [
                {
                    "name": u.name,
                    "country": u.country.name if u.country else "N/A",
                    "city": u.city or "N/A",
                    "qs_world_rank": u.qs_world_rank,
                    "avg_tuition_usd_per_year": float(u.avg_tuition_usd_per_year or 0),
                    "avg_living_cost_usd_per_month": float(u.avg_living_cost_usd_per_month or 0),
                    "min_cgpa": float(u.min_cgpa or 0),
                    "min_ielts": float(u.min_ielts or 0),
                    "backlog_policy": u.backlog_policy or "Standard evaluation",
                    "programs": u.programs or [],
                    "website": u.website or "",
                    "source": "EduPilot Verified Database",
                }
                for u in rows
            ]
    except Exception as e:
        return [{"error": f"University search failed: {str(e)}"}]
