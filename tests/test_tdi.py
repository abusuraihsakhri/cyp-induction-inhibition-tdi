"""Independent analytical checks for illustrative TDI kinetics and audit integrity."""
import math
import pytest

from cyp_kinetics.tdi import calculate_tdi
from agents.base import AuditTrail


def test_tdi_known_parameters():
    result = calculate_tdi(0.2, 5.0, 5.0, 10.0)
    assert result["kobs_per_min"] == pytest.approx(0.1)
    assert result["remaining_activity_pct"] == pytest.approx(100 * math.exp(-1))
    assert result["inactivation_half_life_min"] == pytest.approx(math.log(2) / 0.1)
    assert result["efficiency_per_min_per_um"] == pytest.approx(0.04)


def test_zero_exposure_and_inactivation():
    result = calculate_tdi(0.0, 5.0, 5.0, 10.0)
    assert result["kobs_per_min"] == 0
    assert result["remaining_activity_pct"] == 100
    assert result["inactivation_half_life_min"] is None
    result = calculate_tdi(0.5, 5.0, 0.0, 15.0)
    assert result["remaining_activity_pct"] == 100


@pytest.mark.parametrize("parameters", [
    (-1, 5, 5, 10), (0.2, 0, 5, 10), (0.2, 5, -1, 10),
    (0.2, 5, 5, -1), (math.nan, 5, 5, 10),
    (0.2, math.inf, 5, 10), (True, 5, 5, 10),
])
def test_bad_kinetics_rejected(parameters):
    with pytest.raises(ValueError):
        calculate_tdi(*parameters)


def test_audit_chain_recomputes_hmac():
    chain = AuditTrail("test-hmac-key")
    chain.log("worker", "supervisor", "START", {"task_id": "TEST-1"})
    chain.log("worker", "supervisor", "END", {"task_id": "TEST-1"})
    assert chain.verify_integrity()
    copy = chain.get_trail()
    copy[0]["event_type"] = "tampered"
    assert chain.verify_integrity()  # public snapshots are independent
    chain.logs[0]["event_type"] = "tampered"
    assert not chain.verify_integrity()


def test_audit_chain_detects_modified_signature():
    chain = AuditTrail("test-hmac-key")
    chain.log("worker", "supervisor", "START", {"task_id": "TEST-1"})
    chain.logs[0]["current_hash"] = "0" * 64
    assert not chain.verify_integrity()
