"""
Recommendation engine for GrowthLabs AI.
Enriches analysis findings with dollar-quantified impact estimates,
confidence levels, effort levels, and ranks them by expected impact.

This is the critical P7 deliverable — bridging the gap between
descriptive analytics and a client-ready revenue growth plan.
"""

import math
from typing import Any


# ── Impact Estimation Rules ───────────────────────────────────────
# Each finding area maps to a quantification strategy

IMPACT_RULES = {
    "revenue_growth": {
        "pct_range": (0.03, 0.10),
        "basis": "total_revenue",
        "description": "Accelerating growth rate to capture additional revenue",
        "confidence": "medium",
        "effort": "high",
    },
    "churn_risk": {
        "pct_range": (0.03, 0.08),
        "basis": "at_risk_revenue",
        "description": "Reducing churn through proactive retention",
        "confidence": "medium",
        "effort": "medium",
    },
    "customer_concentration": {
        "pct_range": (0.02, 0.05),
        "basis": "total_revenue",
        "description": "Diversifying customer base to reduce concentration risk",
        "confidence": "low",
        "effort": "high",
    },
    "margin_leak": {
        "pct_range": (0.02, 0.08),
        "basis": "service_revenue",
        "description": "Improving margins on low-margin high-revenue services",
        "confidence": "medium",
        "effort": "medium",
    },
    "margin_pressure": {
        "pct_range": (0.02, 0.05),
        "basis": "total_revenue",
        "description": "Addressing overall margin compression through price/cost adjustments",
        "confidence": "medium",
        "effort": "medium",
    },
    "price_inconsistency": {
        "pct_range": (0.01, 0.05),
        "basis": "total_revenue",
        "description": "Standardizing pricing to capture revenue lost to inconsistent discounting",
        "confidence": "high",
        "effort": "low",
    },
    "channel_quality": {
        "pct_range": (0.02, 0.06),
        "basis": "total_revenue",
        "description": "Optimizing channel mix to improve customer quality and retention",
        "confidence": "medium",
        "effort": "medium",
    },
    "upsell_potential": {
        "pct_range": (0.03, 0.12),
        "basis": "total_revenue",
        "description": "Capturing upsell and cross-sell revenue from existing customers",
        "confidence": "medium",
        "effort": "low",
    },
    "ticket_size": {
        "pct_range": (0.02, 0.08),
        "basis": "total_revenue",
        "description": "Increasing average transaction value through bundling and tiering",
        "confidence": "high",
        "effort": "low",
    },
    "clv_gap": {
        "pct_range": (0.01, 0.04),
        "basis": "total_revenue",
        "description": "Closing the gap between top-tier and bottom-tier customer value",
        "confidence": "low",
        "effort": "high",
    },
}


def _get_basis_amount(report: dict, basis: str, finding: dict) -> float:
    """Get the dollar basis for impact calculation."""
    metrics = report.get("executive_summary", {}).get("key_metrics", {})
    total_rev = metrics.get("total_revenue_analyzed", 0)

    if basis == "total_revenue":
        return total_rev
    elif basis == "at_risk_revenue":
        # Try to get at-risk revenue from customer analysis
        cust = report.get("customer_analysis", {})
        return cust.get("summary", {}).get("churn_risk_revenue_at_risk", total_rev * 0.15)
    elif basis == "service_revenue":
        # For margin leaks, estimate from relevant service
        return total_rev * 0.3  # Rough estimate
    return total_rev


def quantify_finding(report: dict, finding: dict) -> dict:
    """
    Enrich a finding with dollar impact estimate, confidence, and effort.

    Returns:
        dict with finding + impact fields
    """
    area = finding.get("area", "")
    rule = IMPACT_RULES.get(area)

    if not rule:
        # Generic fallback
        return {
            **finding,
            "estimated_annual_impact_low": 0,
            "estimated_annual_impact_mid": 0,
            "estimated_annual_impact_high": 0,
            "impact_arithmetic": "Could not quantify — insufficient data pattern",
            "confidence": "low",
            "effort": "medium",
            "is_quantified": False,
        }

    basis_amount = _get_basis_amount(report, rule["basis"], finding)
    pct_low, pct_high = rule["pct_range"]
    pct_mid = (pct_low + pct_high) / 2

    impact_low = round(basis_amount * pct_low)
    impact_mid = round(basis_amount * pct_mid)
    impact_high = round(basis_amount * pct_high)

    # Build arithmetic explanation
    if rule["basis"] == "total_revenue":
        arithmetic = (
            f"${basis_amount:,.0f} (total revenue) × {pct_low*100:.1f}–{pct_high*100:.1f}% "
            f"= ${impact_low:,}–${impact_high:,}/year"
        )
    elif rule["basis"] == "at_risk_revenue":
        arithmetic = (
            f"${basis_amount:,.0f} (at-risk revenue) × {pct_low*100:.1f}–{pct_high*100:.1f}% "
            f"= ${impact_low:,}–${impact_high:,}/year"
        )
    else:
        arithmetic = (
            f"${basis_amount:,.0f} (estimated applicable revenue) × {pct_low*100:.1f}–{pct_high*100:.1f}% "
            f"= ${impact_low:,}–${impact_high:,}/year"
        )

    return {
        **finding,
        "estimated_annual_impact_low": impact_low,
        "estimated_annual_impact_mid": impact_mid,
        "estimated_annual_impact_high": impact_high,
        "impact_arithmetic": arithmetic,
        "confidence": rule["confidence"],
        "effort": rule["effort"],
        "is_quantified": True,
        "recommendation_action": rule["description"],
    }


