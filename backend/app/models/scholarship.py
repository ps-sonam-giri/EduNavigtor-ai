"""Scholarship model."""

import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Scholarship(Base):
    __tablename__ = "scholarships"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    university_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("universities.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(200), nullable=False)
    # e.g. "Government of Australia", "University of Melbourne", "DAAD"

    scholarship_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # full_tuition | partial_tuition | living_stipend | merit | need_based | country_specific

    amount_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    amount_description: Mapped[str | None] = mapped_column(String(300), nullable=True)
    # e.g. "Full tuition + $15,000/year living allowance"

    # Eligibility
    eligible_countries: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    # ["India", "All"] – list of nationalities eligible
    eligible_courses: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    min_cgpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    min_ielts: Mapped[float | None] = mapped_column(Float, nullable=True)
    requires_work_experience: Mapped[bool] = mapped_column(Boolean, default=False)
    min_work_experience_years: Mapped[int] = mapped_column(Integer, default=0)

    # Application
    application_deadline: Mapped[str | None] = mapped_column(String(100), nullable=True)
    application_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    eligibility_criteria: Mapped[str | None] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationship
    university: Mapped["University | None"] = relationship(
        "University", back_populates="scholarships"
    )

    def __repr__(self) -> str:
        return f"<Scholarship {self.name} by {self.provider}>"
