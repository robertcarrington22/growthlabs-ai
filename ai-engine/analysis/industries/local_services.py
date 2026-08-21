"""
Local Service Business analysis. Independently testable module.
"""

import pandas as pd
import numpy as np


def analyze(transactions: pd.DataFrame, customers: pd.DataFrame) -> dict:
    """Local services analysis: repeat rate, seasonality, service profitability."""
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]
    df["month"] = df["date"].dt.to_period("M")

    customer_freq = df.groupby("customer_id")["transaction_id"].count()
    repeat = int((customer_freq > 1).sum())
    total = len(customer_freq)
    repeat_rate = round(repeat / total * 100, 1) if total > 0 else 0

    monthly = df.groupby("month")["total_amount"].sum()
    seasonal_ratio = round(monthly.max() / monthly.mean(), 2) if len(monthly) >= 3 and monthly.mean() > 0 else 1

    if "service_name" in df.columns and "estimated_margin_pct" in df.columns:
        svc = df.groupby("service_name").agg(revenue=("total_amount", "sum"), avg_margin=("estimated_margin_pct", "mean")).reset_index()
        svc["profit"] = svc["revenue"] * svc["avg_margin"] / 100
        most_profitable = svc.sort_values("profit", ascending=False).iloc[0]["service_name"] if len(svc) > 0 else "N/A"
    else:
        most_profitable = "N/A"

    aov_by_month = df.groupby("month")["total_amount"].mean()
    aov_trend = "up" if len(aov_by_month) > 3 and aov_by_month.iloc[-1] > aov_by_month.iloc[0] else "down"

    return {
        "industry": "Local Services",
        "repeat_purchase_rate_pct": repeat_rate,
        "one_time_customers": int(total - repeat),
        "repeat_customers": repeat,
        "seasonal_ratio": seasonal_ratio,
        "most_profitable_service": most_profitable,
        "aov_trend": aov_trend,
        "avg_ticket": round(df["total_amount"].mean(), 2),
    }


if __name__ == "__main__":
    from data_ingestion import load_data
    ingested = load_data("sample_data/transactions.csv", "sample_data/customers.csv")
    result = analyze(ingested.transactions, ingested.customers)
    print("Local Services Analysis:"), [print(f"  {k}: {v}") for k, v in result.items()]