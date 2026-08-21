#!/usr/bin/env bash
"""
GrowthLabs AI — API Integration Test Script
Tests all 4 API endpoints end-to-end with sample data.

Usage:
    # Start the API server first (in another terminal):
    source .venv/bin/activate && uvicorn api.server:app --host 0.0.0.0 --port 8000

    # Then run this script:
    bash api/test_api.sh

    # Or with a custom host/api key:
    API_HOST=http://localhost:8000 API_KEY=my-key bash api/test_api.sh
"""

set -euo pipefail

API_HOST="${API_HOST:-http://localhost:8000}"
API_KEY="${API_KEY:-gl-dev-key-change-in-production}"
TXNS="${1:-sample_data/transactions.csv}"
CUST="${2:-sample_data/customers.csv}"
PASS=0
FAIL=0

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

pass() { PASS=$((PASS+1)); echo -e "  ${GREEN}✓${NC} $1"; }
fail() { FAIL=$((FAIL+1)); echo -e "  ${RED}✗${NC} $1"; }

echo "========================================"
echo " GrowthLabs AI — API Test Suite"
echo " Host: $API_HOST"
echo "========================================"
echo ""

# ── 1. Health Check ───────────────────────────────────────────────
echo "[1/4] Testing GET /health..."
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "$API_HOST/health")
if [ "$HEALTH" = "200" ]; then
    BODY=$(curl -s "$API_HOST/health")
    if echo "$BODY" | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['status']=='ok'" 2>/dev/null; then
        pass "Health check returned 200 with status=ok"
    else
        fail "Health check body invalid: $BODY"
    fi
else
    fail "Health check returned $HEALTH (expected 200)"
fi

# ── 2. Upload ──────────────────────────────────────────────────────
echo "[2/4] Testing POST /api/audit/upload..."
UPLOAD=$(curl -s -w "\n%{http_code}" -X POST "$API_HOST/api/audit/upload" \
    -H "X-API-Key: $API_KEY" \
    -F "transactions=@$TXNS" \
    -F "customers=@$CUST" \
    -F "client_name=API Test")
HTTP_CODE=$(echo "$UPLOAD" | tail -1)
BODY=$(echo "$UPLOAD" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    AUDIT_ID=$(echo "$BODY" | python3 -c "import json,sys; print(json.load(sys.stdin)['audit_id'])" 2>/dev/null || echo "")
    if [ -n "$AUDIT_ID" ]; then
        pass "Upload returned 200 with audit_id=$AUDIT_ID"
    else
        fail "Upload response missing audit_id: $BODY"
    fi
else
    fail "Upload returned $HTTP_CODE (expected 200)"
    echo "  Body: $BODY"
    echo "  Tip: Is the API server running? Is the API key correct?"
    echo ""
    echo "Results: $PASS passed, $FAIL failed"
    exit 1
fi

# ── 3. Status (poll until complete) ────────────────────────────────
echo "[3/4] Testing GET /api/audit/{id}/status..."
for i in $(seq 1 30); do
    STATUS_JSON=$(curl -s "$API_HOST/api/audit/$AUDIT_ID/status" -H "X-API-Key: $API_KEY")
    STATUS=$(echo "$STATUS_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['status'])" 2>/dev/null || echo "error")
    PROGRESS=$(echo "$STATUS_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['progress'])" 2>/dev/null || echo "0")
    
    if [ "$STATUS" = "completed" ]; then
        pass "Audit completed (${PROGRESS}%) after ~${i}s"
        break
    elif [ "$STATUS" = "failed" ]; then
        ERROR=$(echo "$STATUS_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('error','unknown'))")
        fail "Audit failed: $ERROR"
        break
    fi
    sleep 1
done

if [ "$STATUS" != "completed" ] && [ "$STATUS" != "failed" ]; then
    fail "Audit did not complete within 30s (status=$STATUS)"
fi

# ── 4. Report ──────────────────────────────────────────────────────
echo "[4/4] Testing GET /api/audit/{id}/report..."
HTTP_CODE=$(curl -s -o /tmp/audit_report.json -w "%{http_code}" \
    "$API_HOST/api/audit/$AUDIT_ID/report" -H "X-API-Key: $API_KEY")

if [ "$HTTP_CODE" = "200" ]; then
    # Validate report structure
    python3 -c "
import json
with open('/tmp/audit_report.json') as f:
    r = json.load(f)
assert 'executive_summary' in r, 'Missing executive_summary'
assert 'revenue_analysis' in r, 'Missing revenue_analysis'
assert 'customer_analysis' in r, 'Missing customer_analysis'
assert 'pricing_analysis' in r, 'Missing pricing_analysis'
assert 'all_findings' in r, 'Missing all_findings'
assert 'top_recommendations' in r, 'Missing top_recommendations'
es = r['executive_summary']
assert es['client'] == 'API Test', f'Wrong client: {es[\"client\"]}'
assert es['key_metrics']['total_revenue_analyzed'] > 0, 'Zero revenue'
assert len(r['all_findings']) > 0, 'No findings'
print(f'Client: {es[\"client\"]}')
print(f'Revenue: €{es[\"key_metrics\"][\"total_revenue_analyzed\"]:,.2f}')
print(f'Findings: {len(r[\"all_findings\"])}')
print(f'Recommendations: {len(r[\"top_recommendations\"])}')
" && pass "Report returned 200 with valid structure" || fail "Report validation failed"
else
    fail "Report returned $HTTP_CODE (expected 200)"
    cat /tmp/audit_report.json 2>/dev/null | head -c 200 || true
fi

# ── Summary ────────────────────────────────────────────────────────
echo ""
echo "========================================"
echo " Results: $PASS passed, $FAIL failed"
echo "========================================"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi