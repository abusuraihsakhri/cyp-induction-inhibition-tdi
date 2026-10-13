"""
Command-Line Interface for CYP-Kin: Time-Dependent Inhibition (TDI) & Kinact/KI Pharmacokinetic Agent.
"""
import argparse
import csv
import json
import sys
from .models import FrontierPayload
from .agents import CYPKineticsCoordinator

coordinator = CYPKineticsCoordinator()


def _parse_bool(value):
    """Parse boolean CSV fields explicitly; bool("False") is True."""
    normalized = str(value or "").strip().lower()
    if normalized in ("", "false", "0", "no", "n", "off"):
        return False
    if normalized in ("true", "1", "yes", "y", "on"):
        return True
    raise ValueError(f"Invalid is_critical_flag: {value!r}; use true or false")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="cyp-induction-inhibition-tdi", description="CYP-Kin: Time-Dependent Inhibition (TDI) & Kinact/KI Pharmacokinetic Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Audit
    p_audit = subparsers.add_parser("audit", help="Run single task evaluation")
    p_audit.add_argument("--task-id", default="TASK-2026-001")
    p_audit.add_argument("--target", default="TARGET-GEN-01")
    p_audit.add_argument("--primary", type=float, default=29.4)
    p_audit.add_argument("--secondary", type=float, default=15.1)
    p_audit.add_argument("--critical", action="store_true")
    p_audit.add_argument("--status", default="DISCORDANT")

    # Chat
    p_chat = subparsers.add_parser("chat", help="System configuration query")
    p_chat.add_argument("query", nargs="+")

    # Batch
    p_batch = subparsers.add_parser("batch", help="Batch process CSV records")
    p_batch.add_argument("-i", "--input", required=True)
    p_batch.add_argument("-o", "--output", default="results.csv")

    # Serve
    p_serve = subparsers.add_parser("serve", help="Launch FastAPI REST server")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)

    args = parser.parse_args(argv)

    if args.command == "audit":
        payload = FrontierPayload(
            task_id=args.task_id,
            target_identifier=args.target,
            primary_metric=args.primary,
            secondary_metric=args.secondary,
            status_descriptor=args.status,
            is_critical_flag=args.critical,
        )
        dossier = coordinator.process(payload)
        print("=" * 80)
        print(f"  CYP-KIN: TIME-DEPENDENT INHIBITION (TDI) & KINACT/KI PHARMACOKINETIC AGENT")
        print(f"  Domain: Computational Chemistry & AI Drug Discovery | Standard: FDA In Vitro Drug Interaction Studies 2020")
        print(f"  Task: {dossier['task_id']} | Status: [{dossier['overall_status']}] | Total Alerts: {dossier['total_alerts']}")
        print("=" * 80)
        for a in dossier["alerts"]:
            print(f"\n  [{a['status']}] from {a['origin_agent']}:")
            print(f"  Summary: {a['summary']}")
            print(f"  Details: {a['technical_details']}")
            print(f"  Action:  {a['actionable_remediation']}")
        print("\n" + "=" * 80)
        return 0

    if args.command == "chat":
        ans = coordinator.query_supervisory_chat(" ".join(args.query))
        print(f"\n[CYPKineticsCoordinator]:\n{ans}\n")
        return 0

    if args.command == "batch":
        try:
            with open(args.input, mode="r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                fieldnames = list(reader.fieldnames or [])
                if not fieldnames:
                    raise ValueError("CSV header is missing")
                rows = list(reader)
        except (OSError, UnicodeError, csv.Error, ValueError) as exc:
            print(f"Error reading CSV: {exc}", file=sys.stderr)
            return 1

        extra_fields = ["overall_status", "total_alerts", "critical_count", "consensus_summary"]
        out_fields = list(dict.fromkeys(fieldnames + extra_fields))
        out_rows = []
        for line_number, row in enumerate(rows, start=2):
            try:
                if None in row:
                    raise ValueError("row contains more columns than the header")
                payload = FrontierPayload(
                    task_id=row.get("task_id") or "TASK-01",
                    target_identifier=row.get("target_identifier") or "TARGET-01",
                    primary_metric=float(row.get("primary_metric") or 15.0),
                    secondary_metric=float(row.get("secondary_metric") or 5.0),
                    status_descriptor=row.get("status_descriptor") or "NOMINAL",
                    is_critical_flag=_parse_bool(row.get("is_critical_flag")),
                )
                dossier = coordinator.process(payload)
                output = dict(row)
                output.update(
                    overall_status=dossier["overall_status"],
                    total_alerts=dossier["total_alerts"],
                    critical_count=dossier["critical_count"],
                    consensus_summary=dossier["consensus_summary"],
                )
                out_rows.append(output)
            except (ValueError, TypeError) as exc:
                print(f"Invalid CSV row {line_number}: {exc}", file=sys.stderr)
                return 1

        try:
            with open(args.output, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=out_fields)
                writer.writeheader()
                writer.writerows(out_rows)
        except (OSError, UnicodeError, csv.Error) as exc:
            print(f"Error writing CSV: {exc}", file=sys.stderr)
            return 1
        print(f"Processed {len(out_rows)} records -> {args.output}")
        return 0

    if args.command == "serve":
        try:
            import uvicorn
            from .server import create_app
            app = create_app()
            if app:
                print(f"Starting CYP-Kin: Time-Dependent Inhibition (TDI) & Kinact/KI Pharmacokinetic Agent on http://{args.host}:{args.port}")
                uvicorn.run(app, host=args.host, port=args.port)
        except ImportError:
            print("FastAPI / uvicorn not installed. Run 'pip install fastapi uvicorn'")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
