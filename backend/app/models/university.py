"""University model."""

import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class University(Base):
    __tablename__ = "universities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    country_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("countries.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    short_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    location_city: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Rankings
    qs_world_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    qs_subject_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    times_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Admissions
    acceptance_rate: Mapped[float | None] = mapped_column(Float, nullable=True)  # 0-100
    min_cgpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    min_ielts: Mapped[float | None] = mapped_column(Float, nullable=True)
    min_toefl: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_gre: Mapped[int | None] = mapped_column(Integer, nullable=True)
    requires_gmat: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Finances
    avg_tuition_usd_per_year: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_living_cost_usd_per_month: Mapped[float | None] = mapped_column(Float, nullable=True)
    application_fee_usd: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Programs offered
    programs: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    # e.g. [{"name": "MS Computer Science", "duration_years": 2, "tuition_usd": 35000}]

    # Intake windows
    intake_months: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    # e.g. ["September", "January"]

    # Scholarship availability
    has_scholarships: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Overview
    overview: Mapped[str | None] = mapped_column(Text, nullable=True)
    strengths: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    notable_alumni: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)

    # Employability
    graduate_employment_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_starting_salary_usd: Mapped[float | None] = mapped_column(Float, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    country: Mapped["Country"] = relationship("Country", back_populates="universities")
    scholarships: Mapped[list["Scholarship"]] = relationship(
        "Scholarship", back_populates="university"
    )
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="university"
    )

    def __repr__(self) -> str:
        return f"<University {self.name}>"
