"""
Natural-language summary generator for GrowthLabs AI audit reports.
Converts structured JSON reports into client-ready executive summaries
using template-based natural language generation (no external LLM API).
"""

import json
from typing import Optional
from pricing_proposal import calculate_retainer, format_retainer_summary


def _fmt_eur(amount: float) -> str:
    """Format a number as a readable EUR string."""
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:,.1f}M"
    elif amount >= 1_000:
        return f"${amount:,.0f}"
    return f"${amount:.2f}"


def _describe_growth(growth_pct: float) -> str:
    """Describe a growth rate in natural language."""
    if growth_pct > 10:
        return "strong"
    elif growth_pct > 5:
        return "healthy"
    elif growth_pct > 2:
        return "moderate"
    elif growth_pct > 0:
        return "modest"
    elif growth_pct > -5:
        return "slightly declining"
    else:
        return "concerning"


def generate_executive_summary(report: dict) -> str:
    """
    Generate a 2-3 paragraph executive summary from the audit report.

    Args:
        report: The full audit report dictionary

    Returns:
        A multi-paragraph natural-language executive summary
    """
    meta = report.get("report_metadata", {})
    summary = report.get("executive_summary", {})
    metrics = summary.get("key_metrics", {})
    findings = summary.get("finding_summary", {})
    revenue_analysis = report.get("revenue_analysis", {})
    customer_analysis = report.get("customer_analysis", {})
    pricing_analysis = report.get("pricing_analysis", {})

    client_name = meta.get("client", "Client")
    total_rev = metrics.get("total_revenue_analyzed", 0)
    total_customers = metrics.get("total_customers_analyzed", 0)
    total_txns = metrics.get("transactions_analyzed", 0)
    aov = metrics.get("overall_aov", 0)

    # Growth context
    rev_summary = revenue_analysis.get("summary", {})
    monthly_growth = revenue_analysis.get("monthly_growth_rates", {})
    avg_growth = monthly_growth.get("average_growth_rate_pct", 0)
    months = rev_summary.get("months_of_data", 0)

    # Customer context
    cust_summary = customer_analysis.get("summary", {})
    active = cust_summary.get("active_customers", 0)
    at_risk = cust_summary.get("at_risk_customers", 0)
    churn_pct = cust_summary.get("churn_risk_pct", 0)

    # Pricing context
    price_summary = pricing_analysis.get("summary", {})
    services_count = price_summary.get("total_services_offered", 0)
    avg_services = price_summary.get("avg_services_per_customer", 0)

    # Finding counts
    critical = findings.get("critical_issues", 0)
    warnings = findings.get("warnings", 0)
    opportunities = findings.get("opportunities", 0)

    growth_desc = _describe_growth(avg_growth)

    # ── Paragraph 1: Overview ──
    p1 = (
        f"**{client_name}** completed a GrowthLabs AI Revenue Discovery Audit covering "
        f"**{_fmt_eur(total_rev)}** in revenue across **{total_txns}** transactions from "
        f"**{total_customers}** customers over **{months} months**. "
        f"The business shows **{growth_desc}** revenue momentum "
        f"(avg monthly growth: **{avg_growth:.1f}%**), with an average transaction value of "
        f"**{_fmt_eur(aov)}** and **{services_count}** distinct services offered."
    )

    # ── Paragraph 2: Key findings ──
    p2_parts = ["The analysis identified key areas for attention:"]

    if critical > 0:
        p2_parts.append(
            f"**{critical} critical issue{'s' if critical != 1 else ''}** require immediate action "
            f"to prevent revenue loss."
        )
    if warnings > 0:
        p2_parts.append(
            f"**{warnings} warning{'s' if warnings != 1 else ''}** highlight operational risks "
            f"that should be addressed proactively."
        )
    if opportunities > 0:
        p2_parts.append(
            f"**{opportunities} growth opportunit{'y' if opportunities == 1 else 'ies'}** "
            f"represent untapped revenue potential."
        )

    if churn_pct > 0:
        p2_parts.append(
            f"Customer retention is a key theme — **{at_risk} customers ({churn_pct:.0f}%)** "
            f"show early churn signals, representing at-risk revenue."
        )

    if avg_services < 2:
        p2_parts.append(
            f"Most customers purchase a single service, indicating significant upsell potential."
        )
    elif avg_services > 3:
        p2_parts.append(
            f"Customers engage with an average of **{avg_services:.1f} services**, "
            f"showing strong cross-sell adoption."
        )

    if active > 0:
        pct_active = active / total_customers * 100 if total_customers > 0 else 0
        p2_parts.append(
            f"**{active} customers ({pct_active:.0f}%)** are actively generating revenue."
        )

    p2 = " ".join(p2_parts)

    # ── Paragraph 3: Path forward ──
    recommendations = report.get("top_recommendations", [])
    high_priority = [r for r in recommendations if r.get("priority") == "high"]
    medium_priority = [r for r in recommendations if r.get("priority") == "medium"]

    p3_parts = [
        "Based on these findings, we recommend the following strategic priorities:"
    ]

    for rec in high_priority[:3]:
        p3_parts.append(f"- **{rec['area'].replace('_', ' ').title()}**: {rec['recommendation']}")

    if medium_priority:
        p3_parts.append(
            f"Additionally, **{len(medium_priority)} medium-priority recommendation{'s' if len(medium_priority) != 1 else ''}** "
            f"address secondary optimization opportunities."
        )

    p3_parts.append(
        "Implementing these recommendations in order of priority will "
        "strengthen revenue resilience and unlock sustainable growth."
    )

    p3 = "\n".join(p3_parts)

    return f"{p1}\n\n{p2}\n\n{p3}"


