# GrowthLabs AI — Revenue Analysis Engine

AI-powered revenue analysis engine for the GrowthLabs AI **Discovery Audit** service. Analyzes small business data to uncover pricing inefficiencies, customer churn patterns, underperforming channels, and untapped upsell opportunities.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with synthetic sample data
python main.py --sample

# Or specify your own CSV data
python main.py --transactions data/transactions.csv --customers data/customers.csv

# Specify client name and output location
python main.py --sample --client "Acme Corp" --output acme_report.json
```

## Output

A structured JSON report is saved with:
- **Executive Summary** — key metrics and finding overview
- **Revenue Analysis** — monthly/quarterly trends, growth rates, seasonality
- **Customer Analysis** — segments, cohort retention, churn indicators, CLV estimates
- **Pricing Analysis** — AOV trends, tier distribution, margin analysis, upsell indicators
- **Top Recommendations** — prioritized action items with findings

## Architecture

```
ai-engine/
├── main.py                      # CLI entry point
├── data_ingestion.py            # CSV loading & normalization
├── sample_data_generator.py     # Synthetic data for testing
├── report_generator.py          # JSON report builder
├── requirements.txt             # Python dependencies
├── analysis/
│   ├── revenue_trends.py        # Revenue & growth analysis
│   ├── customer_segments.py     # Customer & churn analysis
│   └── pricing.py               # Pricing & margin analysis
└── README.md
```

## Analysis Modules

### Revenue Trends
- Monthly and quarterly revenue trends
- Growth rate calculations (MoM, QoQ, YoY)
- Seasonality detection
- Revenue concentration risk

### Customer Segments
- RFM-based customer segmentation (Champion, Loyal, High Value, At Risk, etc.)
- Cohort retention analysis
- Churn indicators and at-risk identification
- Customer Lifetime Value (CLV) estimates
- Channel and industry breakdowns

### Pricing
- Average Order Value (AOV) trends and stability
- Pricing tier distribution
- Service/product mix analysis
- Margin analysis (overall and by service)
- Price dispersion and cross-sell indicators

## Data Format

### transactions.csv
| Column | Required | Description |
|--------|----------|-------------|
| `transaction_id` | ✅ | Unique transaction identifier |
| `customer_id` | ✅ | Customer identifier (matches customers.csv) |
| `date` | ✅ | Transaction date (YYYY-MM-DD) |
| `amount` | ✅ | Transaction amount (numeric) |
| `quantity` | ❌ | Quantity (defaults to 1) |
| `service_name` | ❌ | Product/service name |
| `estimated_margin_pct` | ❌ | Estimated margin percentage |

### customers.csv
| Column | Description |
|--------|-------------|
| `customer_id` | Unique customer identifier |
| `company_name` | Customer company name |
| `industry` | Industry vertical |
| `acquisition_channel` | Marketing channel acquired from |
| `acquisition_date` | Date customer was acquired |
| `churn_date` | Date customer churned (if applicable) |
| `is_churned` | Whether the customer has churned |
| `annual_revenue` | Customer's annual revenue |
| `employees` | Number of employees |

## Dependencies

- pandas >= 2.0.0
- numpy >= 1.24.0

## Sample Data

Run `python main.py --sample` to generate 200 customers and 5,000 transactions across 8 industry verticals with realistic pricing and churn patterns. Generated data is stored in `sample_data/`.

## Customization

Each analysis module (`analysis/`) can be used independently:

```python
from data_ingestion import load_data
from analysis.revenue_trends import analyze_revenue_trends

ingested = load_data("transactions.csv")
results = analyze_revenue_trends(ingested.transactions)
```

## Web API

A FastAPI web server wraps the engine for programmatic access. The website, external dashboards, or CI pipelines can trigger audits and retrieve results via HTTP.

### Running the API

```bash
# Activate the virtual environment
source .venv/bin/activate

# Start the API server (dev mode with auto-reload)
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload

# Or via Docker
docker build -t growthlabs-api .
docker run -p 8000:8000 -e GROWTHLABS_API_KEY="your-secret-key" growthlabs-api
```

### Authentication

All `/api/` endpoints require an API key passed via the `X-API-Key` header.

**Default dev key:** `gl-dev-key-change-in-production`
**Override:** Set the `GROWTHLABS_API_KEY` environment variable.

### Endpoints

#### `GET /health`

Health check. No auth required.

```bash
curl http://localhost:8000/health
```

Response:
```json
{ "status": "ok", "version": "1.0.0", "engine_loaded": true }
```

#### `POST /api/audit/upload`

Upload CSV files and trigger a revenue analysis audit.

```bash
curl -X POST http://localhost:8000/api/audit/upload \
  -H "X-API-Key: gl-dev-key-change-in-production" \
  -F "transactions=@sample_data/transactions.csv" \
  -F "customers=@sample_data/customers.csv" \
  -F "client_name=Acme Corp"
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `transactions` | CSV file | ✅ | Transaction data (see format below) |
| `customers` | CSV file | ❌ | Customer metadata |
| `client_name` | string | ❌ | Name for the report (default: "Client Business") |

Response:
```json
{
  "audit_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Files received. Analysis started in background.",
  "transactions_file": "transactions.csv",
  "customers_file": "customers.csv"
}
```

#### `GET /api/audit/{audit_id}/status`

Check the progress of an audit.

```bash
curl http://localhost:8000/api/audit/550e8400-e29b-41d4-a716-446655440000/status \
  -H "X-API-Key: gl-dev-key-change-in-production"
```

Response:
```json
{
  "audit_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 50,
  "created_at": "2026-07-07T20:55:00+00:00",
  "completed_at": null,
  "client_name": "Acme Corp",
  "error": null
}
```

#### `GET /api/audit/{audit_id}/report`

Get the complete JSON report for a completed audit.

```bash
curl http://localhost:8000/api/audit/550e8400-e29b-41d4-a716-446655440000/report \
  -H "X-API-Key: gl-dev-key-change-in-production"
```

Returns the full structured report (see [Output](#output) section for schema details). Returns `425 Too Early` if the audit is still processing, or `500` if it failed.

### Quick Test Script

```bash
# Start the API
source .venv/bin/activate
uvicorn api.server:app --host 0.0.0.0 --port 8000 &

# Wait for startup
sleep 2

# Health check
curl http://localhost:8000/health

# Run an audit with sample data
curl -X POST http://localhost:8000/api/audit/upload \
  -H "X-API-Key: gl-dev-key-change-in-production" \
  -F "transactions=@sample_data/transactions.csv" \
  -F "customers=@sample_data/customers.csv" \
  -F "client_name=Demo Client" > /tmp/upload.json

# Get the audit ID
AUDIT_ID=$(python3 -c "import json; print(json.load(open('/tmp/upload.json'))['audit_id'])")

# Poll until completed
while true; do
  STATUS=$(curl -s "http://localhost:8000/api/audit/$AUDIT_ID/status" -H "X-API-Key: gl-dev-key-change-in-production" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['status'], d['progress'])")
  echo "Status: $STATUS"
  echo "$STATUS" | grep -q "completed" && break
  sleep 1
done

# Get the report
curl "http://localhost:8000/api/audit/$AUDIT_ID/report" -H "X-API-Key: gl-dev-key-change-in-production" | python3 -m json.tool | head -30
