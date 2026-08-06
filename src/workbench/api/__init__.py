"""Thin FastAPI surface over the validation SDK and audit chain (P2).

No business logic lives here: every endpoint is a direct passthrough to
`ValidationRun` / `verify_audit_chain`, matching the P0/P1 CLI's use of the
same SDK entry points.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from workbench.audit import verify_audit_chain
from workbench.sdk import ValidationRun

REPORT_FILENAME = "validation_report.md"
DEFAULT_ARTIFACTS_ROOT = "artifacts"

app = FastAPI(
    title="Workbench Validation API",
    description="Thin HTTP surface over ValidationRun and the audit chain verifier.",
    version="0.1.0",
)


class ValidateRequest(BaseModel):
    config: str


class ValidateResponse(BaseModel):
    run_id: str
    status: str
    artifact_dir: str
    report_path: str


class AuditVerifyResponse(BaseModel):
    status: str
    events: int
    breaks: list[str]


@app.post("/validate", response_model=ValidateResponse)
def validate(request: ValidateRequest) -> ValidateResponse:
    config_path = Path(request.config)
    if not config_path.exists():
        raise HTTPException(status_code=400, detail=f"config not found: {request.config}")
    try:
        result = ValidationRun.from_config(config_path).run()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return ValidateResponse(
        run_id=result.run_id,
        status="PASS",
        artifact_dir=str(result.artifact_dir),
        report_path=str(result.report_path),
    )


@app.get("/report/{run_id}", response_class=PlainTextResponse)
def get_report(run_id: str, artifacts_root: str = DEFAULT_ARTIFACTS_ROOT) -> str:
    if not run_id or run_id in {".", ".."} or "/" in run_id or "\\" in run_id:
        raise HTTPException(status_code=400, detail="invalid run_id")
    report_path = Path(artifacts_root) / run_id / REPORT_FILENAME
    if not report_path.exists():
        raise HTTPException(status_code=404, detail=f"report not found for run_id={run_id}")
    return report_path.read_text()


@app.get("/audit/verify", response_model=AuditVerifyResponse)
def get_audit_verify(db: str) -> AuditVerifyResponse:
    db_path = Path(db)
    if not db_path.exists():
        raise HTTPException(status_code=404, detail=f"audit db not found: {db}")
    verification = verify_audit_chain(db_path)
    return AuditVerifyResponse(
        status=verification.status,
        events=verification.total_events,
        breaks=verification.breaks,
    )
