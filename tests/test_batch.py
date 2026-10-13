"""Batch CSV regression checks for both preserved command-line interfaces."""
import csv
from pathlib import Path
import pytest
from cli import main as legacy_main
from cyp_kinetics.cli import main as kinetics_main


@pytest.mark.parametrize("runner,column,critical", [
    (legacy_main, "overall_urgency", "CRITICAL_STAT_PANIC"),
    (kinetics_main, "overall_status", "CRITICAL_INTERVENTION_REQUIRED"),
])
def test_batch_false_and_true_flags(tmp_path, runner, column, critical):
    source = tmp_path / "input.csv"
    target = tmp_path / "output.csv"
    source.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "ONE,KEY-1,10,2,False,NOMINAL\n"
        "TWO,KEY-2,10,2,True,NOMINAL\n", encoding="utf-8"
    )
    assert runner(["batch", "-i", str(source), "-o", str(target)]) == 0
    with target.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 2
    assert rows[0][column] != critical
    assert rows[1][column] == critical


@pytest.mark.parametrize("runner", [legacy_main, kinetics_main])
@pytest.mark.parametrize("flag", ["maybe", "not boolean", "falsee"])
def test_batch_rejects_invalid_flags_without_output(tmp_path, runner, flag):
    src = tmp_path / "input.csv"
    dest = tmp_path / "output.csv"
    src.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        f"ONE,KEY-1,10,2,{flag},NOMINAL\n", encoding="utf-8"
    )
    assert runner(["batch", "-i", str(src), "-o", str(dest)]) == 1
    assert not dest.exists()


@pytest.mark.parametrize("runner", [legacy_main, kinetics_main])
def test_batch_rejects_nonfinite_values(tmp_path, runner):
    src = tmp_path / "input.csv"
    dest = tmp_path / "output.csv"
    src.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "ONE,KEY-1,nan,2,False,NOMINAL\n", encoding="utf-8"
    )
    assert runner(["batch", "-i", str(src), "-o", str(dest)]) == 1
    assert not dest.exists()
