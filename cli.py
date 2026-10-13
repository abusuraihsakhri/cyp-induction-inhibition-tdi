"""
Command Line Interface for Cyp Induction Inhibition Tdi.
"""
import argparse
import csv
import json
import sys
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor
from agents.base import AuditLogger

supervisor = SystemSupervisor(model_provider="mock")


def _parse_bool(value):
    """Parse boolean CSV fields explicitly; bool("False") is True."""
    normalized = str(value or "").strip().lower()
    if normalized in ("", "false", "0", "no", "n", "off"):
        return False
    if normalized in ("true", "1", "yes", "y", "on"):
        return True
    raise ValueError(f"Invalid is_critical_flag: {value!r}; use true or false")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="cyp-induction-inhibition-tdi", description="Cyp Induction Inhibition Tdi")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Audit
    p_audit = subparsers.add_parser("audit", help="Run single task evaluation")
    p_audit.add_argument("--task-id", default="TASK-2026-001")
    p_audit.add_argument("--target", default="KEY-TARGET-01")
    p_audit.add_argument("--primary", type=float, default=28.5)
    p_audit.add_argument("--secondary", type=float, default=14.2)
    p_audit.add_argument("--critical", action="store_true")
    p_audit.add_argument("--status", default="DISCORDANT")

    # Chat
    p_chat = subparsers.add_parser("chat", help="System configuration query")
    p_chat.add_argument("query", nargs="+")

    # Batch
    p_batch = subparsers.add_parser("batch", help="Batch process CSV records")
    p_batch.add_argument("-i", "--input", required=True)
    p_batch.add_argument("-o", "--output", default="results.csv")

    # Verify Audit
    subparsers.add_parser("verify-audit", help="Verify HMAC audit trail integrity")

    # Serve
    p_serve = subparsers.add_parser("serve", help="Launch FastAPI REST server")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)

    args = parser.parse_args(argv)

    if args.command == "audit":
        payload = SystemTaskPayload(
            task_id=args.task_id,
            target_identifier=args.target,
            primary_metric=args.primary,
            secondary_metric=args.secondary,
            status_descriptor=args.status,
            is_critical_flag=args.critical,
        )
        dossier = supervisor.process_task(payload)
        print("=" * 80)
        print(f"  CYP INDUCTION INHIBITION TDI")
        print(f"  Domain: AI Drug Discovery, Structural Biology & Wet-Lab Robotics | Standard: wwPDB / IUPAC / OpenSMILES / ISAC Standards")
        print(f"  Dossier ID: {dossier.dossier_id} | Urgency: [{dossier.overall_urgency.value}]")
        print("=" * 80)
        for a in dossier.alerts:
            print(f"\n  [{a.urgency.value}] from {a.origin_worker}:")
            print(f"  Summary: {a.summary}")
            print(f"  Details: {a.technical_details}")
            print(f"  Action:  {a.actionable_remediation}")
        print(f"\n  HMAC-SHA256 Audit Hash: {dossier.audit_hash}")
        print("=" * 80)
        return 0

    if args.command == "chat":
        ans = supervisor.query_supervisory_chat(" ".join(args.query))
        print(f"\n[Cyp Induction Inhibition Tdi Supervisor]:\n{ans}\n")
        return 0

    if args.command == "verify-audit":
        trail = AuditLogger.get_trail()
        valid = AuditLogger.verify_integrity()
        print(f"Audit Trail Blocks: {len(trail)} | Cryptographic Integrity Verified: {valid}")
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

        extra_fields = ["overall_urgency", "integrity_status", "total_alerts", "audit_hash"]
        out_fields = list(dict.fromkeys(fieldnames + extra_fields))
        out_rows = []
        for line_number, row in enumerate(rows, start=2):
            try:
                if None in row:
                    raise ValueError("row contains more columns than the header")
                payload = SystemTaskPayload(
                    task_id=row.get("task_id") or "TASK-01",
                    target_identifier=row.get("target_identifier") or "TARGET-01",
                    primary_metric=float(row.get("primary_metric") or 15.0),
                    secondary_metric=float(row.get("secondary_metric") or 5.0),
                    status_descriptor=row.get("status_descriptor") or "NOMINAL",
                    is_critical_flag=_parse_bool(row.get("is_critical_flag")),
                )
                dossier = supervisor.process_task(payload)
                output = dict(row)
                output.update(
                    overall_urgency=dossier.overall_urgency.value,
                    integrity_status=dossier.integrity_status.value,
                    total_alerts=dossier.total_alerts,
                    audit_hash=dossier.audit_hash,
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
        import uvicorn
        from agents.api import app
        print(f"Starting Cyp Induction Inhibition Tdi API server on http://{args.host}:{args.port}")
        uvicorn.run(app, host=args.host, port=args.port)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
