from sqlalchemy import select

from app.database import SessionLocal
from app.models import Component, Equipment


def register_component():
    component_code = "MX-CR-001-CB-001"
    equipment_code = "MX-CR-001"

    with SessionLocal() as session:
        equipment = session.scalar(
            select(Equipment).where(
                Equipment.equipment_code == equipment_code
            )
        )

        if not equipment:
            print("Equipment not found. Register it first.")
            return

        existing_component = session.scalar(
            select(Component).where(
                Component.component_code == component_code
            )
        )

        if existing_component:
            print("Component already registered.")
            print(f"ID: {existing_component.id}")
            print(f"Code: {existing_component.component_code}")
            return

        component = Component(
            equipment_id=equipment.id,
            component_code=component_code,
            name="Countershaft Bearing",
            component_type="bearing",
            location="Countershaft assembly",
            status="operational",
        )

        session.add(component)
        session.commit()
        session.refresh(component)

        print("Component successfully registered!")
        print(f"ID: {component.id}")
        print(f"Code: {component.component_code}")
        print(f"Name: {component.name}")
        print(f"Equipment: {equipment.name}")
        print(f"Status: {component.status}")


if __name__ == "__main__":
    register_component()