"""
Customer segment analysis module.
Cohort analysis, churn indicators, and customer lifetime value estimation.
"""

import pandas as pd
import numpy as np
from typing import Optional


def analyze_customer_segments(
    transactions: pd.DataFrame,
    customers: pd.DataFrame,
) -> dict:
    """
    Analyze customer segments, churn patterns, and retention.

    Args:
        transactions: DataFrame with columns: date, customer_id, amount, quantity
        customers: DataFrame with customer metadata

    Returns:
        dict with customer analysis results
    """
    if len(transactions) == 0:
        return {"error": "No transaction data provided"}

    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]
    df["month"] = df["date"].dt.to_period("M")

    # ── Per-Customer Metrics ──
    customer_metrics = df.groupby("customer_id").agg(
        total_revenue=("total_amount", "sum"),
        transaction_count=("transaction_id", "count"),
        avg_ticket=("total_amount", "mean"),
        first_purchase=("date", "min"),
        last_purchase=("date", "max"),
        service_frequency=("service_name", lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else "Unknown"),
    ).reset_index()

    analysis_end = df["date"].max()
    customer_metrics["days_since_last_purchase"] = (
        analysis_end - customer_metrics["last_purchase"]
    ).dt.days
    customer_metrics["customer_lifetime_days"] = (
        customer_metrics["last_purchase"] - customer_metrics["first_purchase"]
    ).dt.days.clip(lower=1)

    # Revenue per day (activity intensity)
    customer_metrics["revenue_per_active_day"] = round(
        customer_metrics["total_revenue"] / customer_metrics["customer_lifetime_days"], 2
    )

    # ── Customer Segmentation ──
    # RFM-style segmentation
    def segment_customer(row):
        recency = row["days_since_last_purchase"]
        frequency = row["transaction_count"]
        monetary = row["total_revenue"]

        if recency <= 30 and frequency >= 5:
            return "Champion"
        elif recency <= 60 and frequency >= 3:
            return "Loyal"
        elif recency <= 90 and monetary > customer_metrics["total_revenue"].median():
            return "High Value"
        elif recency <= 30:
            return "Recent"
        elif recency <= 180:
            return "At Risk"
        elif recency <= 365:
            return "Dormant"
        else:
            return "Lost"

    customer_metrics["segment"] = customer_metrics.apply(segment_customer, axis=1)

    # Merge with customer data if available
    if len(customers) > 0:
        customer_metrics = customer_metrics.merge(
            customers[["customer_id", "industry", "acquisition_channel", "annual_revenue", "is_churned", "employees"]],
            on="customer_id",
            how="left",
        )
    else:
        for col in ["industry", "acquisition_channel", "annual_revenue", "is_churned", "employees"]:
            customer_metrics[col] = None

    # ── Segment Summary ──
    segment_summary = customer_metrics.groupby("segment").agg(
        customer_count=("customer_id", "count"),
        total_revenue=("total_revenue", "sum"),
        avg_revenue_per_customer=("total_revenue", "mean"),
        avg_transactions=("transaction_count", "mean"),
        avg_days_since_last=("days_since_last_purchase", "mean"),
    ).reset_index()

    segment_summary["revenue_share_pct"] = round(
        segment_summary["total_revenue"] / segment_summary["total_revenue"].sum() * 100, 1
    )
    segment_summary = segment_summary.sort_values("total_revenue", ascending=False)

    segments_list = [
        {
            "segment": row["segment"],
            "customer_count": int(row["customer_count"]),
            "total_revenue": round(row["total_revenue"], 2),
            "revenue_share_pct": row["revenue_share_pct"],
            "avg_revenue_per_customer": round(row["avg_revenue_per_customer"], 2),
            "avg_transactions_per_customer": round(row["avg_transactions"], 1),
            "avg_days_since_last_purchase": round(row["avg_days_since_last"], 1),
        }
        for _, row in segment_summary.iterrows()
    ]

    # ── Cohort Analysis (by acquisition month) ──
    if "first_purchase" in customer_metrics.columns:
        customer_metrics["cohort_month"] = customer_metrics["first_purchase"].dt.to_period("M")

        # Calculate retention: for each cohort, what % are still active in later months?
        cohort_data = customer_metrics.copy()
        cohort_data["cohort_month"] = cohort_data["first_purchase"].dt.to_period("M")

        # For each customer and each subsequent month, was there a purchase?
        df["customer_month"] = df["customer_id"].astype(str) + "_" + df["month"].astype(str)

        cohort_months = sorted(cohort_data["cohort_month"].unique())

        retention_matrix = []
        for cohort in cohort_months[-12:]:  # Last 12 cohorts
            cohort_custs = cohort_data[cohort_data["cohort_month"] == cohort]["customer_id"].tolist()
            if len(cohort_custs) == 0:
                continue

            cohort_txns = df[df["customer_id"].isin(cohort_custs)]
            months_active = cohort_txns.groupby("customer_id")["month"].nunique()

            total_in_cohort = len(cohort_custs)

            # Retention at month 1, 3, 6, 12
            def retention_at_months(n_months):
                """% of cohort that has purchased across at least n distinct months"""
                if total_in_cohort == 0:
                    return 0
                threshold = n_months
                retained = (months_active >= threshold).sum()
                return round(retained / total_in_cohort * 100, 1)

            retention_matrix.append({
                "cohort": str(cohort),
                "customers": total_in_cohort,
                "retention_month_1_pct": retention_at_months(1),
                "retention_month_3_pct": retention_at_months(3),
                "retention_month_6_pct": retention_at_months(6),
                "retention_month_12_pct": retention_at_months(12),
            })

    # ── Churn Indicators ──
    at_risk = customer_metrics[customer_metrics["segment"].isin(["At Risk", "Dormant", "Lost"])]
    churn_risk_revenue = round(at_risk["total_revenue"].sum(), 2)

    # Churn by channel
    churn_by_channel = None
    if "acquisition_channel" in customer_metrics.columns and customer_metrics["acquisition_channel"].notna().any():
        churn_by_channel = (
            customer_metrics[customer_metrics["segment"].isin(["Lost", "Dormant"])]
            .groupby("acquisition_channel")
            .size()
            .reset_index(name="lost_customers")
            .sort_values("lost_customers", ascending=False)
        )
        churn_by_channel["lost_customers"] = churn_by_channel["lost_customers"].astype(int)
        churn_by_channel = churn_by_channel.to_dict(orient="records")

    # ── Industry Breakdown (if available) ──
    industry_breakdown = None
    if "industry" in customer_metrics.columns and customer_metrics["industry"].notna().any():
        industry_breakdown = (
            customer_metrics.groupby("industry")
            .agg(
                customer_count=("customer_id", "count"),
                total_revenue=("total_revenue", "sum"),
                avg_revenue_per_customer=("total_revenue", "mean"),
            )
            .reset_index()
            .sort_values("total_revenue", ascending=False)
        )
        industry_breakdown = [
            {
                "industry": row["industry"],
                "customer_count": int(row["customer_count"]),
                "total_revenue": round(row["total_revenue"], 2),
                "avg_revenue_per_customer": round(row["avg_revenue_per_customer"], 2),
            }
            for _, row in industry_breakdown.iterrows()
        ]

    # ── CLV Estimation ──
    active_customers = customer_metrics[~customer_metrics["segment"].isin(["Lost", "Dormant"])]
    clv_metrics = {
        "avg_customer_lifetime_value": round(customer_metrics["total_revenue"].mean(), 2),
        "median_customer_lifetime_value": round(customer_metrics["total_revenue"].median(), 2),
        "avg_active_clv": round(active_customers["total_revenue"].mean(), 2) if len(active_customers) > 0 else 0,
        "top_10pct_clv_threshold": round(
            customer_metrics["total_revenue"].quantile(0.9), 2
        ),
        "bottom_10pct_clv_threshold": round(
            customer_metrics["total_revenue"].quantile(0.1), 2
        ),
    }

    result = {
        "summary": {
            "total_customers": len(customer_metrics),
            "active_customers": len(active_customers),
            "at_risk_customers": len(at_risk),
            "churn_risk_revenue_at_risk": churn_risk_revenue,
            "churn_risk_pct": round(len(at_risk) / len(customer_metrics) * 100, 1) if len(customer_metrics) > 0 else 0,
        },
        "clv_estimates": clv_metrics,
        "segment_summary": segments_list,
        "cohort_retention": retention_matrix if "retention_matrix" in dir() else None,
        "churn_by_channel": churn_by_channel,
        "industry_breakdown": industry_breakdown,
        "key_findings": _generate_customer_findings(
            segments_list, clv_metrics, at_risk, customer_metrics, churn_by_channel
        ),
    }

    # Add retention matrix if computed
    if "retention_matrix" in dir() and retention_matrix:
        result["cohort_retention"] = retention_matrix

    return result


