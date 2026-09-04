"""
Data Models & Telemetry Definitions for CYP-Kin: Time-Dependent Inhibition (TDI) & Kinact/KI Pharmacokinetic Agent.
Domain: Computational Chemistry & AI Drug Discovery
Standard: FDA In Vitro Drug Interaction Studies 2020
"""
import datetime
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class ExecutionStatus(str, Enum):
    NOMINAL = "NOMINAL_OPTIMAL"
    ELEVATED_RISK = "ELEVATED_RISK_WARNING"
    CRITICAL_INTERVENTION = "CRITICAL_INTERVENTION_REQUIRED"


def _validate_finite_metric(value: float, field_name: str) -> float:
    """Ensure metric values are finite (not NaN or Inf)."""
    if not isinstance(value, (int, float)) or math.isnan(value) or math.isinf(value):
        raise ValueError(f"{field_name} must be a finite number, got {value!r}")
    return float(value)


@dataclass
class FrontierPayload:
    task_id: str
    target_identifier: str
    primary_metric: float
    secondary_metric: float
    status_descriptor: str
    is_critical_flag: bool = False
    attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def __post_init__(self):
        self.primary_metric = _validate_finite_metric(self.primary_metric, "primary_metric")
        self.secondary_metric = _validate_finite_metric(self.secondary_metric, "secondary_metric")


@dataclass
class AgentTelemetryAlert:
    alert_id: str
    origin_agent: str
    status: ExecutionStatus
    summary: str
    technical_details: str
    actionable_remediation: str
    standard_reference: str = "FDA In Vitro Drug Interaction Studies 2020"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "origin_agent": self.origin_agent,
            "status": self.status.value,
            "summary": self.summary,
            "technical_details": self.technical_details,
            "actionable_remediation": self.actionable_remediation,
            "standard_reference": self.standard_reference,
            "timestamp": self.timestamp,
        }
