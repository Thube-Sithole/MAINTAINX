
from sqlalchemy import select

from app.assessment.service import create_equipment_assessment
from app.database import SessionLocal
from app.models import Equipment


EQUIPMENT_CODE = "MX-CR-001"


def assess_equipment():
    with SessionLocal() as session:

        equipment = session.scalar(
            select(Equipment).where(
                Equipment.equipment_code == EQUIPMENT_CODE
            )
        )

        if not equipment:
            raise ValueError(
                f"Equipment not found: {EQUIPMENT_CODE}"
            )

        health_record = create_equipment_assessment(
            session=session,
            equipment_id=equipment.id,
        )

        print("\n" + "=" * 60)
        print("MAINTAINX - EQUIPMENT CONDITION ASSESSMENT")
        print("=" * 60)

        print(f"\nEquipment: {equipment.name}")
        print(f"Equipment code: {equipment.equipment_code}")

        print("\nCONDITION ASSESSMENT")
        print("-" * 60)

        print(
            "Overall condition:",
            health_record.overall_condition.upper(),
        )

        print("Assessment type:", health_record.assessment_type)
        print("Finding count:", health_record.finding_count)

        for finding in health_record.findings:
            print(f"\nSensor: {finding['sensor']}")
            print(f"Severity: {finding['severity'].upper()}")
            print(
                f"Measured value: {finding['value']} "
                f"{finding['unit']}"
            )
            print(f"Finding: {finding['message']}")

        print("\nRECOMMENDATION")
        print("-" * 60)
        print(health_record.recommendation)

        print("\nPERSISTENCE")
        print("-" * 60)
        print("Assessment successfully saved!")
        print(f"Assessment ID: {health_record.id}")
        print(f"Assessment timestamp: {health_record.assessed_at}")

        print("\n" + "=" * 60)


if __name__ == "__main__":
    assess_equipment()
