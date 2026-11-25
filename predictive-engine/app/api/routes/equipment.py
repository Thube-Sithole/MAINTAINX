
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models import Equipment
from app.schemas import EquipmentResponse


router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"],
)


@router.get(
    "/",
    response_model=list[EquipmentResponse],
)
def list_equipment(
    db: Session = Depends(get_db),
):
    """Retrieve all registered equipment."""

    statement = select(Equipment).order_by(
        Equipment.equipment_code
    )

    equipment_records = db.scalars(statement).all()

    return equipment_records


@router.get(
    "/{equipment_id}",
    response_model=EquipmentResponse,
)
def get_equipment(
    equipment_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve a specific equipment record."""

    equipment = db.get(Equipment, equipment_id)

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found.",
        )

    return equipment
