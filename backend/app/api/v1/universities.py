"""
University & scholarship query endpoints – no authentication required.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.country import Country
from app.models.scholarship import Scholarship
from app.models.university import University

router = APIRouter(prefix="/universities", tags=["Universities & Scholarships"])


@router.get("")
async def list_universities(
    country: Optional[str] = Query(None),
    max_tuition: Optional[float] = Query(None),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(University)
        .options(selectinload(University.country))
        .where(University.is_active == True)
    )
    if country:
        query = query.join(Country).where(Country.name.ilike(f"%{country}%"))
    if max_tuition:
        query = query.where(University.avg_tuition_usd_per_year <= max_tuition)

    query = query.order_by(University.qs_world_rank.asc().nullslast()).limit(limit)
    result = await db.execute(query)
    unis = result.scalars().all()

    return [
        {
            "id": str(u.id),
            "name": u.name,
            "short_name": u.short_name,
            "country": u.country.name if u.country else None,
            "location_city": u.location_city,
            "qs_world_rank": u.qs_world_rank,
            "acceptance_rate": u.acceptance_rate,
            "avg_tuition_usd_per_year": u.avg_tuition_usd_per_year,
            "min_cgpa": u.min_cgpa,
            "min_ielts": u.min_ielts,
            "programs": u.programs,
            "intake_months": u.intake_months,
            "has_scholarships": u.has_scholarships,
            "graduate_employment_rate": u.graduate_employment_rate,
        }
        for u in unis
    ]


@router.get("/scholarships/list")
async def list_scholarships(
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Scholarship).where(Scholarship.is_active == True).limit(limit)
    )
    scholarships = result.scalars().all()
    return [
        {
            "id": str(s.id),
            "name": s.name,
            "provider": s.provider,
            "scholarship_type": s.scholarship_type,
            "amount_usd": s.amount_usd,
            "amount_description": s.amount_description,
            "eligible_countries": s.eligible_countries,
            "min_cgpa": s.min_cgpa,
            "description": s.description,
            "application_url": s.application_url,
        }
        for s in scholarships
    ]


@router.get("/countries/list")
async def list_countries(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Country).where(Country.is_active == True).order_by(Country.name)
    )
    countries = result.scalars().all()
    return [
        {
            "id": str(c.id),
            "name": c.name,
            "code": c.code,
            "avg_tuition_usd_per_year": c.avg_tuition_usd_per_year,
            "avg_living_cost_usd_per_month": c.avg_living_cost_usd_per_month,
            "post_study_work_years": c.post_study_work_years,
            "overview": c.overview,
            "pros": c.pros,
            "cons": c.cons,
            "popular_courses": c.popular_courses,
        }
        for c in countries
    ]


@router.get("/{university_id}")
async def get_university(university_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(University)
        .options(selectinload(University.country), selectinload(University.scholarships))
        .where(University.id == university_id)
    )
    uni = result.scalar_one_or_none()
    if not uni:
        raise HTTPException(status_code=404, detail="University not found")

    return {
        "id": str(uni.id),
        "name": uni.name,
        "website": uni.website,
        "location_city": uni.location_city,
        "country": uni.country.name if uni.country else None,
        "qs_world_rank": uni.qs_world_rank,
        "acceptance_rate": uni.acceptance_rate,
        "min_cgpa": uni.min_cgpa,
        "min_ielts": uni.min_ielts,
        "min_gre": uni.min_gre,
        "avg_tuition_usd_per_year": uni.avg_tuition_usd_per_year,
        "avg_living_cost_usd_per_month": uni.avg_living_cost_usd_per_month,
        "application_fee_usd": uni.application_fee_usd,
        "programs": uni.programs,
        "intake_months": uni.intake_months,
        "overview": uni.overview,
        "strengths": uni.strengths,
        "graduate_employment_rate": uni.graduate_employment_rate,
        "avg_starting_salary_usd": uni.avg_starting_salary_usd,
        "has_scholarships": uni.has_scholarships,
        "scholarships": [
            {"id": str(s.id), "name": s.name, "amount_description": s.amount_description}
            for s in uni.scholarships
        ],
    }
