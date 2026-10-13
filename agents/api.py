"""
FastAPI REST API Server for Cyp Induction Inhibition Tdi.
"""
from pathlib import Path
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard, SecurityException
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor
from cyp_kinetics.tdi import calculate_tdi

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Cyp Induction Inhibition Tdi API",
    description="Enterprise Distributed Component Platform (AI Drug Discovery, Structural Biology & Wet-Lab Robotics)",
    version="3.0.0-ENTERPRISE",
)


class ChatRequest(BaseModel):
    query: str


class TDIRequest(BaseModel):
    kinact_per_min: float
    ki_um: float
    inhibitor_um: float
    time_min: float


@app.exception_handler(SecurityException)
async def blocked_identifier_handler(request, exc):
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.post("/api/kinetics")
def api_kinetics(req: TDIRequest):
    try:
        return calculate_tdi(
            req.kinact_per_min, req.ki_um, req.inhibitor_um, req.time_min
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "cyp-induction-inhibition-tdi", "domain": "AI Drug Discovery, Structural Biology & Wet-Lab Robotics", "standard": "wwPDB / IUPAC / OpenSMILES / ISAC Standards", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "NOMINAL_OPTIMAL"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    dossier = supervisor.process_task(payload)
    return dossier.to_dict()


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except SecurityException as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/audit/logs")
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}


# Mount the static browser calculator last, after all API routes.
app.mount("/", StaticFiles(directory=str(Path(__file__).resolve().parents[1] / "web"), html=True), name="web")
