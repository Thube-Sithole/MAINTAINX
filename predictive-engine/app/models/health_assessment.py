
import uuid

from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    JSON,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.base import Base


class HealthAssessment(Base):
    __tablename__ = "health_assessments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    equipment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("equipment.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    component_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("components.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    assessment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="rule_based",
    )

    overall_condition: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    finding_count: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    findings: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    recommendation: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    assessment_metadata: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    assessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
