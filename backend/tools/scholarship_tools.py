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
    Search scholarships matching student eligibility, country, and academic standing.
    """
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    try:
        async with async_session() as session:
            stmt = select(Scholarship)
            filters = []
            if cgpa:
                filters.append(or_(Scholarship.min_cgpa == None, Scholarship.min_cgpa <= cgpa))

            if filters:
                stmt = stmt.where(*filters)

            stmt = stmt.limit(min(limit, 10))

            result = await session.execute(stmt)
            rows = result.scalars().all()
            await engine.dispose()

            matches = []
            for s in rows:
                # Filter eligibility by country/nationality
                eligible_countries = s.eligible_countries or []
                if (
                    not eligible_countries
                    or "All" in eligible_countries
                    or (country and any(country.lower() in c.lower() for c in eligible_countries))
                    or nationality in eligible_countries
                ):
                    matches.append({
                        "name": s.name,
                        "provider": s.provider or "N/A",
                        "amount_usd": float(s.amount_usd or 0),
                        "amount_description": s.amount_description or "Varies",
                        "min_cgpa": float(s.min_cgpa or 0),
                        "eligible_countries": s.eligible_countries or ["All"],
                        "scholarship_basis": s.scholarship_basis or "Merit-based",
                        "application_url": s.application_url or "",
                        "description": s.description or "",
                        "source": "EduPilot Verified Database",
                    })

            return matches[:limit]
    except Exception as e:
        return [{"error": f"Scholarship search failed: {str(e)}"}]
