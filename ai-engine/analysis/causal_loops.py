"""
The 4 Causal Loops for GrowthLabs AI.
Measures the key reinforcing loops that drive revenue growth:
- Pricing Loop
- Retention Loop
- Acquisition Loop
- Expansion Loop
"""

import pandas as pd
import numpy as np


def calculate_pricing_loop(transactions: pd.DataFrame) -> dict:
    """
    Pricing Loop: pricing power score.

    Formula: AOV trend × margin trend × tier diversity

    Returns score 0-100 and component breakdown.
    """
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]
    df["month"] = df["date"].dt.to_period("M")

    # AOV trend (0-40 points)
    monthly_aov = df.groupby("month")["total_amount"].mean()
    if len(monthly_aov) >= 3:
        aov_growth = (monthly_aov.iloc[-1] - monthly_aov.iloc[0]) / monthly_aov.iloc[0] * 100
        aov_score = min(40, max(0, 20 + aov_growth * 2))
    else:
        aov_score = 20

    # Margin trend (0-30 points)
    if "estimated_margin_pct" in df.columns and df["estimated_margin_pct"].notna().any():
        margin_data = df.dropna(subset=["estimated_margin_pct"])
        monthly_margin = margin_data.groupby("month")["estimated_margin_pct"].mean()
        if len(monthly_margin) >= 3:
            margin_trend = (monthly_margin.iloc[-1] - monthly_margin.iloc[0]) / monthly_margin.iloc[0] * 100
            margin_score = min(30, max(0, 15 + margin_trend))
        else:
            margin_score = 15
    else:
        margin_score = 10  # No margin data = lower score

    # Tier diversity (0-30 points)
    if "service_name" in df.columns:
        unique_services = df["service_name"].nunique()
        tier_score = min(30, unique_services * 3)
    else:
        tier_score = 5

    total = round(aov_score + margin_score + tier_score, 1)

    return {
        "loop_name": "Pricing Loop",
        "description": "Measures pricing power — how effectively the business captures value through pricing strategy",
        "score": total,
        "components": {
            "aov_trend_score": round(aov_score, 1),
            "margin_trend_score": round(margin_score, 1),
            "tier_diversity_score": round(tier_score, 1),
        },
        "aov_trend_pct": round(aov_growth, 1) if len(monthly_aov) >= 3 else 0,
        "interpretation": _interpret_score(total, "pricing"),
    }


def calculate_retention_loop(transactions: pd.DataFrame, customers: pd.DataFrame) -> dict:
    """
    Retention Loop: retention health score.

    Formula: cohort retention × NPS proxy × at-risk share

    Returns score 0-100 and component breakdown.
    """
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]

    # Cohort retention (0-40 points)
    if len(customers) > 0 and "is_churned" in customers.columns:
        churn_rate = customers["is_churned"].mean() * 100
    else:
        last_date = df["date"].max()
        customer_last = df.groupby("customer_id")["date"].max()
        churn_rate = ((last_date - customer_last).dt.days > 180).mean() * 100

    retention_score = min(40, max(0, 40 - churn_rate * 0.8))

    # NPS proxy (0-30 points) — using repeat purchase as proxy
    txn_per_customer = df.groupby("customer_id")["transaction_id"].count()
    repeat_pct = (txn_per_customer > 1).mean() * 100
    nps_score = min(30, repeat_pct * 0.3)

    # At-risk share (0-30 points)
    customer_last = df.groupby("customer_id")["date"].max()
    last_date = df["date"].max()
    days_since_last = (last_date - customer_last).dt.days
    at_risk_pct = ((days_since_last > 90) & (days_since_last <= 180)).mean() * 100
    dormant_pct = (days_since_last > 180).mean() * 100
    at_risk_score = min(30, max(0, 30 - at_risk_pct * 0.3 - dormant_pct * 0.6))

    total = round(retention_score + nps_score + at_risk_score, 1)

    return {
        "loop_name": "Retention Loop",
        "description": "Measures customer retention health — how well the business keeps customers and maintains loyalty",
        "score": total,
        "components": {
            "cohort_retention_score": round(retention_score, 1),
            "nps_proxy_score": round(nps_score, 1),
            "at_risk_management_score": round(at_risk_score, 1),
        },
        "churn_rate_pct": round(churn_rate, 1),
        "repeat_purchase_pct": round(repeat_pct, 1),
        "at_risk_pct": round(at_risk_pct, 1),
        "dormant_pct": round(dormant_pct, 1),
        "interpretation": _interpret_score(total, "retention"),
    }