def generate_quick_wins(report: dict, count: int = 3) -> list[dict]:
    """
    Identify the top quick wins from the audit findings.
    Quick wins = high-impact, relatively easy-to-implement findings.

    Args:
        report: The full audit report dictionary
        count: Number of quick wins to return (default: 3)

    Returns:
        List of dicts with 'area', 'finding', 'recommendation', 'potential_impact'
    """
    findings = report.get("all_findings", [])

    # Priority: negative/warning types first, then opportunity
    priority_map = {"negative": 0, "warning": 1, "opportunity": 2, "neutral": 3, "positive": 4}

    # Score each finding as a quick win
    scored = []
    for f in findings:
        score = 0
        # Negative/warnings are most urgent
        score += (4 - priority_map.get(f.get("type", "neutral"), 5)) * 10
        # Specific areas that are typically quick to fix
        quick_areas = ["churn_risk", "price_inconsistency", "channel_quality", "upsell_potential", "ticket_size"]
        if f.get("area") in quick_areas:
            score += 5
        # Shorter findings tend to be more actionable
        if len(f.get("recommendation", "")) < 120:
            score += 3

        scored.append((score, f))

    scored.sort(key=lambda x: x[0], reverse=True)

    quick_wins = []
    for _, f in scored[:count]:
        quick_wins.append({
            "area": f.get("area", "").replace("_", " ").title(),
            "finding": f.get("finding", ""),
            "recommendation": f.get("recommendation", ""),
            "potential_impact": _estimate_quick_win_impact(f, report),
        })

    return quick_wins


