
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Sensor, TelemetryReading


# Reproducible synthetic data for development and testing.
random.seed(42)

READINGS_PER_PHASE = 100
INTERVAL_MINUTES = 1

SENSOR_CODES = {
    "vibration": "MX-CR-001-CB-001-VIB",
    "temperature": "MX-CR-001-CB-001-TEMP",
}


def generate_vibration(phase, index):
    """Generate illustrative vibration RMS readings in mm/s."""

    if phase == "normal":
        baseline = 2.0
        variation = 0.15

    elif phase == "early_degradation":
        baseline = 2.0 + (index / READINGS_PER_PHASE) * 1.5
        variation = 0.30

    else:  # advanced_degradation
        baseline = 4.5 + (index / READINGS_PER_PHASE) * 2.0
        variation = 0.55

    return max(0.1, random.gauss(baseline, variation))


def generate_temperature(phase, index):
    """Generate illustrative bearing temperature readings in °C."""

    if phase == "normal":
        baseline = 45.0
        variation = 1.0

    elif phase == "early_degradation":
        baseline = 45.0 + (index / READINGS_PER_PHASE) * 10.0
        variation = 1.8

    else:  # advanced_degradation
        baseline = 56.0 + (index / READINGS_PER_PHASE) * 14.0
        variation = 2.5

    return max(0.0, random.gauss(baseline, variation))


def generate_telemetry():
    phases = [
        "normal",
        "early_degradation",
        "advanced_degradation",
    ]

    with SessionLocal() as session:
        sensors = {
            sensor.sensor_code: sensor
            for sensor in session.scalars(
                select(Sensor).where(
                    Sensor.sensor_code.in_(SENSOR_CODES.values())
                )
            ).all()
        }

        missing_sensors = set(SENSOR_CODES.values()) - set(sensors)

        if missing_sensors:
            print("Missing sensors:", missing_sensors)
            print("Register the sensors before generating telemetry.")
            return

        start_time = datetime.now(timezone.utc) - timedelta(
            minutes=(len(phases) * READINGS_PER_PHASE)
        )

        readings = []

        for phase_number, phase in enumerate(phases):
            for index in range(READINGS_PER_PHASE):
                timestamp = start_time + timedelta(
                    minutes=(
                        phase_number * READINGS_PER_PHASE + index
                    ) * INTERVAL_MINUTES
                )

                vibration_value = generate_vibration(phase, index)
                temperature_value = generate_temperature(phase, index)

                readings.extend([
                    TelemetryReading(
                        sensor_id=sensors[SENSOR_CODES["vibration"]].id,
                        timestamp=timestamp,
                        value=round(vibration_value, 3),
                        quality="good",
                    ),
                    TelemetryReading(
                        sensor_id=sensors[SENSOR_CODES["temperature"]].id,
                        timestamp=timestamp,
                        value=round(temperature_value, 2),
                        quality="good",
                    ),
                ])

        session.add_all(readings)
        session.commit()

        print("Synthetic telemetry generated successfully.")
        print(f"Operating phases: {len(phases)}")
        print(f"Readings per sensor per phase: {READINGS_PER_PHASE}")
        print(f"Total telemetry records inserted: {len(readings)}")


if __name__ == "__main__":
    generate_telemetry()
