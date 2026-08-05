"""Country reference data model."""

import uuid

from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)

    # Key facts for recommendations
    avg_tuition_usd_per_year: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_living_cost_usd_per_month: Mapped[float | None] = mapped_column(Float, nullable=True)
    visa_fee_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    health_insurance_usd_per_year: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Work rights
    post_study_work_years: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    part_time_hours_per_week: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # QS ranking presence
    top_ranked_universities_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Language
    language: Mapped[str] = mapped_column(String(50), default="English", nullable=False)
    ielts_min_required: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Overview
    overview: Mapped[str | None] = mapped_column(Text, nullable=True)
    pros: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    cons: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    popular_courses: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    universities: Mapped[list["University"]] = relationship(
        "University", back_populates="country"
    )

    def __repr__(self) -> str:
        return f"<Country {self.name} ({self.code})>"
