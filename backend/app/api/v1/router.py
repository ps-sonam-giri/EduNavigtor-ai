"""Main API v1 router."""

from fastapi import APIRouter

from app.api.v1 import auth, profile, agents, universities, reports

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(agents.router)
api_router.include_router(universities.router)
api_router.include_router(reports.router)
