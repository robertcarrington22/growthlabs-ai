"""
Report generator for GrowthLabs AI Revenue Analysis Engine.
Produces a structured JSON report suitable for client deliverables.
"""

import json
import pandas as pd
from typing import Optional
from datetime import datetime

from pricing_proposal import calculate_retainer, format_retainer_summary
from recommendation_engine import build_recommendations, format_opportunity_summary


def generate_report(
    revenue_analysis: dict,
    customer_analysis: dict,
    pricing_analysis: dict,
    ingestion_summary: dict,
    client_name: str = "Sample Business",
    report_date: Optional[str] = None,
    annual_revenue: Optional[float] = None,
    industry_analysis: Optional[dict] = None,
    maturity_assessment: Optional[dict] = None,
    causal_loops: Optional[dict] = None,
    pattern_matches: Optional[list[dict]] = None,
    pattern_summary: Optional[dict] = None,
) -> dict:
    """
    Generate a structured JSON report combining all analysis modules.

    Args:
        revenue_analysis: Output from revenue_trends.analyze_revenue_trends()
        customer_analysis: Output from customer_segments.analyze_customer_segments()
        pricing_analysis: Output from pricing.analyze_pricing()
        ingestion_summary: Summary from data ingestion
        client_name: Name of the client business
        report_date: ISO date string for the report

    Returns:
        dict with full report structure
    """
    if report_date is None:
        report_date = datetime.now().strftime("%Y-%m-%d")

    # ── Aggregate all findings ──
    all_findings = []

    # Collect from each module
    for module_name, module_data in [
        ("revenue_trends", revenue_analysis),
        ("customer_segments", customer_analysis),
        ("pricing", pricing_analysis),
    ]:
        if "key_findings" in module_data:
            for f in module_data["key_findings"]:
                f["module"] = module_name
                all_findings.append(f)

    # Sort by severity
    severity_order = {"negative": 0, "warning": 1, "opportunity": 2, "neutral": 3, "positive": 4}
    all_findings.sort(key=lambda x: (severity_order.get(x.get("type", "neutral"), 5), x.get("area", "")))

    # ── Executive Summary ──
    total_revenue = (
        revenue_analysis.get("summary", {}).get("total_revenue", 0)
        if "error" not in revenue_analysis
        else 0
    )
    total_customers = (
        customer_analysis.get("summary", {}).get("total_customers", 0)
        if "error" not in customer_analysis
        else 0
    )
    aov = (
        pricing_analysis.get("summary", {}).get("overall_aov", 0)
        if "error" not in pricing_analysis
        else 0
    )

    # Count findings by type
    positive = len([f for f in all_findings if f.get("type") == "positive"])
    warnings = len([f for f in all_findings if f.get("type") == "warning"])
    negatives = len([f for f in all_findings if f.get("type") == "negative"])
    opportunities = len([f for f in all_findings if f.get("type") == "opportunity"])

    executive_summary = {
        "client": client_name,
        "report_date": report_date,
        "analysis_period": revenue_analysis.get("summary", {}).get("date_range", {}),
        "key_metrics": {
            "total_revenue_analyzed": total_revenue,
            "total_customers_analyzed": total_customers,
            "overall_aov": aov,
            "transactions_analyzed": revenue_analysis.get("summary", {}).get("total_transactions", 0),
            "data_quality_warnings": len(ingestion_summary.get("warnings", [])),
        },
        "finding_summary": {
            "total_findings": len(all_findings),
            "critical_issues": negatives,
            "warnings": warnings,
            "opportunities": opportunities,
            "positive_signals": positive,
        },
    }

    # ── Top Recommendations (prioritized) ──
    top_recs = []
    for f in all_findings:
        if "recommendation" in f:
            top_recs.append({
                "priority": "high"
                if f.get("type") in ("negative", "warning")
                else "medium"
                if f.get("type") == "opportunity"
                else "low",
                "area": f.get("area", ""),
                "finding": f.get("finding", ""),
                "recommendation": f["recommendation"],
                "module": f.get("module", ""),
            })

    # ── Build quantified recommendations (P7) ──
    temp_report = {
        "executive_summary": executive_summary,
        "revenue_analysis": revenue_analysis,
        "customer_analysis": customer_analysis,
        "pricing_analysis": pricing_analysis,
        "all_findings": all_findings,
    }
    recommendations = build_recommendations(temp_report)
    quantified_findings = recommendations.get("all_findings_ranked", all_findings)
    opportunity_summary = format_opportunity_summary(recommendations)

    # Update the finding_summary with opportunity counts
    total_opportunities = recommendations.get("quantified_finding_count", 0)
    executive_summary["finding_summary"]["opportunities"] = total_opportunities
    executive_summary["finding_summary"]["total_opportunity_value_mid"] = recommendations.get("total_opportunity_mid", 0)
    executive_summary["finding_summary"]["total_opportunity_value_range"] = (
        recommendations.get("total_opportunity_low", 0),
        recommendations.get("total_opportunity_high", 0),
    )

    # ── Assemble Report ──
    report = {
        "report_metadata": {
            "title": f"GrowthLabs AI — Revenue Discovery Audit: {client_name}",
            "client": client_name,
            "report_date": report_date,
            "engine_version": "1.0.0",
            "generated_by": "GrowthLabs AI Revenue Analysis Engine",
        },
        "executive_summary": executive_summary,
        "data_quality": {
            "records_loaded": ingestion_summary,
            "issues": ingestion_summary.get("validation_errors", []) + ingestion_summary.get("warnings", []),
        },
        "revenue_analysis": revenue_analysis if "error" not in revenue_analysis else {"error": revenue_analysis["error"]},
        "customer_analysis": customer_analysis if "error" not in customer_analysis else {"error": customer_analysis["error"]},
        "pricing_analysis": pricing_analysis if "error" not in pricing_analysis else {"error": pricing_analysis["error"]},
        "pricing_proposal": calculate_retainer({"executive_summary": executive_summary, "revenue_analysis": revenue_analysis, "customer_analysis": customer_analysis, "pricing_analysis": pricing_analysis, "all_findings": all_findings}, annual_revenue),
        "industry_analysis": industry_analysis if industry_analysis else None,
        "maturity_assessment": maturity_assessment if maturity_assessment else None,
        "causal_loops": causal_loops if causal_loops else None,
        "pattern_library": {
            "matches": pattern_matches if pattern_matches else [],
            "summary": pattern_summary if pattern_summary else {"total": 0},
        } if pattern_matches else None,
        "recommendations": recommendations,
        "top_recommendations": top_recs[:10],  # Top 10
        "all_findings": quantified_findings,  # Ranked + quantified (P7)
    }

    return report


