
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Equipment


def register_equipment():
    equipment_code = "MX-CR-001"

    with SessionLocal() as session:
        # Check whether this equipment already exists.
        existing_equipment = session.scalar(
            select(Equipment).where(
                Equipment.equipment_code == equipment_code
            )
        )

        if existing_equipment:
            print("Equipment already registered.")
            print(f"ID: {existing_equipment.id}")
            print(f"Code: {existing_equipment.equipment_code}")
            print(f"Name: {existing_equipment.name}")
            return

        # Create a new demonstration equipment record.
        equipment = Equipment(
            equipment_code=equipment_code,
            name="Primary Cone Crusher",
            equipment_type="cone_crusher",
            manufacturer="Generic Demo",
            model="CR-DEMO-01",
            site="Demo Mining Site",
            description=(
                "Demonstration cone crusher for MAINTAINX "
                "predictive maintenance development."
            ),
            status="operational",
        )

        session.add(equipment)
        session.commit()
        session.refresh(equipment)

        print("Equipment successfully registered!")
        print(f"ID: {equipment.id}")
        print(f"Code: {equipment.equipment_code}")
        print(f"Name: {equipment.name}")
        print(f"Site: {equipment.site}")
        print(f"Status: {equipment.status}")


if __name__ == "__main__":
    register_equipment()
