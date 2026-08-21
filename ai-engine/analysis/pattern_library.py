"""
Pattern Library of Revenue Gaps for GrowthLabs AI.
A lookup table of known revenue gap patterns that the engine can flag
when it sees matching data patterns in client data.
"""

from typing import Any


# Each pattern has:
# - id: unique identifier
# - name: human-readable name
# - category: pricing, churn, channel, upsell, operations
# - severity: low, medium, high, critical
# - description: what this pattern looks like
# - data_triggers: what data conditions trigger this pattern
# - typical_impact: estimated revenue impact range
# - recommendation: what to do about it
# - industries: which industries it applies to (None = all)

PATTERNS = [
    # ── Pricing Patterns ──
    {
        "id": "PRICE-001",
        "name": "Flat Pricing Across All Customers",
        "category": "pricing",
        "severity": "high",
        "description": "All customers pay approximately the same price regardless of service tier, volume, or value received. This indicates cost-plus or one-size-fits-all pricing.",
        "data_triggers": {
            "condition": "price_cv < 15",
            "metrics": {"price_cv": "Coefficient of variation of transaction amounts"},
        },
        "typical_impact": "5-15% revenue leakage",
        "recommendation": "Introduce tiered pricing based on value delivered. Analyze customer willingness to pay by segment and create 3-4 pricing tiers.",
        "industries": None,
    },
    {
        "id": "PRICE-002",
        "name": "No Price Increases Over Time",
        "category": "pricing",
        "severity": "medium",
        "description": "Average transaction value has remained flat or declined over 12+ months, indicating prices haven't kept pace with inflation or value delivered.",
        "data_triggers": {
            "condition": "aov_trend < 0 and months_of_data >= 12",
            "metrics": {"aov_trend": "AOV month-over-month growth rate", "months_of_data": "Months of transaction history"},
        },
        "typical_impact": "3-7% annual erosion",
        "recommendation": "Implement annual price increases (3-10% depending on market). Consider grandfathering existing clients and raising prices for new business.",
        "industries": None,
    },
    {
        "id": "PRICE-003",
        "name": "High Price Variability Without Structure",
        "category": "pricing",
        "severity": "medium",
        "description": "Prices for the same service vary widely (CV > 40%), suggesting inconsistent discounting, ad-hoc pricing, or lack of price governance.",
        "data_triggers": {
            "condition": "price_cv > 40",
            "metrics": {"price_cv": "Coefficient of variation of same-service prices"},
        },
        "typical_impact": "2-8% margin loss",
        "recommendation": "Standardize pricing with clear discount governance. Define approval levels for discounts and track discounting patterns by salesperson.",
        "industries": None,
    },
    {
        "id": "PRICE-004",
        "name": "Low-Margin Services Driving Revenue",
        "category": "pricing",
        "severity": "high",
        "description": "The highest-revenue services have the lowest margins. Revenue is masking inefficiency — the business is working harder for less profit.",
        "data_triggers": {
            "condition": "has_margin_data and low_margin_high_rev_exists",
            "metrics": {"margin_revenue_correlation": "Correlation between revenue and margin by service"},
        },
        "typical_impact": "10-20% margin recovery opportunity",
        "recommendation": "Audit delivery costs for top revenue services. Consider price increases, scope tightening, or delivery automation for low-margin high-revenue services.",
        "industries": ["professional_services", "consulting", "digital_agency"],
    },
    # ── Churn Patterns ──
    {
        "id": "CHURN-001",
        "name": "High Share of One-Time Customers",
        "category": "churn",
        "severity": "high",
        "description": "A large percentage of customers make only one purchase and never return. This indicates poor onboarding, low engagement, or unmet expectations.",
        "data_triggers": {
            "condition": "one_time_pct > 50",
            "metrics": {"one_time_pct": "Percentage of customers with exactly one transaction"},
        },
        "typical_impact": "15-30% revenue at risk",
        "recommendation": "Implement a structured onboarding process for new customers. Define 'first 30 days' milestones and track activation metrics.",
        "industries": None,
    },
    {
        "id": "CHURN-002",
        "name": "Long Gaps Between Purchases",
        "category": "churn",
        "severity": "medium",
        "description": "Customers have long gaps between purchases (90+ days between transactions), suggesting low engagement and high churn risk.",
        "data_triggers": {
            "condition": "avg_days_between_purchases > 90",
            "metrics": {"avg_days_between_purchases": "Average days between customer transactions"},
        },
        "typical_impact": "10-20% annual churn increase",
        "recommendation": "Create re-engagement campaigns for customers who haven't purchased in 60+ days. Consider subscription or retainer models to increase purchase frequency.",
        "industries": None,
    },
    {
        "id": "CHURN-003",
        "name": "Declining Average Transaction Value Per Customer",
        "category": "churn",
        "severity": "medium",
        "description": "Customers' average transaction values are declining over time, indicating they're buying less or downgrading — a leading churn indicator.",
        "data_triggers": {
            "condition": "customer_aov_trend_declining",
            "metrics": {"customer_aov_trend": "Trend in average transaction value per customer over time"},
        },
        "typical_impact": "Leading indicator — 20-40% churn risk within 6 months",
        "recommendation": "Flag customers with declining AOV for proactive outreach. Offer value-add services or check-in calls to understand changing needs.",
        "industries": None,
    },
    # ── Channel Patterns ──
    {
        "id": "CHNL-001",
        "name": "Over-Reliance on One Channel",
        "category": "channel",
        "severity": "high",
        "description": "More than 60% of customers come from a single acquisition channel, creating concentration risk.",
        "data_triggers": {
            "condition": "top_channel_share > 60",
            "metrics": {"top_channel_share": "Percentage of customers from the top acquisition channel"},
        },
        "typical_impact": "High risk — 20-40% revenue at risk if channel dries up",
        "recommendation": "Diversify acquisition channels. Test 2-3 new channels at small scale. Aim for no single channel exceeding 40% of new customers.",
        "industries": None,
    },
    {
        "id": "CHNL-002",
        "name": "High Churn from Specific Channel",
        "category": "channel",
        "severity": "medium",
        "description": "Customers acquired from certain channels have significantly higher churn rates than others, indicating poor lead quality or misaligned messaging.",
        "data_triggers": {
            "condition": "channel_churn_variance > 20",
            "metrics": {"channel_churn_variance": "Difference in churn rate between best and worst channel"},
        },
        "typical_impact": "15-25% improvement in customer quality through channel optimization",
        "recommendation": "Review lead quality by channel. Adjust targeting, messaging, or qualification criteria for high-churn channels. Consider reducing spend on worst-performing channels.",
        "industries": None,
    },
    # ── Upsell Patterns ──
    {
        "id": "UPSELL-001",
        "name": "Single-Service Customers",
        "category": "upsell",
        "severity": "medium",
        "description": "Majority of customers buy only one service, indicating significant untapped cross-sell and upsell potential.",
        "data_triggers": {
            "condition": "single_service_pct > 60",
            "metrics": {"single_service_pct": "Percentage of customers who buy only one service"},
        },
        "typical_impact": "15-30% additional revenue from existing customers",
        "recommendation": "Create bundled service packages with a small discount. Train sales team on cross-sell paths between services. Implement post-purchase follow-up sequences.",
        "industries": None,
    },
    {
        "id": "UPSELL-002",
        "name": "No Revenue Growth from Existing Customers",
        "category": "upsell",
        "severity": "medium",
        "description": "Existing customers' revenue is flat or declining, with no expansion revenue from upsells or cross-sells.",
        "data_triggers": {
            "condition": "expansion_rate < 5",
            "metrics": {"expansion_rate": "Percentage of revenue from upsells/cross-sells to existing customers"},
        },
        "typical_impact": "20-35% revenue gap vs. best-in-class",
        "recommendation": "Implement a systematic account management process. Set quarterly business reviews with top customers. Create upgrade paths from basic to premium offerings.",
        "industries": None,
    },
    # ── Operations Patterns ──
    {
        "id": "OPS-001",
        "name": "Customer Concentration Risk",
        "category": "operations",
        "severity": "critical",
        "description": "Top 3 customers represent more than 40% of total revenue. Losing any one would be a significant revenue event.",
        "data_triggers": {
            "condition": "top3_concentration > 40",
            "metrics": {"top3_concentration": "Revenue share of top 3 customers"},
        },
        "typical_impact": "Critical — 40%+ revenue at risk from customer loss",
        "recommendation": "Diversify customer base. Set a maximum of 15-20% revenue from any single customer. Develop contingency plans for top customers.",
        "industries": ["b2b", "manufacturing", "distribution"],
    },
    {
        "id": "OPS-002",
        "name": "High Revenue Volatility",
        "category": "operations",
        "severity": "high",
        "description": "Monthly revenue varies significantly (CV > 50%), indicating unpredictable cash flow and lack of recurring revenue.",
        "data_triggers": {
            "condition": "revenue_cv > 50",
            "metrics": {"revenue_cv": "Coefficient of variation of monthly revenue"},
        },
        "typical_impact": "Cash flow instability — 20-40% planning difficulty",
        "recommendation": "Build recurring revenue streams (retainers, subscriptions, maintenance contracts). Create a revenue forecasting process based on pipeline and historical patterns.",
        "industries": None,
    },
    {
        "id": "OPS-003",
        "name": "Scope Creep / Unbilled Work",
        "category": "operations",
        "severity": "medium",
        "description": "Transactions for the same customer vary significantly in amount, suggesting scope creep, unbilled overages, or inconsistent pricing.",
        "data_triggers": {
            "condition": "scope_creep_events > 0",
            "metrics": {"scope_creep_events": "Number of transactions exceeding expected range"},
        },
        "typical_impact": "5-20% revenue leakage from unbilled work",
        "recommendation": "Implement clear scope-of-work agreements with change order processes. Track billable vs. non-billable hours. Send mid-project budget updates to clients.",
        "industries": ["professional_services", "consulting", "digital_agency"],
    },
]


