"""
E-commerce / Retail analysis. Independently testable module.
"""

import pandas as pd
import numpy as np


def analyze(transactions: pd.DataFrame, customers: pd.DataFrame) -> dict:
    """E-commerce analysis: AOV trends, CLV by cohort, channel analysis, abandonment indicators."""
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]
    df["month"] = df["date"].dt.to_period("M")

    aov_monthly = df.groupby("month")["total_amount"].mean()
    aov_current = round(aov_monthly.iloc[-1], 2) if len(aov_monthly) > 0 else 0
    aov_initial = round(aov_monthly.iloc[0], 2) if len(aov_monthly) > 0 else 0
    aov_change = round((aov_current - aov_initial) / aov_initial * 100, 1) if aov_initial > 0 else 0

    # CLV by cohort
    df["fp_month"] = df.groupby("customer_id")["date"].transform("min").dt.to_period("M")
    clv_by_cohort = df.groupby("fp_month")["total_amount"].mean()
    latest_clv = round(clv_by_cohort.iloc[-1], 2) if len(clv_by_cohort) > 0 else 0
    earliest_clv = round(clv_by_cohort.iloc[0], 2) if len(clv_by_cohort) > 0 else 0

    # Channel AOV
    if len(customers) > 0 and "acquisition_channel" in customers.columns:
        cr = df.merge(customers[["customer_id", "acquisition_channel"]], on="customer_id", how="left")
        caov = cr.groupby("acquisition_channel")["total_amount"].mean().sort_values(ascending=False)
        top_channel = caov.index[0] if len(caov) > 0 else "N/A"
        best_aov = round(caov.iloc[0], 2) if len(caov) > 0 else 0
    else:
        top_channel, best_aov = "N/A", 0

    # Abandonment proxy: tiny transactions
    small = df[df["total_amount"] < 50]["customer_id"].nunique()
    total_cust = df["customer_id"].nunique()
    abandon_pct = round(small / total_cust * 100, 1) if total_cust > 0 else 0

    return {
        "industry": "E-commerce / Retail",
        "aov_current": aov_current,
        "aov_initial": aov_initial,
        "aov_change_pct": aov_change,
        "aov_trend": "up" if aov_change > 0 else "down",
        "clv_latest_cohort": latest_clv,
        "clv_growth_pct": round((latest_clv - earliest_clv) / earliest_clv * 100, 1) if earliest_clv > 0 else 0,
        "top_channel_aov": top_channel,
        "best_channel_aov": best_aov,
        "abandonment_indicator_pct": abandon_pct,
    }


if __name__ == "__main__":
    from data_ingestion import load_data
    ingested = load_data("sample_data/transactions.csv", "sample_data/customers.csv")
    result = analyze(ingested.transactions, ingested.customers)
    print("E-commerce Analysis:"), [print(f"  {k}: {v}") for k, v in result.items()]