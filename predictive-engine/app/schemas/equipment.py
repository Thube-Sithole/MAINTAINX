
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EquipmentResponse(BaseModel):
    """Schema for returning equipment information."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    equipment_code: str
    name: str
    equipment_type: str
    manufacturer: str | None = None
    model: str | None = None
    site: str | None = None
    description: str | None = None
    status: str
    created_at: datetime
