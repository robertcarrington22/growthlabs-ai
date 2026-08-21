"""
Professional Services analysis (agencies, consultancies, law/accounting).
Independently testable module.
"""

import pandas as pd
import numpy as np


def analyze(transactions: pd.DataFrame, customers: pd.DataFrame) -> dict:
    """
    Professional Services analysis.

    Metrics:
    - Utilization rate proxy (billable vs non-billable hours via transaction frequency)
    - Project profitability by client type
    - Scope creep detection (projects that run over budget)
    - Retainer vs project revenue mix
    """
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]
    df["month"] = df["date"].dt.to_period("M")

    # Retainer vs project mix: estimate based on service names
    retainer_keywords = ["retainer", "monthly", "subscription", "ongoing", "maintenance"]
    if "service_name" in df.columns:
        df["is_retainer"] = df["service_name"].str.lower().apply(
            lambda x: any(kw in x for kw in retainer_keywords) if isinstance(x, str) else False
        )
    else:
        df["is_retainer"] = False

    retainer_rev = round(df[df["is_retainer"]]["total_amount"].sum(), 2)
    project_rev = round(df[~df["is_retainer"]]["total_amount"].sum(), 2)
    total_rev = retainer_rev + project_rev
    retainer_pct = round(retainer_rev / total_rev * 100, 1) if total_rev > 0 else 0

    # Client profitability variance
    client_profit = df.groupby("customer_id")["total_amount"].agg(["sum", "mean", "std", "count"])
    client_profit["cv"] = (client_profit["std"] / client_profit["mean"] * 100).fillna(0)
    high_variance = int((client_profit["cv"] > 50).sum())

    # Scope creep proxy
    df["customer_avg"] = df.groupby("customer_id")["total_amount"].transform("mean")
    df["is_scope_creep"] = (df["total_amount"] > df["customer_avg"] * 1.5) & (df["customer_avg"] > 0)

    return {
        "industry": "Professional Services",
        "retainer_revenue": retainer_rev,
        "project_revenue": project_rev,
        "retainer_revenue_pct": retainer_pct,
        "project_revenue_pct": round(100 - retainer_pct, 1),
        "high_variance_clients": high_variance,
        "total_clients": int(client_profit["sum"].count()),
        "scope_creep_events": int(df["is_scope_creep"].sum()),
        "scope_creep_revenue": round(df[df["is_scope_creep"]]["total_amount"].sum(), 2),
        "avg_revenue_per_client": round(client_profit["sum"].mean(), 2),
        "utilization_proxy_pct": round((df["customer_id"].nunique() / max(1, len(df))) * 100, 2),
    }


if __name__ == "__main__":
    # Self-test with sample data
    from data_ingestion import load_data
    ingested = load_data("sample_data/transactions.csv", "sample_data/customers.csv")
    result = analyze(ingested.transactions, ingested.customers)
    print(f"Professional Services Analysis:")
    for k, v in result.items():
        print(f"  {k}: {v}")