"""
Revenue trend analysis module.
Analyzes monthly/quarterly revenue trends, growth rates, and seasonality.
"""

import pandas as pd
import numpy as np
from typing import Optional


def analyze_revenue_trends(transactions: pd.DataFrame) -> dict:
    """
    Perform comprehensive revenue trend analysis.

    Args:
        transactions: DataFrame with columns: date, amount, quantity

    Returns:
        dict with trend analysis results
    """
    if len(transactions) == 0:
        return {"error": "No transaction data provided"}

    # Derive total revenue per transaction
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]
    df["month"] = df["date"].dt.to_period("M")
    df["quarter"] = df["date"].dt.to_period("Q")
    df["year"] = df["date"].dt.year

    # ── Monthly Revenue ──
    monthly = df.groupby("month").agg(
        revenue=("total_amount", "sum"),
        transaction_count=("transaction_id", "count"),
        avg_ticket=("total_amount", "mean"),
    ).reset_index()
    monthly["month_str"] = monthly["month"].astype(str)
    monthly = monthly.sort_values("month")

    monthly_trend = [
        {
            "period": row["month_str"],
            "revenue": round(row["revenue"], 2),
            "transaction_count": int(row["transaction_count"]),
            "avg_ticket_size": round(row["avg_ticket"], 2),
        }
        for _, row in monthly.iterrows()
    ]

    # ── Quarterly Revenue ──
    quarterly = df.groupby("quarter").agg(
        revenue=("total_amount", "sum"),
        transaction_count=("transaction_id", "count"),
    ).reset_index()
    quarterly["quarter_str"] = quarterly["quarter"].astype(str)
    quarterly = quarterly.sort_values("quarter")

    quarterly_trend = [
        {
            "period": row["quarter_str"],
            "revenue": round(row["revenue"], 2),
            "transaction_count": int(row["transaction_count"]),
        }
        for _, row in quarterly.iterrows()
    ]

    # ── Growth Rate Calculations ──
    monthly_revenue = monthly.set_index("month")["revenue"]
    quarterly_revenue = quarterly.set_index("quarter")["revenue"]

    def calc_growth_rates(series):
        rates = series.pct_change() * 100
        rates = rates.dropna()
        return {
            "average_growth_rate_pct": round(rates.mean(), 2) if len(rates) > 0 else 0,
            "median_growth_rate_pct": round(rates.median(), 2) if len(rates) > 0 else 0,
            "min_growth_rate_pct": round(rates.min(), 2) if len(rates) > 0 else 0,
            "max_growth_rate_pct": round(rates.max(), 2) if len(rates) > 0 else 0,
            "volatility_pct": round(rates.std(), 2) if len(rates) > 0 else 0,
            "positive_periods_pct": round(
                (rates > 0).sum() / len(rates) * 100, 1
            )
            if len(rates) > 0
            else 0,
        }

    monthly_growth = calc_growth_rates(monthly_revenue)
    quarterly_growth = calc_growth_rates(quarterly_revenue)

    # ── YOY Comparison ──
    df["year_month"] = df["date"].dt.to_period("M")
    if len(monthly_trend) >= 12:
        # Compare latest month to same month last year
        latest_month = monthly["month"].iloc[-1]
        year_ago = latest_month - 12
        yoy_months = monthly[monthly["month"].isin([latest_month, year_ago])]

        if len(yoy_months) == 2:
            latest_rev = yoy_months[yoy_months["month"] == latest_month]["revenue"].values[0]
            prev_rev = yoy_months[yoy_months["month"] == year_ago]["revenue"].values[0]
            yoy_growth = round(((latest_rev - prev_rev) / prev_rev) * 100, 2) if prev_rev > 0 else 0
        else:
            yoy_growth = None
    else:
        yoy_growth = None

    # ── Seasonality Detection ──
    monthly["month_num"] = monthly["month"].dt.month
    seasonality = monthly.groupby("month_num").agg(
        avg_revenue=("revenue", "mean"),
    ).reset_index()

    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
    }
    seasonality["month_name"] = seasonality["month_num"].map(month_names)
    seasonality["deviation_pct"] = round(
        (seasonality["avg_revenue"] / seasonality["avg_revenue"].mean() - 1) * 100, 1
    )

    # ── Revenue Concentration ──
    top_months = monthly.nlargest(3, "revenue")
    total_rev = monthly["revenue"].sum()
    concentration = round(top_months["revenue"].sum() / total_rev * 100, 1) if total_rev > 0 else 0

    # ── Overall Metrics ──
    total_revenue = round(df["total_amount"].sum(), 2)
    avg_monthly_revenue = round(monthly["revenue"].mean(), 2)
    median_monthly_revenue = round(monthly["revenue"].median(), 2)

    # Revenue per transaction
    avg_revenue_per_txn = round(df["total_amount"].mean(), 2)
    median_revenue_per_txn = round(df["total_amount"].median(), 2)

    result = {
        "summary": {
            "total_revenue": total_revenue,
            "total_transactions": len(df),
            "date_range": {
                "start": str(df["date"].min().date()),
                "end": str(df["date"].max().date()),
            },
            "months_of_data": len(monthly_trend),
            "avg_monthly_revenue": avg_monthly_revenue,
            "median_monthly_revenue": median_monthly_revenue,
            "avg_revenue_per_transaction": avg_revenue_per_txn,
            "median_revenue_per_transaction": median_revenue_per_txn,
        },
        "monthly_trend": monthly_trend,
        "quarterly_trend": quarterly_trend,
        "monthly_growth_rates": monthly_growth,
        "quarterly_growth_rates": quarterly_growth,
        "year_over_year_growth_pct": yoy_growth,
        "seasonality": [
            {
                "month": r["month_name"],
                "avg_revenue": round(r["avg_revenue"], 2),
                "deviation_from_avg_pct": r["deviation_pct"],
            }
            for _, r in seasonality.sort_values("month_num").iterrows()
        ],
        "concentration": {
            "top_3_months_share_pct": concentration,
            "top_months": [
                {
                    "month": str(r["month_str"]),
                    "revenue": round(r["revenue"], 2),
                }
                for _, r in top_months.iterrows()
            ],
        },
        "key_findings": _generate_trend_findings(monthly_growth, yoy_growth, concentration, avg_revenue_per_txn, total_revenue),
    }

    return result