def _estimate_quick_win_impact(finding: dict, report: dict) -> str:
    """Estimate the potential revenue impact of a specific finding."""
    area = finding.get("area", "")
    f_type = finding.get("type", "")
    metrics = report.get("executive_summary", {}).get("key_metrics", {})
    total_rev = metrics.get("total_revenue_analyzed", 0)

    if area == "churn_risk":
        customer_analysis = report.get("customer_analysis", {})
        at_risk_rev = customer_analysis.get("summary", {}).get("churn_risk_revenue_at_risk", 0)
        if at_risk_rev > 0:
            potential = at_risk_rev * 0.3  # Assume 30% retention improvement
            return f"Preserving **{_fmt_eur(potential)}** of at-risk revenue ({_fmt_eur(at_risk_rev)} at risk)"
        return "Reducing churn by 10-20% through targeted re-engagement"

    elif area == "upsell_potential":
        single_svc_pct = report.get("pricing_analysis", {}).get("cross_sell_indicators", {}).get("pct_single_service_customers", 0)
        if single_svc_pct > 0 and total_rev > 0:
            potential = total_rev * (single_svc_pct / 100) * 0.15  # 15% uplift from cross-sell
            return f"Up to **{_fmt_eur(potential)}** in additional revenue from multi-service adoption"
        return "Revenue uplift from cross-selling existing customers"

    elif area == "price_inconsistency":
        return "**5-15% margin improvement** through pricing standardization"

    elif area == "margin_leak":
        return "**10-20% margin recovery** through cost structure optimization"

    elif area == "channel_quality":
        return "**15-25% improvement** in customer quality and retention through channel optimization"

    elif area == "ticket_size":
        return "**10-20% AOV increase** through bundling and tiered pricing"

    elif area == "customer_concentration":
        return "Reduced revenue risk through **customer diversification**"

    elif area == "revenue_growth":
        return "Accelerated growth trajectory through **channel optimization**"

    return "Measurable improvement in revenue performance"


def generate_revenue_impact_estimate(report: dict) -> dict:
    """
    Calculate a combined revenue impact estimate from all findings.

    Returns:
        dict with 'low', 'mid', 'high' estimates and breakdown
    """
    metrics = report.get("executive_summary", {}).get("key_metrics", {})
    total_rev = metrics.get("total_revenue_analyzed", 0)
    findings = report.get("all_findings", [])

    if total_rev == 0:
        return {"low": 0, "mid": 0, "high": 0, "pct_low": 0, "pct_mid": 0, "pct_high": 0}

    # Estimate impact % from each finding type
    impact_ranges = {
        "churn_risk": (0.03, 0.08, 0.15),
        "margin_leak": (0.02, 0.05, 0.10),
        "margin_pressure": (0.02, 0.04, 0.08),
        "upsell_potential": (0.03, 0.07, 0.12),
        "price_inconsistency": (0.01, 0.03, 0.06),
        "channel_quality": (0.02, 0.05, 0.10),
        "revenue_growth": (0.03, 0.08, 0.15),
        "customer_concentration": (0.01, 0.03, 0.05),
        "ticket_size": (0.02, 0.04, 0.08),
    }

    areas_found = set()
    for f in findings:
        area = f.get("area", "")
        if area in impact_ranges:
            areas_found.add(area)

    if not areas_found:
        return {
            "low": round(total_rev * 0.02),
            "mid": round(total_rev * 0.05),
            "high": round(total_rev * 0.10),
            "pct_low": 2,
            "pct_mid": 5,
            "pct_high": 10,
        }

    low_pct = sum(impact_ranges[a][0] for a in areas_found)
    mid_pct = sum(impact_ranges[a][1] for a in areas_found)
    high_pct = sum(impact_ranges[a][2] for a in areas_found)

    # Cap at reasonable total
    low_pct = min(low_pct, 0.25)
    mid_pct = min(mid_pct, 0.35)
    high_pct = min(high_pct, 0.50)

    return {
        "low": round(total_rev * low_pct),
        "mid": round(total_rev * mid_pct),
        "high": round(total_rev * high_pct),
        "pct_low": round(low_pct * 100),
        "pct_mid": round(mid_pct * 100),
        "pct_high": round(high_pct * 100),
        "areas_identified": list(areas_found),
        "area_count": len(areas_found),
    }


