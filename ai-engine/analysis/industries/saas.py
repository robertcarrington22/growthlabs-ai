"""
SaaS / Tech analysis. Independently testable module.
"""

import pandas as pd
import numpy as np


def analyze(transactions: pd.DataFrame, customers: pd.DataFrame) -> dict:
    """SaaS analysis: MRR/ARR, logo vs revenue churn, tier patterns, expansion rate."""
    df = transactions.copy()
    df["total_amount"] = df["amount"] * df["quantity"]
    df["month"] = df["date"].dt.to_period("M")

    monthly = df.groupby("month")["total_amount"].sum().reset_index()
    monthly.columns = ["month", "mrr"]

    if len(customers) > 0 and "is_churned" in customers.columns:
        churned = customers[customers["is_churned"] == True]
        logo_churn = len(churned)
        total_cust = len(customers)
        logo_churn_pct = round(logo_churn / total_cust * 100, 1) if total_cust > 0 else 0
    else:
        all_cust = df["customer_id"].unique()
        active = df[df["date"] >= df["date"].max() - pd.Timedelta(days=90)]["customer_id"].nunique()
        total_cust = len(all_cust)
        logo_churn = total_cust - active
        logo_churn_pct = round((1 - active / total_cust) * 100, 1) if total_cust > 0 else 0

    # Expansion revenue
    cm = df.groupby(["customer_id", "month"])["total_amount"].sum().reset_index()
    cm = cm.sort_values(["customer_id", "month"])
    cm["prev_rev"] = cm.groupby("customer_id")["total_amount"].shift(1)
    cm["expansion"] = cm["total_amount"] - cm["prev_rev"]
    expansion = cm[cm["expansion"] > 0]["expansion"].sum()
    total_rev = cm["total_amount"].sum()
    expansion_rate = round(expansion / total_rev * 100, 1) if total_rev > 0 else 0

    return {
        "industry": "SaaS / Tech",
        "logo_churn_count": int(logo_churn),
        "logo_churn_pct": logo_churn_pct,
        "expansion_revenue": round(expansion, 2),
        "expansion_rate_pct": expansion_rate,
        "avg_monthly_revenue": round(monthly["mrr"].mean(), 2),
        "mrr_trend": "up" if len(monthly) > 3 and monthly["mrr"].iloc[-1] > monthly["mrr"].iloc[0] else "down",
    }


if __name__ == "__main__":
    from data_ingestion import load_data
    ingested = load_data("sample_data/transactions.csv", "sample_data/customers.csv")
    result = analyze(ingested.transactions, ingested.customers)
    print(f"SaaS Analysis:"), [print(f"  {k}: {v}") for k, v in result.items()]