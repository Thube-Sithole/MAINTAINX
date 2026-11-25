from sqlalchemy import select

from app.database import SessionLocal
from app.models import Component, Sensor


def register_sensors():
    component_code = "MX-CR-001-CB-001"

    sensors_to_register = [
        {
            "sensor_code": "MX-CR-001-CB-001-VIB",
            "measurement_type": "vibration_rms",
            "unit": "mm/s",
            "location": "Countershaft bearing housing",
        },
        {
            "sensor_code": "MX-CR-001-CB-001-TEMP",
            "measurement_type": "bearing_temperature",
            "unit": "°C",
            "location": "Countershaft bearing housing",
        },
    ]

    with SessionLocal() as session:
        component = session.scalar(
            select(Component).where(
                Component.component_code == component_code
            )
        )

        if not component:
            print("Component not found. Register it first.")
            return

        for sensor_data in sensors_to_register:
            existing_sensor = session.scalar(
                select(Sensor).where(
                    Sensor.sensor_code == sensor_data["sensor_code"]
                )
            )

            if existing_sensor:
                print(
                    f"Sensor already registered: "
                    f"{existing_sensor.sensor_code}"
                )
                continue

            sensor = Sensor(
                component_id=component.id,
                sensor_code=sensor_data["sensor_code"],
                measurement_type=sensor_data["measurement_type"],
                unit=sensor_data["unit"],
                location=sensor_data["location"],
                status="active",
            )

            session.add(sensor)
            session.flush()

            print(
                f"Sensor registered: {sensor.sensor_code} "
                f"({sensor.measurement_type}, {sensor.unit})"
            )

        session.commit()

        print("\nSensor registration process completed.")


if __name__ == "__main__":
    register_sensors()