def generate_full_summary(report: dict, output_format: str = "markdown") -> str:
    """
    Generate a complete human-readable summary in the specified format.

    Args:
        report: The full audit report dictionary
        output_format: 'markdown' or 'html'

    Returns:
        Formatted summary string
    """
    meta = report.get("report_metadata", {})
    summary = report.get("executive_summary", {})
    metrics = summary.get("key_metrics", {})

    client_name = meta.get("client", "Client")
    report_date = meta.get("report_date", "")
    total_rev = metrics.get("total_revenue_analyzed", 0)

    # Generate components
    exec_summary = generate_executive_summary(report)
    quick_wins = generate_quick_wins(report)
    impact = generate_revenue_impact_estimate(report)

    # Build sections
    sections = []

    # Header
    if output_format == "html":
        sections.append(f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
<h1 style="color: #1a56db;">GrowthLabs AI — Revenue Discovery Audit</h1>
<h2 style="color: #374151;">{client_name}</h2>
<p style="color: #6b7280;">Report Date: {report_date}</p>
<hr style="border: 1px solid #e5e7eb;">""")
    else:
        sections.append(f"# GrowthLabs AI — Revenue Discovery Audit\n## {client_name}\n*Report Date: {report_date}*")
        sections.append("---")

    # Key Metrics Bar
    if output_format == "html":
        sections.append(f"""<div style="display: flex; gap: 16px; margin: 20px 0; flex-wrap: wrap;">
<div style="background: #f3f4f6; padding: 12px 20px; border-radius: 8px; flex: 1; min-width: 140px;">
  <strong style="color: #6b7280; font-size: 12px; text-transform: uppercase;">Revenue Analyzed</strong>
  <div style="font-size: 24px; font-weight: bold; color: #111827;">{_fmt_eur(total_rev)}</div>
</div>
<div style="background: #f3f4f6; padding: 12px 20px; border-radius: 8px; flex: 1; min-width: 140px;">
  <strong style="color: #6b7280; font-size: 12px; text-transform: uppercase;">Customers</strong>
  <div style="font-size: 24px; font-weight: bold; color: #111827;">{metrics.get('total_customers_analyzed', 0)}</div>
</div>
<div style="background: #f3f4f6; padding: 12px 20px; border-radius: 8px; flex: 1; min-width: 140px;">
  <strong style="color: #6b7280; font-size: 12px; text-transform: uppercase;">Transactions</strong>
  <div style="font-size: 24px; font-weight: bold; color: #111827;">{metrics.get('transactions_analyzed', 0)}</div>
</div>
<div style="background: #f3f4f6; padding: 12px 20px; border-radius: 8px; flex: 1; min-width: 140px;">
  <strong style="color: #6b7280; font-size: 12px; text-transform: uppercase;">Avg Order Value</strong>
  <div style="font-size: 24px; font-weight: bold; color: #111827;">{_fmt_eur(metrics.get('overall_aov', 0))}</div>
</div>
</div>""")
    else:
        sections.append(f"**Revenue:** {_fmt_eur(total_rev)} | **Customers:** {metrics.get('total_customers_analyzed', 0)} | **Transactions:** {metrics.get('transactions_analyzed', 0)} | **AOV:** {_fmt_eur(metrics.get('overall_aov', 0))}")

    # Executive Summary
    if output_format == "html":
        sections.append(f'<h3 style="color: #1a56db;">Executive Summary</h3>')
        sections.append(f"<div style='line-height: 1.6;'>{exec_summary.replace('**', '<strong>').replace('**', '</strong>').replace('\n', '<br>')}</div>")
    else:
        sections.append("## Executive Summary")
        sections.append(exec_summary)

    # Top 3 Quick Wins
    sections.append("")
    if output_format == "html":
        sections.append(f'<h3 style="color: #1a56db;">Top 3 Quick Wins</h3>')
        for i, qw in enumerate(quick_wins, 1):
            sections.append(f"""<div style="background: #f0fdf4; border-left: 4px solid #22c55e; padding: 12px 16px; margin: 8px 0; border-radius: 4px;">
<strong style="color: #166534;">Quick Win #{i}: {qw['area']}</strong>
<p style="margin: 4px 0;">{qw['finding']}</p>
<p style="margin: 4px 0; color: #059669;"><strong>→</strong> {qw['recommendation']}</p>
<p style="margin: 4px 0; font-size: 14px; color: #6b7280;">💡 <em>Estimated impact: {qw['potential_impact']}</em></p>
</div>""")
    else:
        sections.append("## 🚀 Top 3 Quick Wins")
        for i, qw in enumerate(quick_wins, 1):
            sections.append(f"### Quick Win #{i}: {qw['area']}")
            sections.append(f"**Finding:** {qw['finding']}")
            sections.append(f"**Recommendation:** {qw['recommendation']}")
            sections.append(f"*💡 Estimated impact: {qw['potential_impact']}*")
            sections.append("")

    # Revenue Impact Estimate
    sections.append("")
    if output_format == "html":
        sections.append(f'<h3 style="color: #1a56db;">Revenue Impact Estimate</h3>')
        sections.append(f"""<div style="background: #fffbeb; border-left: 4px solid #f59e0b; padding: 16px; border-radius: 4px;">
<p style="margin: 0 0 8px 0;">Based on <strong>{impact.get('area_count', 0)} opportunity areas</strong> identified, the estimated annual revenue impact is:</p>
<div style="display: flex; gap: 12px; margin-top: 12px;">
<div style="flex: 1; text-align: center; padding: 8px; background: white; border-radius: 6px;">
  <div style="font-size: 12px; color: #6b7280;">Conservative</div>
  <div style="font-size: 18px; font-weight: bold; color: #059669;">{_fmt_eur(impact.get('low', 0))}</div>
  <div style="font-size: 12px; color: #6b7280;">({impact.get('pct_low', 0)}% of revenue)</div>
</div>
<div style="flex: 1; text-align: center; padding: 8px; background: white; border-radius: 6px;">
  <div style="font-size: 12px; color: #6b7280;">Realistic</div>
  <div style="font-size: 18px; font-weight: bold; color: #ca8a04;">{_fmt_eur(impact.get('mid', 0))}</div>
  <div style="font-size: 12px; color: #6b7280;">({impact.get('pct_mid', 0)}% of revenue)</div>
</div>
<div style="flex: 1; text-align: center; padding: 8px; background: white; border-radius: 6px;">
  <div style="font-size: 12px; color: #6b7280;">Optimistic</div>
  <div style="font-size: 18px; font-weight: bold; color: #dc2626;">{_fmt_eur(impact.get('high', 0))}</div>
  <div style="font-size: 12px; color: #6b7280;">({impact.get('pct_high', 0)}% of revenue)</div>
</div>
</div>
</div>""")
    else:
        sections.append("## 💰 Revenue Impact Estimate")
        sections.append(f"Based on **{impact.get('area_count', 0)} opportunity areas** identified:")
        sections.append(f"| Scenario | Impact | % of Revenue |")
        sections.append(f"|----------|--------|--------------|")
        sections.append(f"| Conservative | {_fmt_eur(impact.get('low', 0))} | {impact.get('pct_low', 0)}% |")
        sections.append(f"| Realistic | {_fmt_eur(impact.get('mid', 0))} | {impact.get('pct_mid', 0)}% |")
        sections.append(f"| Optimistic | {_fmt_eur(impact.get('high', 0))} | {impact.get('pct_high', 0)}% |")

    # ── Retainer Pricing Proposal ──
    sections.append("")
    try:
        proposal = calculate_retainer(report)
        price_lines = format_retainer_summary(proposal).split("\n")
        for line in price_lines:
            sections.append(line)
        sections.append("")
    except Exception:
        pass  # Skip pricing if calculation fails

    # Footer
    if output_format == "html":
        sections.append(f"""<hr style="border: 1px solid #e5e7eb; margin-top: 30px;">
<p style="color: #9ca3af; font-size: 12px; text-align: center;">Generated by GrowthLabs AI Revenue Analysis Engine v{meta.get('engine_version', '1.0.0')}</p>
</div>""")
    else:
        sections.append("")
        sections.append("---")
        sections.append(f"*Generated by GrowthLabs AI Revenue Analysis Engine v{meta.get('engine_version', '1.0.0')}*")

    return "\n\n".join(sections)