def _generate_customer_findings(
    segments: list[dict],
    clv: dict,
    at_risk: pd.DataFrame,
    customer_metrics: pd.DataFrame,
    churn_by_channel: Optional[list],
) -> list[dict]:
    """Generate findings from customer analysis."""
    findings = []

    # At-risk assessment
    at_risk_count = len(at_risk)
    total_count = len(customer_metrics)
    if at_risk_count > 0 and total_count > 0:
        pct = at_risk_count / total_count * 100
        if pct > 30:
            findings.append({
                "type": "negative",
                "area": "churn_risk",
                "finding": f"{pct:.0f}% of customers ({at_risk_count}) are at risk of churning — a critical mass.",
                "recommendation": "Launch a re-engagement campaign targeting dormant and at-risk segments immediately. Offer incentives.",
            })
        elif pct > 15:
            findings.append({
                "type": "warning",
                "area": "churn_risk",
                "finding": f"{pct:.0f}% of customers ({at_risk_count}) show early churn signals.",
                "recommendation": "Proactive outreach to at-risk customers. Consider a check-in call or satisfaction survey.",
            })
        else:
            findings.append({
                "type": "positive",
                "area": "churn_risk",
                "finding": f"Only {pct:.0f}% of customers ({at_risk_count}) are at risk — healthy retention overall.",
                "recommendation": "Maintain current retention practices. Monitor at-risk segment monthly.",
            })

    # Segment concentration
    if segments:
        champion_loyal = [s for s in segments if s["segment"] in ("Champion", "Loyal")]
        if champion_loyal:
            champion_rev = sum(s["total_revenue"] for s in champion_loyal)
            total_rev = sum(s["total_revenue"] for s in segments)
            if total_rev > 0:
                share = champion_rev / total_rev * 100
                if share > 60:
                    findings.append({
                        "type": "warning",
                        "area": "customer_concentration",
                        "finding": f"Top-tier customers (Champions + Loyal) drive {share:.0f}% of revenue — high dependency.",
                        "recommendation": "Nurture mid-tier customers to reduce concentration risk. Consider a loyalty program.",
                    })

    # CLV opportunity
    if clv:
        top_threshold = clv.get("top_10pct_clv_threshold", 0)
        bottom_threshold = clv.get("bottom_10pct_clv_threshold", 0)
        ratio = top_threshold / bottom_threshold if bottom_threshold > 0 else 0
        if ratio > 10:
            findings.append({
                "type": "opportunity",
                "area": "clv_gap",
                "finding": f"10x+ gap between top and bottom customer value (${top_threshold:.0f} vs ${bottom_threshold:.0f}).",
                "recommendation": "Analyze what top customers have in common and build targeting criteria to find more like them.",
            })

    # Channel churn
    if churn_by_channel and len(churn_by_channel) > 0:
        worst_channel = churn_by_channel[0]
        findings.append({
            "type": "warning",
            "area": "channel_quality",
            "finding": f"'{worst_channel['acquisition_channel']}' has the highest churn count ({worst_channel['lost_customers']} lost customers).",
            "recommendation": "Review lead quality from this channel. Adjust targeting or reduce spend if ROI is negative.",
        })

    return findings
