"""
Revenue Health Maturity Model for GrowthLabs AI.
Assesses a business on a 5-stage maturity scale:
Survival → Growth → Efficiency → Optimization → Predictability
"""

import pandas as pd
import numpy as np
from typing import Optional

STAGES = [
    "Survival",
    "Growth",
    "Efficiency",
    "Optimization",
    "Predictability",
]

STAGE_DESCRIPTIONS = {
    "Survival": "Revenue is unpredictable and reactive. Cash flow is the primary concern. Basic financial tracking exists but no analytics. Pricing is ad-hoc or cost-plus only.",
    "Growth": "Revenue is growing but inconsistently. Basic metrics are tracked (revenue, expenses). Some repeat customers exist. Pricing is market-competitive but not data-driven.",
    "Efficiency": "Revenue is stable with consistent growth. Metrics are tracked systematically. Customer segments are understood. Pricing has some tiering. Churn is monitored.",
    "Optimization": "Revenue is optimized across channels and segments. Advanced analytics inform decisions. Pricing is value-based and differentiated. Churn is proactively managed. Upsell is systematic.",
    "Predictability": "Revenue is highly predictable with strong recurring elements. Full data-driven decision making. Pricing is dynamic and optimized. Customer lifetime value is maximized. The business runs on metrics.",
}


def assess_revenue_stability(transactions: pd.DataFrame) -> float:
    """Score revenue stability (0-100)."""
    if len(transactions) < 3:
        return 20

    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]
    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("month")["total_amount"].sum()

    if len(monthly) < 3:
        return 20

    # Coefficient of variation (lower = more stable)
    cv = monthly.std() / monthly.mean() * 100 if monthly.mean() > 0 else 100
    growth_months = sum(1 for i in range(1, len(monthly)) if monthly.iloc[i] > monthly.iloc[i - 1])
    growth_pct = growth_months / (len(monthly) - 1) * 100

    # Score: low CV = good, high growth consistency = good
    stability_score = max(0, min(100, 100 - cv * 0.5 + growth_pct * 0.3))
    return round(stability_score, 1)


def assess_pricing_sophistication(transactions: pd.DataFrame) -> float:
    """Score pricing sophistication (0-100)."""
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]

    # Tier diversity: more distinct price points = better
    if "service_name" in df.columns:
        unique_services = df["service_name"].nunique()
    else:
        unique_services = 1

    # Price range (wider range = more tiering)
    price_range = df["total_amount"].max() - df["total_amount"].min()
    price_cv = df["total_amount"].std() / df["total_amount"].mean() * 100 if df["total_amount"].mean() > 0 else 0

    # Margin data availability
    has_margin = "estimated_margin_pct" in df.columns and df["estimated_margin_pct"].notna().any()

    score = 0
    score += min(30, unique_services * 5)  # Up to 30 for service diversity
    score += min(30, price_cv * 0.3)  # Up to 30 for price differentiation
    score += 20 if has_margin else 5  # Margin tracking
    score += min(20, price_range / 1000 * 0.5)  # Price range breadth

    return round(min(100, score), 1)


def assess_data_maturity(transactions: pd.DataFrame, customers: pd.DataFrame) -> float:
    """Score data maturity (0-100) based on data quality and completeness."""
    score = 0

    # Have customer data
    if len(customers) > 0:
        score += 15

    # Customer data completeness
    if len(customers) > 0:
        fields = ["industry", "acquisition_channel", "acquisition_date", "annual_revenue", "employees"]
        completeness = sum(1 for f in fields if f in customers.columns and customers[f].notna().any())
        score += min(20, completeness * 4)

    # Transaction data quality
    if len(transactions) > 0:
        score += 10
        if "service_name" in transactions.columns:
            score += 10
        if "estimated_margin_pct" in transactions.columns and transactions["estimated_margin_pct"].notna().any():
            score += 10

    # Data volume (more data = more mature)
    if len(transactions) > 1000:
        score += 10
    elif len(transactions) > 100:
        score += 5

    # Date range breadth
    date_range = (transactions["date"].max() - transactions["date"].min()).days if len(transactions) > 0 else 0
    if date_range > 730:
        score += 15
    elif date_range > 365:
        score += 10
    elif date_range > 180:
        score += 5

    return round(min(100, score), 1)


def assess_churn_health(transactions: pd.DataFrame, customers: pd.DataFrame) -> float:
    """Score churn health (0-100)."""
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]

    if len(customers) > 0 and "is_churned" in customers.columns:
        churn_pct = customers["is_churned"].mean() * 100
    else:
        # Estimate from transaction recency
        last_date = df["date"].max()
        customer_last = df.groupby("customer_id")["date"].max()
        churned_est = ((last_date - customer_last).dt.days > 180).mean() * 100
        churn_pct = churned_est

    # Lower churn = higher score
    # 0% churn = 100, 50%+ churn = 0
    score = max(0, 100 - churn_pct * 2)
    return round(score, 1)


