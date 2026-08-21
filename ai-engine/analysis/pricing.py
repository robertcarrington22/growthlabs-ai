"""
Pricing analysis module.
Analyzes pricing effectiveness, tier distribution, and margin estimation.
"""

import pandas as pd
import numpy as np
from typing import Optional


def analyze_pricing(
    transactions: pd.DataFrame,
    customers: pd.DataFrame,
) -> dict:
    """
    Analyze pricing structure, effectiveness, and opportunities.

    Args:
        transactions: DataFrame with columns: date, amount, quantity, service_name, estimated_margin_pct
        customers: DataFrame with customer metadata

    Returns:
        dict with pricing analysis results
    """
    if len(transactions) == 0:
        return {"error": "No transaction data provided"}

    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]

    # ── Average Order Value (AOV) Analysis ──
    aov_overall = round(df["total_amount"].mean(), 2)
    aov_median = round(df["total_amount"].median(), 2)

    # AOV by month
    df["month"] = df["date"].dt.to_period("M")
    aov_by_month = df.groupby("month").agg(
        aov=("total_amount", "mean"),
        median_amount=("total_amount", "median"),
        transaction_count=("transaction_id", "count"),
    ).reset_index()
    aov_by_month["month_str"] = aov_by_month["month"].astype(str)
    aov_by_month = aov_by_month.sort_values("month")

    # AOV trend
    aov_trend = [
        {
            "period": row["month_str"],
            "avg_order_value": round(row["aov"], 2),
            "median_order_value": round(row["median_amount"], 2),
            "transaction_count": int(row["transaction_count"]),
        }
        for _, row in aov_by_month.iterrows()
    ]

    # AOV stability (coefficient of variation)
    aov_cv = round(df["total_amount"].std() / df["total_amount"].mean() * 100, 1) if df["total_amount"].mean() > 0 else 0

    # ── Pricing Tier Distribution ──
    # Define tiers based on transaction total
    def price_tier(amount):
        if amount < 100:
            return "Budget (<$100)"
        elif amount < 500:
            return "Standard ($100–$499)"
        elif amount < 2000:
            return "Premium ($500–$1,999)"
        elif amount < 10000:
            return "Enterprise ($2K–$9,999)"
        else:
            return "Strategic ($10K+)"

    df["tier"] = df["total_amount"].apply(price_tier)

    tier_distribution = (
        df.groupby("tier")
        .agg(
            transaction_count=("transaction_id", "count"),
            total_revenue=("total_amount", "sum"),
            avg_amount=("total_amount", "mean"),
        )
        .reset_index()
        .sort_values("avg_amount", ascending=False)
    )

    total_rev = tier_distribution["total_revenue"].sum()
    tier_distribution["revenue_share_pct"] = round(
        tier_distribution["total_revenue"] / total_rev * 100, 1
    ) if total_rev > 0 else 0

    tiers = [
        {
            "tier": row["tier"],
            "transaction_count": int(row["transaction_count"]),
            "total_revenue": round(row["total_revenue"], 2),
            "revenue_share_pct": row["revenue_share_pct"],
            "avg_amount": round(row["avg_amount"], 2),
        }
        for _, row in tier_distribution.iterrows()
    ]

    # ── Service/Product Mix ──
    service_mix = (
        df.groupby("service_name")
        .agg(
            transaction_count=("transaction_id", "count"),
            total_revenue=("total_amount", "sum"),
            avg_amount=("total_amount", "mean"),
            median_amount=("total_amount", "median"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )

    service_mix["revenue_share_pct"] = round(
        service_mix["total_revenue"] / service_mix["total_revenue"].sum() * 100, 1
    )

    services = [
        {
            "service": row["service_name"],
            "transaction_count": int(row["transaction_count"]),
            "total_revenue": round(row["total_revenue"], 2),
            "revenue_share_pct": row["revenue_share_pct"],
            "avg_amount": round(row["avg_amount"], 2),
            "median_amount": round(row["median_amount"], 2),
        }
        for _, row in service_mix.iterrows()
    ]

    # ── Margin Analysis ──
    if "estimated_margin_pct" in df.columns and df["estimated_margin_pct"].notna().any():
        margin_data = df.dropna(subset=["estimated_margin_pct"])
        avg_margin = round(margin_data["estimated_margin_pct"].mean(), 1)
        margin_by_service = (
            margin_data.groupby("service_name")
            .agg(
                avg_margin=("estimated_margin_pct", "mean"),
                total_revenue=("total_amount", "sum"),
            )
            .reset_index()
            .sort_values("total_revenue", ascending=False)
        )

        margin_analysis = {
            "overall_avg_margin_pct": avg_margin,
            "margin_by_service": [
                {
                    "service": row["service_name"],
                    "avg_margin_pct": round(row["avg_margin"], 1),
                    "total_revenue": round(row["total_revenue"], 2),
                }
                for _, row in margin_by_service.iterrows()
            ],
        }

        # Revenue-weighted margin
        weighted_margin = round(
            (margin_data["estimated_margin_pct"] * margin_data["total_amount"]).sum()
            / margin_data["total_amount"].sum(),
            1,
        ) if margin_data["total_amount"].sum() > 0 else 0
        margin_analysis["revenue_weighted_margin_pct"] = weighted_margin
    else:
        margin_analysis = None

    # ── Price Dispersion ──
    # For services with many transactions, check price variability
    price_dispersion = []
    for svc in df["service_name"].unique():
        svc_data = df[df["service_name"] == svc]
        if len(svc_data) >= 5:
            prices = svc_data["total_amount"]
            cv = round(prices.std() / prices.mean() * 100, 1) if prices.mean() > 0 else 0
            price_dispersion.append({
                "service": svc,
                "min_price": round(prices.min(), 2),
                "max_price": round(prices.max(), 2),
                "avg_price": round(prices.mean(), 2),
                "median_price": round(prices.median(), 2),
                "coefficient_of_variation_pct": cv,
            })

    # ── Cross-Sell / Upsell Indicators ──
    # Count distinct services per customer
    customer_services = df.groupby("customer_id")["service_name"].nunique().reset_index()
    customer_services.columns = ["customer_id", "distinct_services"]

    single_service_customers = (customer_services["distinct_services"] == 1).sum()
    multi_service_customers = (customer_services["distinct_services"] >= 2).sum()
    total_cust = len(customer_services)

    cross_sell_metrics = {
        "pct_single_service_customers": round(single_service_customers / total_cust * 100, 1) if total_cust > 0 else 0,
        "pct_multi_service_customers": round(multi_service_customers / total_cust * 100, 1) if total_cust > 0 else 0,
        "avg_services_per_customer": round(customer_services["distinct_services"].mean(), 1),
    }

    result = {
        "summary": {
            "overall_aov": aov_overall,
            "median_aov": aov_median,
            "aov_coefficient_of_variation_pct": aov_cv,
            "total_services_offered": len(services),
            "avg_services_per_customer": cross_sell_metrics["avg_services_per_customer"],
        },
        "aov_trend": aov_trend,
        "pricing_tiers": tiers,
        "service_mix": services,
        "margin_analysis": margin_analysis,
        "price_dispersion": price_dispersion,
        "cross_sell_indicators": cross_sell_metrics,
        "key_findings": _generate_pricing_findings(
            tiers, services, margin_analysis, cross_sell_metrics, aov_overall, aov_cv, price_dispersion
        ),
    }

    return result


def _generate_pricing_findings(
    tiers: list[dict],
    services: list[dict],
    margin_analysis: Optional[dict],
    cross_sell: dict,
    aov: float,
    aov_cv: float,
    price_dispersion: list[dict],
) -> list[dict]:
    """Generate findings from pricing analysis."""
    findings = []

    # Revenue concentration in tiers
    if tiers:
        top_tier = tiers[0]  # Highest avg amount
        if top_tier["revenue_share_pct"] > 50 and top_tier["transaction_count"] < 100:
            findings.append({
                "type": "opportunity",
                "area": "tier_concentration",
                "finding": f"'{top_tier['tier']}' tier dominates at {top_tier['revenue_share_pct']:.0f}% of revenue but only {top_tier['transaction_count']} transactions.",
                "recommendation": "Develop mid-tier offerings to capture customers who can't yet afford the top tier.",
            })

    # Upsell opportunity
    single_pct = cross_sell.get("pct_single_service_customers", 0)
    if single_pct > 60:
        findings.append({
            "type": "opportunity",
            "area": "upsell_potential",
            "finding": f"{single_pct:.0f}% of customers buy only one service — significant upsell opportunity.",
            "recommendation": "Create bundled packages and train sales team on cross-sell paths between services.",
        })
    elif single_pct > 40:
        findings.append({
            "type": "opportunity",
            "area": "upsell_potential",
            "finding": f"{single_pct:.0f}% of customers are single-service — moderate upsell opportunity.",
            "recommendation": "Introduce service bundles with a small discount to encourage multi-service adoption.",
        })

    # Margin insight
    if margin_analysis:
        weighted = margin_analysis.get("revenue_weighted_margin_pct", 0)
        avg_margin = margin_analysis.get("overall_avg_margin_pct", 0)
        if weighted > 0 and weighted < 25:
            findings.append({
                "type": "warning",
                "area": "margin_pressure",
                "finding": f"Weighted average margin is {weighted:.0f}% — on the lower end.",
                "recommendation": "Review cost structure for top revenue services. Consider price adjustments for low-margin offerings.",
            })

        # Low-margin high-revenue services
        margin_by_svc = margin_analysis.get("margin_by_service", [])
        if margin_by_svc:
            low_margin_high_rev = [s for s in margin_by_svc if s["avg_margin_pct"] < 25 and s["total_revenue"] > 10000]
            for item in low_margin_high_rev:
                findings.append({
                    "type": "warning",
                    "area": "margin_leak",
                    "finding": f"'{item['service']}' generates ${item['total_revenue']:,.0f} revenue but only {item['avg_margin_pct']:.0f}% margin — revenue is masking inefficiency.",
                    "recommendation": "Audit delivery costs for this service. Consider automation, scoping improvements, or price increase.",
                })

    # Price dispersion
    if price_dispersion:
        high_var = [s for s in price_dispersion if s["coefficient_of_variation_pct"] > 40]
        for item in high_var:
            findings.append({
                "type": "warning",
                "area": "price_inconsistency",
                "finding": f"'{item['service']}' shows high price variability (CV: {item['coefficient_of_variation_pct']:.0f}%), ranging from ${item['min_price']:,.0f} to ${item['max_price']:,.0f}.",
                "recommendation": "Standardize pricing tiers or implement discount governance to preserve margin.",
            })

    return findings