def match_patterns(report: dict) -> list[dict]:
    """
    Match patterns from the library against audit report data.

    Args:
        report: The full audit report dictionary

    Returns:
        List of matched patterns with evidence
    """
    revenue = report.get("revenue_analysis", {})
    customer = report.get("customer_analysis", {})
    pricing = report.get("pricing_analysis", {})
    industry = report.get("industry_analysis", {}).get("industry_detected", "generic")

    matched = []

    for pattern in PATTERNS:
        # Check industry filter
        if pattern["industries"] is not None and industry not in pattern["industries"]:
            continue

        trigger = pattern["data_triggers"]["condition"]
        evidence = _check_trigger(trigger, revenue, customer, pricing, report)

        if evidence is not None:
            matched.append({
                "pattern_id": pattern["id"],
                "name": pattern["name"],
                "category": pattern["category"],
                "severity": pattern["severity"],
                "description": pattern["description"],
                "evidence": evidence,
                "typical_impact": pattern["typical_impact"],
                "recommendation": pattern["recommendation"],
            })

    # Sort by severity
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    matched.sort(key=lambda x: severity_order.get(x["severity"], 4))

    return matched


def _check_trigger(condition: str, revenue: dict, customer: dict, pricing: dict, report: dict) -> Any:
    """Check a trigger condition against the data. Returns evidence string or None."""
    try:
        if condition == "price_cv < 15":
            cv = pricing.get("summary", {}).get("aov_coefficient_of_variation_pct", 100)
            if cv < 15:
                return f"Price CV is {cv}% — all transactions cluster around the same value"
            return None

        elif condition == "aov_trend < 0 and months_of_data >= 12":
            aov_trend = None
            trend = pricing.get("aov_trend", [])
            if len(trend) >= 3:
                first = trend[0].get("avg_order_value", 0)
                last = trend[-1].get("avg_order_value", 0)
                if first > 0:
                    aov_trend = (last - first) / first * 100
            if aov_trend is not None and aov_trend < 0:
                return f"AOV declined {abs(aov_trend):.1f}% over {len(trend)} months"
            return None

        elif condition == "price_cv > 40":
            # Check per-service price dispersion
            dispersion = pricing.get("price_dispersion", [])
            high_var = [d for d in dispersion if d.get("coefficient_of_variation_pct", 0) > 40]
            if high_var:
                return f"High price variability in {len(high_var)} services: {', '.join(d['service'] for d in high_var[:3])}"
            return None

        elif condition == "has_margin_data and low_margin_high_rev_exists":
            margin = pricing.get("margin_analysis", {})
            if margin and margin.get("overall_avg_margin_pct", 0) > 0:
                by_svc = margin.get("margin_by_service", [])
                low_high = [s for s in by_svc if s.get("avg_margin_pct", 100) < 25 and s.get("total_revenue", 0) > 10000]
                if low_high:
                    return f"Low-margin/high-revenue: {', '.join(s['service'] for s in low_high[:3])}"
            return None

        elif condition == "one_time_pct > 50":
            segments = customer.get("segment_summary", [])
            total_cust = customer.get("summary", {}).get("total_customers", 0)
            # Use segment data to estimate one-time customers
            return None  # Requires more data than currently available

        elif condition == "avg_days_between_purchases > 90":
            segment = customer.get("segment_summary", [])
            for s in segment:
                if s.get("segment") == "At Risk" and s.get("avg_days_since_last_purchase", 0) > 90:
                    return f"At-risk segment: {s['avg_days_since_last_purchase']:.0f} days since last purchase"
            return None

        elif condition == "customer_aov_trend_declining":
            return None  # Requires per-customer trend analysis

        elif condition == "top_channel_share > 60":
            churn_ch = customer.get("churn_by_channel", [])
            # If we have channel data, use it
            return None

        elif condition == "channel_churn_variance > 20":
            churn_ch = customer.get("churn_by_channel", [])
            if churn_ch and len(churn_ch) > 1:
                counts = [c.get("lost_customers", 0) for c in churn_ch]
                if max(counts) - min(counts) > 20:
                    return f"Churn varies significantly: {churn_ch[0]['acquisition_channel']} ({counts[0]}) vs {churn_ch[-1]['acquisition_channel']} ({counts[-1]})"
            return None

        elif condition == "single_service_pct > 60":
            xsell = pricing.get("cross_sell_indicators", {})
            pct = xsell.get("pct_single_service_customers", 0)
            if pct > 60:
                return f"{pct}% of customers buy only one service"
            return None

        elif condition == "expansion_rate < 5":
            expansion = xsell.get("pct_multi_service_customers", 0) if "xsell" in dir() else 0
            return None

        elif condition == "top3_concentration > 40":
            conc = revenue.get("concentration", {})
            top3 = conc.get("top_3_months_share_pct", 0)
            if top3 > 40:
                return f"Top 3 months: {top3}% of total revenue"
            return None

        elif condition == "revenue_cv > 50":
            monthly_growth = revenue.get("monthly_growth_rates", {})
            vol = monthly_growth.get("volatility_pct", 0)
            if vol > 50:
                return f"Monthly revenue volatility: {vol}%"
            return None

        elif condition == "scope_creep_events > 0":
            ia = report.get("industry_analysis", {})
            if ia.get("scope_creep_events", 0) > 0:
                return f"{ia['scope_creep_events']} scope creep events detected"
            return None

        return None
    except Exception:
        return None


def get_pattern_summary(matched: list[dict]) -> dict:
    """Summarize matched patterns."""
    if not matched:
        return {"total": 0, "by_severity": {}, "top_patterns": []}

    by_severity = {}
    for p in matched:
        s = p["severity"]
        by_severity[s] = by_severity.get(s, 0) + 1

    return {
        "total": len(matched),
        "by_severity": by_severity,
        "top_patterns": [{"name": p["name"], "severity": p["severity"], "impact": p["typical_impact"]} for p in matched[:5]],
    }