def build_recommendations(report: dict) -> dict:
    """
    Build full ranked recommendation layer.

    Args:
        report: Full audit report dictionary

    Returns:
        dict with quantified_findings, total_opportunity, rankings
    """
    raw_findings = report.get("all_findings", [])

    # Quantify every finding
    quantified = [quantify_finding(report, f) for f in raw_findings]

    # Re-map types: all actionable findings become "opportunity" for taxonomy fix (D5.3)
    for qf in quantified:
        if qf["is_quantified"] and qf.get("type") in ("warning",):
            qf["type"] = "opportunity"

    # Rank by midpoint impact (descending)
    ranked = sorted(quantified, key=lambda x: x.get("estimated_annual_impact_mid", 0), reverse=True)

    # Calculate total opportunity value
    total_opportunity_low = sum(f.get("estimated_annual_impact_low", 0) for f in ranked if f.get("is_quantified"))
    total_opportunity_mid = sum(f.get("estimated_annual_impact_mid", 0) for f in ranked if f.get("is_quantified"))
    total_opportunity_high = sum(f.get("estimated_annual_impact_high", 0) for f in ranked if f.get("is_quantified"))

    # Get top 10
    top_10 = [f for f in ranked if f.get("is_quantified")][:10]

    # Build summary
    metrics = report.get("executive_summary", {}).get("key_metrics", {})
    total_rev = metrics.get("total_revenue_analyzed", 0)

    opportunity_pct_low = round(total_opportunity_low / total_rev * 100, 1) if total_rev > 0 else 0
    opportunity_pct_mid = round(total_opportunity_mid / total_rev * 100, 1) if total_rev > 0 else 0
    opportunity_pct_high = round(total_opportunity_high / total_rev * 100, 1) if total_rev > 0 else 0

    return {
        "total_opportunity_low": total_opportunity_low,
        "total_opportunity_mid": total_opportunity_mid,
        "total_opportunity_high": total_opportunity_high,
        "total_opportunity_pct_low": opportunity_pct_low,
        "total_opportunity_pct_mid": opportunity_pct_mid,
        "total_opportunity_pct_high": opportunity_pct_high,
        "quantified_finding_count": sum(1 for f in ranked if f.get("is_quantified")),
        "ranked_findings_10": top_10,
        "all_findings_ranked": ranked,
    }


def format_opportunity_summary(recommendations: dict) -> str:
    """Format the recommendation summary for the report."""
    lines = [
        "## 💰 Revenue Opportunity Summary",
        "",
        f"**Total Identified Opportunity:** ${recommendations['total_opportunity_mid']:,}/year",
        f"(Range: ${recommendations['total_opportunity_low']:,} – ${recommendations['total_opportunity_high']:,}/year)",
        f"({recommendations['total_opportunity_pct_mid']}% of current revenue)",
        "",
        f"**Quantified Findings:** {recommendations['quantified_finding_count']}",
        "",
        "### Top 10 Ranked Opportunities",
        "",
        "| # | Area | Est. Annual Impact | Confidence | Effort |",
        "|---|------|-------------------|------------|--------|",
    ]
    for i, f in enumerate(recommendations["ranked_findings_10"], 1):
        area = f.get("area", "").replace("_", " ").title()
        impact = f"${f.get('estimated_annual_impact_mid', 0):,}"
        conf = f.get("confidence", "medium").title()
        effort = f.get("effort", "medium").title()
        lines.append(f"| {i} | {area} | {impact} | {conf} | {effort} |")

    lines.append("")
    lines.append("### How These Are Calculated")
    for i, f in enumerate(recommendations["ranked_findings_10"][:5], 1):
        lines.append(f"**{i}. {f.get('area', '').replace('_', ' ').title()}**")
        lines.append(f"- Finding: {f.get('finding', '')}")
        lines.append(f"- Action: {f.get('recommendation_action', f.get('recommendation', ''))}")
        lines.append(f"- Calculation: {f.get('impact_arithmetic', 'N/A')}")
        lines.append("")

    return "\n".join(lines)