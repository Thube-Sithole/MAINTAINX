
import numpy as np
import pandas as pd


def calculate_sensor_features(
    readings: list[dict],
    window_size: int = 10,
) -> pd.DataFrame:
    """
    Calculate statistical and time-series features
    for an individual sensor.

    Each reading must contain:
        timestamp
        value
    """

    if not readings:
        raise ValueError("No sensor readings supplied.")

    if window_size < 2:
        raise ValueError("window_size must be at least 2.")

    dataframe = pd.DataFrame(readings)

    required_columns = {"timestamp", "value"}

    if not required_columns.issubset(dataframe.columns):
        raise ValueError(
            "Each reading must contain timestamp and value."
        )

    dataframe["timestamp"] = pd.to_datetime(
        dataframe["timestamp"],
        utc=True,
    )

    dataframe["value"] = pd.to_numeric(
        dataframe["value"],
        errors="raise",
    )

    if dataframe["value"].isna().any():
        raise ValueError("Sensor readings cannot contain null values.")

    if not np.isfinite(dataframe["value"]).all():
        raise ValueError("Sensor readings must contain finite values.")

    dataframe = dataframe.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    # Short-term statistical features.
    dataframe["rolling_mean"] = (
        dataframe["value"]
        .rolling(window=window_size, min_periods=window_size)
        .mean()
    )

    dataframe["rolling_std"] = (
        dataframe["value"]
        .rolling(window=window_size, min_periods=window_size)
        .std()
    )

    # Change in the measurement from the previous reading.
    dataframe["rate_of_change"] = dataframe["value"].diff()

    # Overall sensor statistics, repeated for convenient inspection.
    dataframe["overall_mean"] = dataframe["value"].mean()
    dataframe["overall_std"] = dataframe["value"].std()
    dataframe["overall_min"] = dataframe["value"].min()
    dataframe["overall_max"] = dataframe["value"].max()

    return dataframe


def summarize_sensor_features(
    dataframe: pd.DataFrame,
) -> dict:
    """Produce a compact statistical summary."""

    if dataframe.empty:
        raise ValueError("Cannot summarize an empty dataframe.")

    return {
        "reading_count": int(len(dataframe)),
        "mean": round(float(dataframe["value"].mean()), 3),
        "standard_deviation": round(
            float(dataframe["value"].std()), 3
        ),
        "minimum": round(float(dataframe["value"].min()), 3),
        "maximum": round(float(dataframe["value"].max()), 3),
        "latest_value": round(
            float(dataframe.iloc[-1]["value"]), 3
        ),
        "latest_rolling_mean": (
            round(float(dataframe.iloc[-1]["rolling_mean"]), 3)
            if pd.notna(dataframe.iloc[-1]["rolling_mean"])
            else None
        ),
        "latest_rolling_std": (
            round(float(dataframe.iloc[-1]["rolling_std"]), 3)
            if pd.notna(dataframe.iloc[-1]["rolling_std"])
            else None
        ),
    }
