"""Student academic and personal profile model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # Academic
    cgpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    cgpa_scale: Mapped[float] = mapped_column(Float, default=10.0, nullable=False)
    backlogs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    degree: Mapped[str | None] = mapped_column(String(100), nullable=True)
    specialization: Mapped[str | None] = mapped_column(String(200), nullable=True)
    graduation_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    university_name: Mapped[str | None] = mapped_column(String(300), nullable=True)

    # English Proficiency
    ielts_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    toefl_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pte_score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Standardised Tests
    gre_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gmat_score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Preferences
    preferred_countries: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    course_interest: Mapped[str | None] = mapped_column(String(200), nullable=True)
    career_goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_intake: Mapped[str | None] = mapped_column(String(50), nullable=True)  # e.g. "Fall 2025"

    # Finance
    total_budget_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    financial_background: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # Options: self_funded, education_loan, partial_scholarship, full_scholarship

    # Work Experience
    work_experience_years: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    work_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Uploaded Documents (file paths)
    documents: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    # e.g. {"resume": "uploads/...", "marksheet": "uploads/...", "ielts": "uploads/..."}

    # Extracted / parsed data from documents
    extracted_data: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="profile")

    def __repr__(self) -> str:
        return f"<StudentProfile user_id={self.user_id} cgpa={self.cgpa}>"
