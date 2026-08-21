"""
GrowthLabs AI — Revenue Analysis Web API

A lightweight FastAPI server that wraps the analysis engine for programmatic access.

Run with:
    source .venv/bin/activate
    uvicorn api.server:app --host 0.0.0.0 --port 8000

Endpoints:
    GET  /health               — Health check
    POST /api/audit/upload     — Upload CSVs and trigger analysis
    GET  /api/audit/{id}/status — Check audit progress
    GET  /api/audit/{id}/report — Get the complete JSON report
    GET  /api/audit/{id}/summary — Get a human-readable summary (markdown)
"""

import json
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

# ── Engine imports ─────────────────────────────────────────────────
import sys

# Ensure the engine root is on the path
API_DIR = Path(__file__).parent.resolve()
ENGINE_DIR = API_DIR.parent
sys.path.insert(0, str(ENGINE_DIR))

from data_ingestion import load_data
from analysis.revenue_trends import analyze_revenue_trends
from analysis.customer_segments import analyze_customer_segments
from analysis.pricing import analyze_pricing
from report_generator import generate_report, save_report
from nlp_summary import generate_full_summary

# ── API imports ────────────────────────────────────────────────────
from api.auth import verify_api_key
from api.models import AuditStatus, AuditUploadResponse, ErrorResponse, HealthResponse

# ── App setup ──────────────────────────────────────────────────────
app = FastAPI(
    title="GrowthLabs AI — Revenue Analysis API",
    description="AI-powered revenue analysis for Discovery Audits. Upload transaction data and get a structured report with growth opportunities.",
    version="1.0.0",
)

# CORS — allow the website (port 3000) to call us, plus dev origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://f69074b6f79359de24090350c8743e0c.ctonew.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Data directories ───────────────────────────────────────────────
UPLOAD_DIR = ENGINE_DIR / "api" / "uploads"
REPORTS_DIR = ENGINE_DIR / "api" / "reports"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# In-memory audit registry (will be persisted to disk for restarts)
AUDITS_FILE = API_DIR / "audits.json"
audits: dict[str, dict] = {}

