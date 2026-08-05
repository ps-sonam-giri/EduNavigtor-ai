"""Student profile request/response schemas."""

import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_serializer


class ProfileCreateRequest(BaseModel):
    cgpa: Optional[float] = None
    cgpa_scale: Optional[float] = 10.0
    backlogs: Optional[int] = 0
    degree: Optional[str] = None
    specialization: Optional[str] = None
    graduation_year: Optional[int] = None
    university_name: Optional[str] = None
    ielts_score: Optional[float] = None
    toefl_score: Optional[int] = None
    pte_score: Optional[int] = None
    gre_score: Optional[int] = None
    gmat_score: Optional[int] = None
    preferred_countries: Optional[List[str]] = []
    course_interest: Optional[str] = None
    career_goal: Optional[str] = None
    target_intake: Optional[str] = None
    total_budget_usd: Optional[float] = None
    financial_background: Optional[str] = None
    work_experience_years: Optional[int] = 0
    work_description: Optional[str] = None

    model_config = {"extra": "ignore"}


class ProfileUpdateRequest(ProfileCreateRequest):
    pass


class ProfileResponse(BaseModel):
    id: Any
    user_id: Any
    cgpa: Optional[float] = None
    cgpa_scale: float = 10.0
    backlogs: int = 0
    degree: Optional[str] = None
    specialization: Optional[str] = None
    graduation_year: Optional[int] = None
    university_name: Optional[str] = None
    ielts_score: Optional[float] = None
    toefl_score: Optional[int] = None
    pte_score: Optional[int] = None
    gre_score: Optional[int] = None
    gmat_score: Optional[int] = None
    preferred_countries: List[str] = []
    course_interest: Optional[str] = None
    career_goal: Optional[str] = None
    target_intake: Optional[str] = None
    total_budget_usd: Optional[float] = None
    financial_background: Optional[str] = None
    work_experience_years: int = 0
    work_description: Optional[str] = None
    documents: Dict[str, Any] = {}
    extracted_data: Dict[str, Any] = {}

    # Serialize UUID fields to string automatically
    @field_serializer('id', 'user_id')
    def serialize_uuid(self, v: Any) -> str:
        return str(v)

    model_config = {"from_attributes": True}
