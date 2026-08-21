"""
API key authentication for the GrowthLabs AI web API.
Supports Bearer token auth via the X-API-Key header.
"""

import os
import secrets
from fastapi import Header, HTTPException, status
from typing import Optional

# Default API key — override via GROWTHLABS_API_KEY env var
# In production, always set this via environment variable
DEFAULT_API_KEY = "gl-dev-key-change-in-production"

# Set via environment or use default
API_KEY = os.environ.get("GROWTHLABS_API_KEY", DEFAULT_API_KEY)

# Store a secure hash for comparison to prevent timing attacks
# We use secrets.compare_digest for constant-time comparison


def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Dependency for FastAPI routes. Validates the API key from the X-API-Key header.

    Usage:
        @router.get("/protected")
        async def protected_route(auth: str = Depends(verify_api_key)):
            ...
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Provide it via the X-API-Key header.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )

    return x_api_key