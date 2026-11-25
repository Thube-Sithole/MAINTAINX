
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.analytics.features import (
    calculate_sensor_features,
    summarize_sensor_features,
)
from app.assessment.condition_engine import assess_condition
from app.models import (
    Component,
    Equipment,
    HealthAssessment,
    Sensor,
    TelemetryReading,
)


def get_sensor_features(
    session: Session,
    component_id: UUID,
    measurement_type: str,
):
    """Retrieve sensor telemetry and calculate its features."""

    sensor = session.scalar(
        select(Sensor).where(
            Sensor.component_id == component_id,
            Sensor.measurement_type == measurement_type,
        )
    )

    if not sensor:
        raise ValueError(
            f"Sensor not found for measurement type: {measurement_type}"
        )

    readings = session.scalars(
        select(TelemetryReading)
        .where(TelemetryReading.sensor_id == sensor.id)
        .order_by(TelemetryReading.timestamp)
    ).all()

    if not readings:
        raise ValueError(
            f"No telemetry readings found for sensor: {sensor.sensor_code}"
        )

    reading_data = [
        {
            "timestamp": reading.timestamp,
            "value": reading.value,
        }
        for reading in readings
    ]

    features = calculate_sensor_features(
        reading_data,
        window_size=10,
    )

    summary = summarize_sensor_features(features)

    return sensor, summary


def create_equipment_assessment(
    session: Session,
    equipment_id: UUID,
    component_id: UUID | None = None,
) -> HealthAssessment:
    """Assess equipment condition and persist the assessment."""

    equipment = session.get(Equipment, equipment_id)

    if not equipment:
        raise ValueError("Equipment not found.")

    component_statement = select(Component).where(
        Component.equipment_id == equipment.id,
        Component.component_type == "bearing",
    )

    if component_id is not None:
        component_statement = component_statement.where(
            Component.id == component_id
        )

    components = session.scalars(component_statement).all()

    if not components:
        raise ValueError(
            "No matching bearing component found for this equipment."
        )

    if len(components) > 1:
        raise ValueError(
            "Multiple bearing components found. Specify a component ID."
        )

    component = components[0]

    vibration_sensor, vibration_features = get_sensor_features(
        session,
        component.id,
        "vibration_rms",
    )

    temperature_sensor, temperature_features = get_sensor_features(
        session,
        component.id,
        "bearing_temperature",
    )

    assessment = assess_condition(
        vibration_features=vibration_features,
        temperature_features=temperature_features,
    )

    health_record = HealthAssessment(
        equipment_id=equipment.id,
        component_id=component.id,
        assessment_type=assessment["assessment_type"],
        overall_condition=assessment["equipment_condition"],
        finding_count=assessment["finding_count"],
        findings=assessment["findings"],
        recommendation=assessment["recommendation"],
        assessment_metadata={
            "sensor_features": {
                "vibration": vibration_features,
                "temperature": temperature_features,
            },
            "thresholds": assessment["thresholds"],
            "limitations": assessment["limitations"],
        },
    )

    try:
        session.add(health_record)
        session.commit()
        session.refresh(health_record)

    except Exception:
        session.rollback()
        raise

    return health_record