def assess_upsell_effectiveness(transactions: pd.DataFrame) -> float:
    """Score upsell/expansion effectiveness (0-100)."""
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]

    # Multi-service adoption
    if "service_name" in df.columns:
        svc_per_customer = df.groupby("customer_id")["service_name"].nunique()
        multi_svc_pct = (svc_per_customer > 1).mean() * 100
    else:
        multi_svc_pct = 0

    # Repeat purchase rate
    txn_per_customer = df.groupby("customer_id")["transaction_id"].count()
    repeat_pct = (txn_per_customer > 1).mean() * 100

    # Revenue per customer growth
    customer_monthly = df.groupby(["customer_id", df["date"].dt.to_period("M")])["total_amount"].sum().reset_index()
    customer_monthly = customer_monthly.sort_values(["customer_id", "date"])
    customer_monthly["prev_rev"] = customer_monthly.groupby("customer_id")["total_amount"].shift(1)
    customer_monthly["growth"] = (customer_monthly["total_amount"] - customer_monthly["prev_rev"]) / customer_monthly["prev_rev"].replace(0, float("nan"))
    avg_growth = customer_monthly["growth"].mean() * 100

    score = 0
    score += min(30, multi_svc_pct * 0.6)  # Multi-service adoption
    score += min(30, repeat_pct * 0.4)  # Repeat purchases
    score += min(40, max(0, avg_growth * 2))  # Revenue growth per customer

    return round(min(100, score), 1)


def assess_maturity(
    transactions: pd.DataFrame,
    customers: pd.DataFrame,
) -> dict:
    """
    Assess the business's revenue health maturity stage.

    Args:
        transactions: Transaction DataFrame
        customers: Customer DataFrame

    Returns:
        dict with maturity assessment
    """
    dimensions = {
        "revenue_stability": assess_revenue_stability(transactions),
        "pricing_sophistication": assess_pricing_sophistication(transactions),
        "data_maturity": assess_data_maturity(transactions, customers),
        "churn_health": assess_churn_health(transactions, customers),
        "upsell_effectiveness": assess_upsell_effectiveness(transactions),
    }

    # Overall score (weighted average)
    weights = {
        "revenue_stability": 0.25,
        "pricing_sophistication": 0.20,
        "data_maturity": 0.15,
        "churn_health": 0.25,
        "upsell_effectiveness": 0.15,
    }
    overall = sum(dimensions[k] * weights[k] for k in dimensions)

    # Determine stage
    if overall < 20:
        stage = "Survival"
    elif overall < 40:
        stage = "Growth"
    elif overall < 60:
        stage = "Efficiency"
    elif overall < 80:
        stage = "Optimization"
    else:
        stage = "Predictability"

    # Find current stage index and next stage
    stage_idx = STAGES.index(stage)
    next_stage = STAGES[stage_idx + 1] if stage_idx < len(STAGES) - 1 else None

    # Generate "what's next" recommendations
    whats_next = _get_next_stage_recs(stage, dimensions)

    return {
        "overall_score": round(overall, 1),
        "current_stage": stage,
        "next_stage": next_stage,
        "stage_description": STAGE_DESCRIPTIONS[stage],
        "dimensions": dimensions,
        "whats_next": whats_next,
    }


def _get_next_stage_recs(stage: str, dims: dict) -> list[str]:
    """Generate recommendations for reaching the next stage."""
    recs = []
    if stage == "Survival":
        if dims["revenue_stability"] < 30:
            recs.append("Focus on stabilizing revenue — identify consistent revenue sources and reduce dependency on irregular income.")
        if dims["pricing_sophistication"] < 30:
            recs.append("Move from ad-hoc pricing to basic tiered packages. Start tracking what customers actually pay.")
        recs.append("Establish basic financial tracking: revenue by month, by customer, by service.")
    elif stage == "Growth":
        if dims["churn_health"] < 50:
            recs.append("Implement churn tracking by customer segment. Identify at-risk customers before they leave.")
        if dims["data_maturity"] < 50:
            recs.append("Improve data collection: track service names, margins, and customer acquisition channels.")
        if dims["upsell_effectiveness"] < 40:
            recs.append("Develop a systematic upsell process — identify customers who are ready for additional services.")
    elif stage == "Efficiency":
        if dims["pricing_sophistication"] < 60:
            recs.append("Move from tiered pricing to value-based pricing. Analyze willingness to pay by segment.")
        if dims["upsell_effectiveness"] < 60:
            recs.append("Build automated upsell triggers based on customer behavior patterns.")
        recs.append("Develop predictive churn models to proactively retain at-risk customers.")
    elif stage == "Optimization":
        if dims["data_maturity"] < 80:
            recs.append("Implement full data stack: integration between CRM, billing, and analytics tools.")
        if dims["churn_health"] < 80:
            recs.append("Fine-tune retention programs with personalized interventions based on customer health scores.")
        recs.append("Explore dynamic pricing models and AI-driven revenue optimization.")
    elif stage == "Predictability":
        recs.append("Achieve 90%+ revenue predictability. Focus on expansion revenue and customer advocacy.")
        recs.append("Share your revenue operations playbook — your systems are now a competitive advantage.")

    return recs[:3]  # Top 3 recommendations