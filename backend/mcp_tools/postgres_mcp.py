"""
PostgreSQL MCP Client
Allows AI agents to query the database using natural language
via the PostgreSQL MCP server.
"""

from typing import Any, Dict, List, Optional

import structlog

from app.config import settings

logger = structlog.get_logger(__name__)


class PostgresMCPClient:
    """
    PostgreSQL MCP integration.
    Translates natural language queries to SQL via the MCP server,
    or executes direct parameterised queries.
    """

    def __init__(self):
        self.mcp_server_url = f"http://localhost:{settings.mcp_postgres_server_port}"

    async def natural_language_query(self, question: str) -> List[Dict[str, Any]]:
        """
        Submit a natural language question to the PostgreSQL MCP server.
        The MCP server translates it to SQL and returns results.
        """
        try:
            import httpx

            payload = {
                "tool": "query",
                "arguments": {
                    "question": question,
                    "database_url": settings.database_sync_url,
                },
            }

            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.mcp_server_url}/tools/call",
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("result", [])

        except Exception as e:
            logger.warning("PostgreSQL MCP unavailable, using direct query", error=str(e))
            return await self._direct_query_fallback(question)

    async def get_universities_for_profile(
        self,
        cgpa: float,
        ielts: float,
        budget_usd: float,
        countries: List[str],
        course: str,
    ) -> List[Dict[str, Any]]:
        """Parameterised query for university matching."""
        from sqlalchemy import select, text
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from app.models.university import University
        from app.models.country import Country

        try:
            engine = create_async_engine(settings.database_url, echo=False)
            AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

            async with AsyncSession() as session:
                q = (
                    select(University, Country.name.label("country_name"))
                    .join(Country, University.country_id == Country.id)
                    .where(University.is_active == True)
                    .where(
                        (University.min_cgpa == None) | (University.min_cgpa <= cgpa)
                    )
                    .where(
                        (University.min_ielts == None) | (University.min_ielts <= ielts)
                    )
                    .where(
                        (University.avg_tuition_usd_per_year == None)
                        | (University.avg_tuition_usd_per_year <= budget_usd)
                    )
                )

                if countries:
                    q = q.where(Country.name.in_(countries))

                q = q.order_by(University.qs_world_rank.asc().nullslast()).limit(20)
                result = await session.execute(q)
                rows = result.all()
                await engine.dispose()

                return [
                    {
                        "id": str(uni.id),
                        "name": uni.name,
                        "country": country_name,
                        "qs_world_rank": uni.qs_world_rank,
                        "acceptance_rate": uni.acceptance_rate,
                        "avg_tuition_usd_per_year": float(uni.avg_tuition_usd_per_year or 0),
                        "programs": uni.programs,
                        "has_scholarships": uni.has_scholarships,
                    }
                    for uni, country_name in rows
                ]
        except Exception as e:
            logger.error("Direct DB query failed", error=str(e))
            return []

    async def get_scholarships_for_profile(
        self,
        cgpa: float,
        ielts: float,
        nationality: str = "India",
    ) -> List[Dict[str, Any]]:
        """Query scholarships matching student eligibility."""
        from sqlalchemy import select, or_
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from app.models.scholarship import Scholarship

        try:
            engine = create_async_engine(settings.database_url, echo=False)
            AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

            async with AsyncSession() as session:
                result = await session.execute(
                    select(Scholarship)
                    .where(Scholarship.is_active == True)
                    .where(
                        (Scholarship.min_cgpa == None) | (Scholarship.min_cgpa <= cgpa)
                    )
                    .where(
                        (Scholarship.min_ielts == None) | (Scholarship.min_ielts <= ielts)
                    )
                    .limit(15)
                )
                scholarships = result.scalars().all()
                await engine.dispose()

                # Filter by nationality eligibility
                return [
                    {
                        "id": str(s.id),
                        "name": s.name,
                        "provider": s.provider,
                        "amount_usd": float(s.amount_usd or 0),
                        "amount_description": s.amount_description,
                        "eligible_countries": s.eligible_countries,
                        "min_cgpa": s.min_cgpa,
                        "description": s.description,
                        "application_url": s.application_url,
                    }
                    for s in scholarships
                    if not s.eligible_countries
                    or "All" in s.eligible_countries
                    or nationality in s.eligible_countries
                ]
        except Exception as e:
            logger.error("Scholarship query failed", error=str(e))
            return []

    async def _direct_query_fallback(self, question: str) -> List[Dict[str, Any]]:
        """Use LLM to generate SQL from natural language and execute it."""
        try:
            from agents.llm import ainvoke_llm, extract_json_from_response

            schema_hint = """
            Tables: universities(id, name, country_id, qs_world_rank, min_cgpa, min_ielts, avg_tuition_usd_per_year, programs)
                    countries(id, name, code, avg_tuition_usd_per_year)
                    scholarships(id, name, provider, amount_usd, min_cgpa, eligible_countries)
            """

            prompt = f"""Convert this question to a PostgreSQL SELECT query.
Question: {question}
Schema: {schema_hint}
Return ONLY the SQL query, nothing else. Keep it simple and safe (SELECT only, LIMIT 20)."""

            sql, _ = await ainvoke_llm(prompt, fast=True)
            sql = sql.strip().strip("```sql").strip("```").strip()

            if not sql.upper().startswith("SELECT"):
                return []

            from sqlalchemy import text
            from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

            engine = create_async_engine(settings.database_url, echo=False)
            AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

            async with AsyncSession() as session:
                result = await session.execute(text(sql))
                cols = list(result.keys())
                rows = [dict(zip(cols, row)) for row in result.fetchall()]
                await engine.dispose()
                return rows

        except Exception as e:
            logger.error("NL query fallback failed", error=str(e))
            return []