def save_report(report: dict, filepath: str) -> str:
    """
    Save report to a JSON file with pretty formatting.

    Args:
        report: Report dictionary
        filepath: Path to write the JSON file

    Returns:
        The path the report was saved to
    """
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"📄 Report saved to: {filepath}")
    return filepath


def print_report_summary(report: dict):
    """Print a human-readable summary of the report to stdout."""
    meta = report.get("report_metadata", {})
    summary = report.get("executive_summary", {})

    print("=" * 70)
    print(f"  GROWTHLABS AI — REVENUE DISCOVERY AUDIT")
    print(f"  {meta.get('client', 'N/A')}")
    print(f"  Report Date: {meta.get('report_date', 'N/A')}")
    print("=" * 70)

    metrics = summary.get("key_metrics", {})
    print(f"\n📊 KEY METRICS")
    print(f"  Total Revenue:        ${metrics.get('total_revenue_analyzed', 0):,.2f}")
    print(f"  Total Customers:      {metrics.get('total_customers_analyzed', 0)}")
    print(f"  Average Order Value:  ${metrics.get('overall_aov', 0):,.2f}")
    print(f"  Transactions:         {metrics.get('transactions_analyzed', 0)}")

    findings = summary.get("finding_summary", {})
    print(f"\n🔍 FINDINGS OVERVIEW")
    print(f"  🟢 Positive:   {findings.get('positive_signals', 0)}")
    print(f"  🟡 Warnings:   {findings.get('warnings', 0)}")
    print(f"  🔴 Critical:   {findings.get('critical_issues', 0)}")
    print(f"  💡 Opportunity: {findings.get('opportunities', 0)}")

    recs = report.get("top_recommendations", [])
    if recs:
        print(f"\n🎯 TOP RECOMMENDATIONS")
        for i, rec in enumerate(recs[:5], 1):
            priority_icon = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "🟢"
            print(f"\n  {i}. {priority_icon} [{rec['priority'].upper()}] {rec['area']}")
            print(f"     {rec['finding'][:100]}...")
            print(f"     → {rec['recommendation']}")

    print(f"\n{'=' * 70}")
    print(f"  Full report saved with all details and data tables.")
    print(f"{'=' * 70}")
