"""Deterministic one-site model of CYP time-dependent inactivation.

Given fitted experimental parameters k_inact and K_I, evaluate the apparent
first-order inactivation rate k_obs = k_inact * [I] / (K_I + [I]).

These equations are illustrative assay kinetics, NOT a clinical DDI prediction
or an estimation of k_inact/K_I from experimental datasets.
"""
import math
from typing import Dict, Optional


def calculate_tdi(
    kinact_per_min: float, ki_um: float, inhibitor_um: float, time_min: float
) -> Dict[str, Optional[float]]:
    """Calculate k_obs and remaining activity for a single inhibitor exposure.

    k_inact: min^-1; K_I and inhibitor concentration: micromolar;
    preincubation time: minutes. Assumes constant unbound concentration,
    single-site saturable inactivation, and first-order loss of activity.
    """
    values = {
        "kinact_per_min": kinact_per_min,
        "ki_um": ki_um,
        "inhibitor_um": inhibitor_um,
        "time_min": time_min,
    }
    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{name} must be a finite number")
        if value < 0:
            raise ValueError(f"{name} cannot be negative")
    if ki_um == 0:
        raise ValueError("ki_um must be greater than zero")

    # The normalized concentration ratio avoids overflow in K_I + [I].
    x = inhibitor_um / ki_um if inhibitor_um <= ki_um else ki_um / inhibitor_um
    fraction = x / (1 + x) if inhibitor_um <= ki_um else 1 / (1 + x)
    kobs = kinact_per_min * fraction
    efficiency = kinact_per_min / ki_um
    if not math.isfinite(efficiency):
        raise ValueError("k_inact/K_I is outside the representable numeric range")
    half_life = math.log(2) / kobs if kobs > 0 else None
    if half_life is not None and not math.isfinite(half_life):
        half_life = None
    return {
        "kobs_per_min": kobs,
        "remaining_activity_pct": 100 * math.exp(-kobs * time_min),
        "inactivation_half_life_min": half_life,
        "efficiency_per_min_per_um": efficiency,
    }
