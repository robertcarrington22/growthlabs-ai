"""
B2B Manufacturing / Distribution analysis. Independently testable module.
"""

import pandas as pd
import numpy as np


def analyze(transactions: pd.DataFrame, customers: pd.DataFrame) -> dict:
    """B2B Manufacturing analysis: concentration risk, order frequency, margin analysis."""
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]
    df["month"] = df["date"].dt.to_period("M")

    cust_rev = df.groupby("customer_id")["total_amount"].sum().sort_values(ascending=False)
    total_rev = cust_rev.sum()
    top3_conc = round(cust_rev.head(3).sum() / total_rev * 100, 1) if total_rev > 0 else 0
    top1_conc = round(cust_rev.iloc[0] / total_rev * 100, 1) if total_rev > 0 and len(cust_rev) > 0 else 0

    freq = df.groupby("customer_id")["month"].nunique()
    avg_active = round(freq.mean(), 1)

    weighted_margin = 0
    margin_leak = []
    if "service_name" in df.columns and "estimated_margin_pct" in df.columns:
        md = df.dropna(subset=["estimated_margin_pct"])
        if len(md) > 0:
            mx = md.groupby("service_name").agg(revenue=("total_amount", "sum"), avg_margin=("estimated_margin_pct", "mean")).reset_index()
            mx["weight"] = mx["revenue"] * mx["avg_margin"] / 100
            weighted_margin = round(mx["weight"].sum() / mx["revenue"].sum() * 100, 1) if mx["revenue"].sum() > 0 else 0
            leak = mx[(mx["avg_margin"] < 20) & (mx["revenue"] > total_rev * 0.05)]
            margin_leak = leak["service_name"].tolist()

    cycle = df.groupby("customer_id")["date"].agg(["min", "max"])
    cycle["days"] = (cycle["max"] - cycle["min"]).dt.days
    avg_cycle = round(cycle["days"].mean(), 1)

    return {
        "industry": "B2B Manufacturing / Distribution",
        "top1_customer_concentration_pct": top1_conc,
        "top3_customer_concentration_pct": top3_conc,
        "total_customers": len(cust_rev),
        "avg_active_months": avg_active,
        "weighted_avg_margin_pct": weighted_margin,
        "margin_leak_services": margin_leak,
        "avg_sales_cycle_days": avg_cycle,
    }


if __name__ == "__main__":
    from data_ingestion import load_data
    ingested = load_data("sample_data/transactions.csv", "sample_data/customers.csv")
    result = analyze(ingested.transactions, ingested.customers)
    print("B2B Manufacturing Analysis:"), [print(f"  {k}: {v}") for k, v in result.items()]