def _generate_trend_findings(
    monthly_growth: dict,
    yoy_growth: Optional[float],
    concentration: float,
    avg_ticket: float,
    total_revenue: float,
) -> list[dict]:
    """Generate natural-language findings based on trend analysis."""
    findings = []

    # Growth assessment
    avg_growth = monthly_growth.get("average_growth_rate_pct", 0)
    if avg_growth > 5:
        findings.append({
            "type": "positive",
            "area": "revenue_growth",
            "finding": f"Strong monthly growth rate of {avg_growth:.1f}% — revenue is trending upward consistently.",
            "recommendation": "Double down on what's working. Identify top-performing channels and allocate more budget.",
        })
    elif avg_growth > 0:
        findings.append({
            "type": "neutral",
            "area": "revenue_growth",
            "finding": f"Modest monthly growth at {avg_growth:.1f}%. Revenue is growing but slowly.",
            "recommendation": "Review customer acquisition costs and explore upsell/cross-sell opportunities to accelerate growth.",
        })
    else:
        findings.append({
            "type": "negative",
            "area": "revenue_growth",
            "finding": f"Negative growth trend ({avg_growth:.1f}% avg monthly). Revenue is declining.",
            "recommendation": "URGENT: Conduct a full pipeline review. Analyze churn reasons and competitive positioning.",
        })

    # YoY
    if yoy_growth is not None and yoy_growth < 0:
        findings.append({
            "type": "negative",
            "area": "year_over_year",
            "finding": f"Year-over-year revenue is down {abs(yoy_growth):.1f}% compared to the same period last year.",
            "recommendation": "Investigate what drove revenue in the prior period and diagnose what changed.",
        })

    # Concentration risk
    if concentration > 50:
        findings.append({
            "type": "warning",
            "area": "revenue_concentration",
            "finding": f"Top 3 months account for {concentration:.1f}% of total revenue — high concentration risk.",
            "recommendation": "Diversify revenue streams to reduce dependency on seasonal peaks.",
        })

    # Ticket size
    if avg_ticket < 500:
        findings.append({
            "type": "opportunity",
            "area": "ticket_size",
            "finding": f"Average transaction value is ${avg_ticket:.0f} — relatively low.",
            "recommendation": "Explore bundling, tiered pricing, or volume discounts to increase per-transaction value.",
        })

    return findings
