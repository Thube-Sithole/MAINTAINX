
from sqlalchemy import select

from app.analytics.features import (
    calculate_sensor_features,
    summarize_sensor_features,
)
from app.database import SessionLocal
from app.models import Sensor, TelemetryReading


def analyse_telemetry():
    sensor_codes = [
        "MX-CR-001-CB-001-VIB",
        "MX-CR-001-CB-001-TEMP",
    ]

    with SessionLocal() as session:
        for sensor_code in sensor_codes:
            sensor = session.scalar(
                select(Sensor).where(
                    Sensor.sensor_code == sensor_code
                )
            )

            if not sensor:
                print(f"Sensor not found: {sensor_code}")
                continue

            readings = session.scalars(
                select(TelemetryReading)
                .where(TelemetryReading.sensor_id == sensor.id)
                .order_by(TelemetryReading.timestamp)
            ).all()

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

            print("\n" + "=" * 55)
            print(f"SENSOR: {sensor.sensor_code}")
            print(f"MEASUREMENT: {sensor.measurement_type}")
            print(f"UNIT: {sensor.unit}")
            print("=" * 55)

            for feature, value in summary.items():
                print(f"{feature}: {value}")

            print("\nLatest five engineered observations:")

            print(
                features[
                    [
                        "timestamp",
                        "value",
                        "rolling_mean",
                        "rolling_std",
                        "rate_of_change",
                    ]
                ].tail(5).to_string(index=False)
            )


if __name__ == "__main__":
    analyse_telemetry()
