# GrowthLabs AI — Revenue Analysis Engine
# Multi-stage: build deps in a venv, then copy to runtime

FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# ── Runtime stage ──────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Copy the virtualenv from builder
COPY --from=builder /venv /venv

# Copy application code
COPY . .

# Use the venv's python
ENV PATH="/venv/bin:$PATH"

# Default API key (override in production)
ENV GROWTHLABS_API_KEY="gl-dev-key-change-in-production"

# Port
EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]