def calculate_acquisition_loop(transactions: pd.DataFrame, customers: pd.DataFrame) -> dict:
    """
    Acquisition Loop: channel efficiency score.

    Formula: ROI per channel × conversion rate × concentration risk

    Returns score 0-100 and component breakdown.
    """
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]

    # Channel ROI (0-40 points)
    if len(customers) > 0 and "acquisition_channel" in customers.columns:
        cust_rev = df.merge(customers[["customer_id", "acquisition_channel"]], on="customer_id", how="left")
        channel_rev = cust_rev.groupby("acquisition_channel")["total_amount"].sum()
        if len(channel_rev) > 0:
            # More channels with significant revenue = better diversity
            active_channels = (channel_rev > channel_rev.sum() * 0.05).sum()
            channel_score = min(40, active_channels * 8)
        else:
            channel_score = 10
    else:
        channel_score = 10

    # Concentration risk (0-30 points)
    cust_rev = df.groupby("customer_id")["total_amount"].sum().sort_values(ascending=False)
    total_rev = cust_rev.sum()
    if total_rev > 0:
        top3_pct = cust_rev.head(3).sum() / total_rev * 100
        # Lower concentration = higher score
        concentration_score = min(30, max(0, 30 - top3_pct * 0.3))
    else:
        concentration_score = 15

    # New customer acquisition rate (0-30 points)
    if len(customers) > 0 and "acquisition_date" in customers.columns:
        acq = customers["acquisition_date"].dropna()
        if len(acq) > 0:
            recent = (acq >= acq.max() - pd.Timedelta(days=90)).sum()
            total_acq = len(acq)
            new_cust_pct = recent / total_acq * 100
            acquisition_score = min(30, new_cust_pct * 0.5)
        else:
            acquisition_score = 10
    else:
        # Estimate from transaction data
        first_txn = df.groupby("customer_id")["date"].min()
        recent_new = (first_txn >= first_txn.max() - pd.Timedelta(days=90)).sum()
        acquisition_score = min(30, recent_new / len(first_txn) * 100 * 0.5) if len(first_txn) > 0 else 10

    total = round(channel_score + concentration_score + acquisition_score, 1)

    return {
        "loop_name": "Acquisition Loop",
        "description": "Measures customer acquisition efficiency — how effectively the business attracts new customers",
        "score": total,
        "components": {
            "channel_efficiency_score": round(channel_score, 1),
            "concentration_risk_score": round(concentration_score, 1),
            "acquisition_rate_score": round(acquisition_score, 1),
        },
        "interpretation": _interpret_score(total, "acquisition"),
    }


def calculate_expansion_loop(transactions: pd.DataFrame) -> dict:
    """
    Expansion Loop: expansion velocity score.

    Formula: upsell rate × cross-sell adoption × multi-service share

    Returns score 0-100 and component breakdown.
    """
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]

    # Upsell rate (0-35 points)
    df["month"] = df["date"].dt.to_period("M")
    customer_monthly = df.groupby(["customer_id", "month"])["total_amount"].sum().reset_index()
    customer_monthly = customer_monthly.sort_values(["customer_id", "month"])
    customer_monthly["prev_rev"] = customer_monthly.groupby("customer_id")["total_amount"].shift(1)
    customer_monthly["increase"] = customer_monthly["total_amount"] > customer_monthly["prev_rev"]
    upsell_rate = customer_monthly["increase"].mean() * 100 if len(customer_monthly) > 1 else 0
    upsell_score = min(35, upsell_rate * 0.35)

    # Cross-sell adoption (multi-service) (0-35 points)
    if "service_name" in df.columns:
        svc_per_customer = df.groupby("customer_id")["service_name"].nunique()
        multi_svc_pct = (svc_per_customer > 1).mean() * 100
        cross_sell_score = min(35, multi_svc_pct * 0.5)
    else:
        cross_sell_score = 10

    # Revenue per customer growth (0-30 points)
    customer_monthly["growth"] = customer_monthly.groupby("customer_id")["total_amount"].pct_change()
    avg_growth = customer_monthly["growth"].mean() * 100
    growth_score = min(30, max(0, 15 + avg_growth))

    total = round(upsell_score + cross_sell_score + growth_score, 1)

    return {
        "loop_name": "Expansion Loop",
        "description": "Measures expansion velocity — how effectively the business grows revenue from existing customers",
        "score": total,
        "components": {
            "upsell_rate_score": round(upsell_score, 1),
            "cross_sell_adoption_score": round(cross_sell_score, 1),
            "revenue_growth_per_customer_score": round(growth_score, 1),
        },
        "upsell_rate_pct": round(upsell_rate, 1),
        "interpretation": _interpret_score(total, "expansion"),
    }


def _interpret_score(score: float, loop: str) -> str:
    """Generate a natural-language interpretation of a loop score."""
    if score >= 80:
        return f"Excellent {loop} health. This is a well-tuned revenue engine."
    elif score >= 60:
        return f"Good {loop} health with room for improvement. Focus on the weakest component."
    elif score >= 40:
        return f"Moderate {loop} health. Several components need attention to build momentum."
    elif score >= 20:
        return f"Weak {loop} health. This loop is a drag on revenue growth — prioritize improvements."
    else:
        return f"Critical {loop} health. This loop is broken and needs immediate attention."


def calculate_all_loops(transactions: pd.DataFrame, customers: pd.DataFrame) -> dict:
    """
    Calculate all 4 causal loops.

    Returns:
        dict with all loop scores and an overall health score
    """
    pricing = calculate_pricing_loop(transactions)
    retention = calculate_retention_loop(transactions, customers)
    acquisition = calculate_acquisition_loop(transactions, customers)
    expansion = calculate_expansion_loop(transactions)

    loops = [pricing, retention, acquisition, expansion]
    overall = round(sum(l["score"] for l in loops) / len(loops), 1)

    # Find weakest loop
    weakest = min(loops, key=lambda x: x["score"])

    return {
        "overall_loop_health": overall,
        "weakest_loop": weakest["loop_name"],
        "weakest_loop_score": weakest["score"],
        "loops": {
            "pricing": pricing,
            "retention": retention,
            "acquisition": acquisition,
            "expansion": expansion,
        },
    }