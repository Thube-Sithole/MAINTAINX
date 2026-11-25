from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models import HealthAssessment
from app.schemas import AssessmentResponse
from app.assessment.service import create_equipment_assessment


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)
assessment_execution_router = APIRouter(
    tags=["Assessments"],
)

@router.get(
    "/",
    response_model=list[AssessmentResponse],
)
def list_assessments(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """Retrieve historical equipment condition assessments."""

    statement = (
        select(HealthAssessment)
        .order_by(HealthAssessment.assessed_at.desc())
        .limit(limit)
        .offset(offset)
    )

    assessments = db.scalars(statement).all()

    return assessments


@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse,
)
def get_assessment(
    assessment_id: UUID,
    db: Session = Depends(get_db),
):
    """Retrieve an individual condition assessment."""

    assessment = db.get(HealthAssessment, assessment_id)

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found.",
        )

    return assessment

@assessment_execution_router.post(
    "/equipment/{equipment_id}/assess",
    response_model=AssessmentResponse,
    status_code=201,
)
def run_equipment_assessment(
    equipment_id: UUID,
    db: Session = Depends(get_db),
):
    """Run and persist a new equipment condition assessment."""

    try:
        assessment = create_equipment_assessment(
            session=db,
            equipment_id=equipment_id,
        )

        return assessment

    except ValueError as exc:
        if str(exc) == "Equipment not found.":
            raise HTTPException(
                status_code=404,
                detail=str(exc),
            ) from exc

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
