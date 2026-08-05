"""Student application tracker model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    university_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("universities.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    program_name: Mapped[str | None] = mapped_column(String(300), nullable=True)
    intake: Mapped[str | None] = mapped_column(String(50), nullable=True)

    status: Mapped[str] = mapped_column(
        String(50),
        default="shortlisted",
        nullable=False,
        index=True,
    )
    # shortlisted | applied | under_review | accepted | rejected | deferred | withdrawn

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    documents_submitted: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    deadlines: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    # e.g. {"application": "2024-12-01", "scholarship": "2024-11-01"}

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="applications")
    university: Mapped["University"] = relationship("University", back_populates="applications")

    def __repr__(self) -> str:
        return f"<Application user={self.user_id} uni={self.university_id} status={self.status}>"
