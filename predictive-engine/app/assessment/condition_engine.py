
from dataclasses import dataclass


@dataclass
class ConditionThresholds:
    """
    Illustrative development thresholds.

    These are not manufacturer specifications,
    validated failure limits, or safety limits.
    """

    vibration_warning: float = 4.0
    vibration_critical: float = 6.0

    temperature_warning: float = 55.0
    temperature_critical: float = 65.0


def assess_condition(
    vibration_features: dict,
    temperature_features: dict,
    thresholds: ConditionThresholds | None = None,
) -> dict:
    """
    Evaluate bearing condition using vibration
    and temperature sensor summaries.

    Returns an explainable condition assessment.
    """

    if thresholds is None:
        thresholds = ConditionThresholds()

    findings = []

    vibration_mean = vibration_features.get(
        "latest_rolling_mean"
    )

    temperature_mean = temperature_features.get(
        "latest_rolling_mean"
    )

    # Validate that the required features are available.
    if vibration_mean is None or temperature_mean is None:
        raise ValueError(
            "Both sensors require valid rolling means."
        )

    # Evaluate vibration behaviour.
    if vibration_mean >= thresholds.vibration_critical:
        findings.append({
            "sensor": "vibration_rms",
            "severity": "critical",
            "value": vibration_mean,
            "unit": "mm/s",
            "message": (
                "Vibration RMS exceeds the illustrative "
                "critical development threshold."
            ),
        })

    elif vibration_mean >= thresholds.vibration_warning:
        findings.append({
            "sensor": "vibration_rms",
            "severity": "warning",
            "value": vibration_mean,
            "unit": "mm/s",
            "message": (
                "Vibration RMS exceeds the illustrative "
                "warning development threshold."
            ),
        })

    # Evaluate bearing temperature.
    if temperature_mean >= thresholds.temperature_critical:
        findings.append({
            "sensor": "bearing_temperature",
            "severity": "critical",
            "value": temperature_mean,
            "unit": "°C",
            "message": (
                "Bearing temperature exceeds the illustrative "
                "critical development threshold."
            ),
        })

    elif temperature_mean >= thresholds.temperature_warning:
        findings.append({
            "sensor": "bearing_temperature",
            "severity": "warning",
            "value": temperature_mean,
            "unit": "°C",
            "message": (
                "Bearing temperature exceeds the illustrative "
                "warning development threshold."
            ),
        })

    # Determine the overall condition.
    severities = [
        finding["severity"]
        for finding in findings
    ]

    if "critical" in severities:
        overall_condition = "critical"

    elif "warning" in severities:
        overall_condition = "warning"

    else:
        overall_condition = "normal"

    # Generate a human-readable recommendation.
    recommendations = {
        "normal": (
            "Continue monitoring equipment condition "
            "and maintain routine inspections."
        ),
        "warning": (
            "Investigate the elevated sensor readings "
            "and review recent operating conditions."
        ),
        "critical": (
            "Prioritise an engineering inspection and "
            "review the equipment's operating condition."
        ),
    }

    return {
        "equipment_condition": overall_condition,
        "assessment_type": "rule_based",
        "findings": findings,
        "finding_count": len(findings),
        "recommendation": recommendations[overall_condition],
        "thresholds": {
            "vibration_warning": thresholds.vibration_warning,
            "vibration_critical": thresholds.vibration_critical,
            "temperature_warning": thresholds.temperature_warning,
            "temperature_critical": thresholds.temperature_critical,
        },
        "limitations": (
            "Development demonstration using synthetic telemetry "
            "and illustrative thresholds. Not validated for "
            "operational maintenance decisions."
        ),
    }
