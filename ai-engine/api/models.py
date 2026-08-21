"""
Pydantic models for the GrowthLabs AI web API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AuditStatus(BaseModel):
    """Status of an audit job."""
    audit_id: str
    status: str = Field(description="pending | processing | completed | failed")
    progress: int = Field(ge=0, le=100, description="Progress percentage")
    created_at: str
    completed_at: Optional[str] = None
    client_name: str
    error: Optional[str] = None


class AuditUploadResponse(BaseModel):
    """Response after uploading files and triggering an audit."""
    audit_id: str
    status: str = "pending"
    message: str = "Files received. Audit queued."
    transactions_file: str
    customers_file: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    error_code: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    version: str = "1.0.0"
    engine_loaded: bool = True