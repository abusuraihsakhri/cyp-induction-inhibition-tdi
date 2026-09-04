import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import math
import pytest
from cyp_kinetics.models import FrontierPayload, ExecutionStatus
from cyp_kinetics.engine import FrontierDomainEngine
from cyp_kinetics.agents import KinactKICalculatorAgent, PartitionRatioAssessorAgent, ClinicalDDIProjectionAgent, CYPKineticsCoordinator
from cyp_kinetics.cli import main


def test_frontier_payload_rejects_nan():
    """NaN values should be rejected by FrontierPayload validation."""
    with pytest.raises(ValueError, match="primary_metric must be a finite number"):
        FrontierPayload(task_id="T-NAN", target_identifier="KEY-NAN", primary_metric=math.nan,
                        secondary_metric=4.0, status_descriptor="NOMINAL")


def test_frontier_payload_rejects_inf():
    """Infinity values should be rejected by FrontierPayload validation."""
    with pytest.raises(ValueError, match="primary_metric must be a finite number"):
        FrontierPayload(task_id="T-INF", target_identifier="KEY-INF", primary_metric=math.inf,
                        secondary_metric=4.0, status_descriptor="NOMINAL")

    with pytest.raises(ValueError, match="secondary_metric must be a finite number"):
        FrontierPayload(task_id="T-INF2", target_identifier="KEY-INF2", primary_metric=10.0,
                        secondary_metric=-math.inf, status_descriptor="NOMINAL")


def test_batch_file_not_found():
    """Batch command should return non-zero exit code for missing file."""
    result = main(["batch", "-i", "nonexistent_file.csv"])
    assert result == 1


def test_sub_agents():
    a1 = KinactKICalculatorAgent()
    p1 = FrontierPayload("T1", "KEY-01", primary_metric=35.0, secondary_metric=4.0, status_descriptor="NOMINAL")
    alerts1 = a1.audit(p1)
    assert len(alerts1) == 1
    assert alerts1[0].status == ExecutionStatus.ELEVATED_RISK

    a2 = PartitionRatioAssessorAgent()
    p2 = FrontierPayload("T2", "KEY-02", primary_metric=10.0, secondary_metric=15.0, status_descriptor="NOMINAL", is_critical_flag=True)
    alerts2 = a2.audit(p2)
    assert len(alerts2) == 1
    assert alerts2[0].status == ExecutionStatus.CRITICAL_INTERVENTION

    a3 = ClinicalDDIProjectionAgent()
    p3 = FrontierPayload("T3", "KEY-03", primary_metric=10.0, secondary_metric=4.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = a3.audit(p3)
    assert len(alerts3) == 1


def test_coordinator():
    coord = CYPKineticsCoordinator()
    p_nominal = FrontierPayload("T4", "KEY-04", primary_metric=12.0, secondary_metric=4.0, status_descriptor="NOMINAL")
    dossier = coord.process(p_nominal)
    assert dossier["overall_status"] == ExecutionStatus.NOMINAL.value
    assert dossier["total_alerts"] == 0

    ans = coord.query_supervisory_chat("What standard is applied?")
    assert "FDA In Vitro Drug Interaction Studies 2020" in ans or "specifications" in ans


def test_cli():
    assert main(["audit", "--task-id", "CLI-01"]) == 0
    assert main(["chat", "What", "is", "the", "system", "status?"]) == 0