if AUDITS_FILE.exists():
    try:
        audits = json.loads(AUDITS_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        audits = {}


def _save_audits():
    """Persist the audit registry to disk."""
    AUDITS_FILE.write_text(json.dumps(audits, indent=2, default=str))


def _run_analysis(audit_id: str, txn_path: str, cust_path: Optional[str], client_name: str):
    """Run the full analysis pipeline and update the audit record."""
    try:
        audits[audit_id]["status"] = "processing"
        audits[audit_id]["progress"] = 10
        _save_audits()

        # Step 1: Ingest
        ingested = load_data(txn_path, cust_path)
        if not ingested.is_valid:
            raise ValueError(f"Data validation failed: {ingested.validation_errors}")

        audits[audit_id]["progress"] = 30
        _save_audits()

        # Step 2: Revenue trends
        revenue = analyze_revenue_trends(ingested.transactions)

        audits[audit_id]["progress"] = 50
        _save_audits()

        # Step 3: Customer segments
        customer = analyze_customer_segments(ingested.transactions, ingested.customers)

        audits[audit_id]["progress"] = 70
        _save_audits()

        # Step 4: Pricing analysis
        pricing = analyze_pricing(ingested.transactions, ingested.customers)

        audits[audit_id]["progress"] = 85
        _save_audits()

        # Step 5: Generate report
        report = generate_report(
            revenue_analysis=revenue,
            customer_analysis=customer,
            pricing_analysis=pricing,
            ingestion_summary=ingested.summary(),
            client_name=client_name,
        )

        report_path = str(REPORTS_DIR / f"{audit_id}.json")
        save_report(report, report_path)

        audits[audit_id]["status"] = "completed"
        audits[audit_id]["progress"] = 100
        audits[audit_id]["completed_at"] = datetime.now(timezone.utc).isoformat()
        audits[audit_id]["report_path"] = report_path
        _save_audits()

    except Exception as e:
        audits[audit_id]["status"] = "failed"
        audits[audit_id]["error"] = str(e)
        audits[audit_id]["progress"] = 0
        _save_audits()


# ── Endpoints ──────────────────────────────────────────────────────


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check — confirms the API is running and the engine is loaded."""
    return HealthResponse(
        status="ok",
        version="1.0.0",
        engine_loaded=True,
    )


@app.post(
    "/api/audit/upload",
    response_model=AuditUploadResponse,
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
    tags=["Audit"],
)
async def upload_audit(
    transactions: UploadFile = File(..., description="CSV file with transaction data"),
    customers: Optional[UploadFile] = File(None, description="Optional CSV file with customer data"),
    client_name: str = Form("Client Business", description="Name of the client for the report"),
    _: str = Depends(verify_api_key),
):
    """
    Upload CSV files and trigger a revenue analysis audit.

    - **transactions**: CSV with columns: transaction_id, customer_id, date, amount (required), service_name, quantity, estimated_margin_pct
    - **customers**: CSV with columns: customer_id, company_name, industry, acquisition_channel, acquisition_date, churn_date, is_churned, annual_revenue, employees
    - **client_name**: Name to use in the generated report
    """
    # Validate file types
    if not transactions.filename or not transactions.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transactions file must be a CSV.",
        )
    if customers and customers.filename and not customers.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customers file must be a CSV.",
        )

    # Generate audit ID
    audit_id = str(uuid.uuid4())
    audit_dir = UPLOAD_DIR / audit_id
    audit_dir.mkdir(parents=True, exist_ok=True)

    # Save uploaded files
    txn_path = str(audit_dir / "transactions.csv")
    with open(txn_path, "wb") as f:
        shutil.copyfileobj(transactions.file, f)

    cust_path = None
    if customers:
        cust_path = str(audit_dir / "customers.csv")
        with open(cust_path, "wb") as f:
            shutil.copyfileobj(customers.file, f)

    # Register the audit
    now = datetime.now(timezone.utc).isoformat()
    audits[audit_id] = {
        "audit_id": audit_id,
        "status": "pending",
        "progress": 0,
        "created_at": now,
        "completed_at": None,
        "client_name": client_name,
        "txn_path": txn_path,
        "cust_path": cust_path,
        "error": None,
        "report_path": None,
    }
    _save_audits()

    # Kick off analysis in background
    import threading
    thread = threading.Thread(
        target=_run_analysis,
        args=(audit_id, txn_path, cust_path, client_name),
        daemon=True,
    )
    thread.start()

    return AuditUploadResponse(
        audit_id=audit_id,
        status="pending",
        message="Files received. Analysis started in background.",
        transactions_file=transactions.filename or "transactions.csv",
        customers_file=customers.filename if customers else None,
    )


@app.get(
    "/api/audit/{audit_id}/status",
    response_model=AuditStatus,
    responses={404: {"model": ErrorResponse}},
    tags=["Audit"],
)
async def get_audit_status(
    audit_id: str,
    _: str = Depends(verify_api_key),
):
    """Check the status and progress of an audit."""
    audit = audits.get(audit_id)
    if audit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit '{audit_id}' not found.",
        )

    return AuditStatus(
        audit_id=audit["audit_id"],
        status=audit["status"],
        progress=audit["progress"],
        created_at=audit["created_at"],
        completed_at=audit.get("completed_at"),
        client_name=audit["client_name"],
        error=audit.get("error"),
    )


@app.get(
    "/api/audit/{audit_id}/report",
    responses={
        200: {"description": "The full audit report as JSON"},
        404: {"model": ErrorResponse},
        425: {"model": ErrorResponse, "description": "Audit not yet completed"},
    },
    tags=["Audit"],
)
async def get_audit_report(
    audit_id: str,
    _: str = Depends(verify_api_key),
):
    """Get the complete JSON report for a completed audit."""
    audit = audits.get(audit_id)
    if audit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit '{audit_id}' not found.",
        )

    if audit["status"] == "pending" or audit["status"] == "processing":
        raise HTTPException(
            status_code=status.HTTP_425_TOO_EARLY,
            detail=f"Audit is still {audit['status']}. Check status endpoint.",
        )

    if audit["status"] == "failed":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audit failed: {audit.get('error', 'Unknown error')}",
        )

    report_path = audit.get("report_path")
    if not report_path or not os.path.exists(report_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found on disk.",
        )

    with open(report_path) as f:
        report = json.load(f)

    return report


@app.get(
    "/api/audit/{audit_id}/summary",
    responses={
        200: {"description": "Human-readable audit summary (markdown)"},
        404: {"model": ErrorResponse},
        425: {"model": ErrorResponse, "description": "Audit not yet completed"},
    },
    tags=["Audit"],
)
async def get_audit_summary(
    audit_id: str,
    format: str = "markdown",
    _: str = Depends(verify_api_key),
):
    """
    Get a human-readable summary of the audit report.

    - **format**: Output format — 'markdown' (default) or 'html'
    """
    audit = audits.get(audit_id)
    if audit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit '{audit_id}' not found.",
        )

    if audit["status"] == "pending" or audit["status"] == "processing":
        raise HTTPException(
            status_code=status.HTTP_425_TOO_EARLY,
            detail=f"Audit is still {audit['status']}. Check status endpoint.",
        )

    if audit["status"] == "failed":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Audit failed: {audit.get('error', 'Unknown error')}",
        )

    report_path = audit.get("report_path")
    if not report_path or not os.path.exists(report_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found on disk.",
        )

    with open(report_path) as f:
        report = json.load(f)

    # Validate format parameter
    if format not in ("markdown", "html"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Format must be 'markdown' or 'html'.",
        )

    summary = generate_full_summary(report, output_format=format)

    return {"summary": summary, "format": format}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)