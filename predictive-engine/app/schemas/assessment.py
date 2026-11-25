
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AssessmentFindingResponse(BaseModel):
    """Individual finding identified by the condition engine."""

    sensor: str
    severity: str
    value: float
    unit: str
    message: str


class AssessmentResponse(BaseModel):
    """Structured equipment-condition assessment response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    equipment_id: UUID
    component_id: UUID
    assessment_type: str
    overall_condition: str
    finding_count: int
    findings: list[AssessmentFindingResponse]
    recommendation: str
    assessment_metadata: dict
    assessed_at: datetime
