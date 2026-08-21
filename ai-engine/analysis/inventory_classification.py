"""
Inventory ABC-XYZ Classification Module — GrowthLabs AI
Classical APICS/CPIM standard classification for retail inventory management.

ABC classification: by revenue or margin contribution
XYZ classification: by demand variability (coefficient of variation)
ABC-XYZ 9-cell matrix: drives replenishment and management policy
"""

import pandas as pd
import numpy as np
from typing import Optional, Literal


def classify_abc(
    df: pd.DataFrame,
    value_col: str = "revenue",
    sku_col: str = "sku",
    a_threshold: float = 0.80,
    b_threshold: float = 0.95,
) -> pd.DataFrame:
    """
    ABC classification by revenue/margin contribution.

    A: top contributors up to `a_threshold` cumulative (default 80%)
    B: next contributors up to `b_threshold` cumulative (default 95%)
    C: bottom contributors (remaining 5%)

    Args:
        df: DataFrame with SKU and value column
        value_col: Column to classify by (e.g., 'revenue', 'margin')
        sku_col: SKU identifier column
        a_threshold: Cumulative % cutoff for A items (default 0.80)
        b_threshold: Cumulative % cutoff for B items (default 0.95)

    Returns:
        DataFrame with ['sku', value_col, 'total_value', 'pct_of_total',
                         'cumulative_pct', 'abc_class']
    """
    # Aggregate by SKU
    sku_values = df.groupby(sku_col)[value_col].sum().reset_index()
    sku_values = sku_values.rename(columns={value_col: "total_value"})

    # Sort descending by value
    sku_values = sku_values.sort_values("total_value", ascending=False).reset_index(drop=True)

    # Calculate percentage of total and cumulative
    total = sku_values["total_value"].sum()
    sku_values["pct_of_total"] = sku_values["total_value"] / total
    sku_values["cumulative_pct"] = sku_values["pct_of_total"].cumsum()

    # Assign ABC classes
    def _abc_class(cum_pct):
        if cum_pct <= a_threshold:
            return "A"
        elif cum_pct <= b_threshold:
            return "B"
        else:
            return "C"

    sku_values["abc_class"] = sku_values["cumulative_pct"].apply(_abc_class)

    return sku_values


def classify_xyz(
    df: pd.DataFrame,
    sku_col: str = "sku",
    qty_col: str = "quantity",
    date_col: str = "date",
    x_threshold: float = 0.5,
    y_threshold: float = 1.0,
    min_periods: int = 4,
) -> pd.DataFrame:
    """
    XYZ classification by demand variability (coefficient of variation).

    X: stable demand, CV < x_threshold (default 0.5)
    Y: variable/seasonal, x_threshold <= CV < y_threshold (default 0.5–1.0)
    Z: erratic demand, CV >= y_threshold (default 1.0)

    Computes CV = σ / μ on monthly demand aggregates per SKU.

    Args:
        df: Sales transaction DataFrame
        sku_col: SKU identifier column
        qty_col: Quantity sold column
        date_col: Date column
        x_threshold: Max CV for X classification (default 0.5)
        y_threshold: Max CV for Y classification (default 1.0)
        min_periods: Minimum periods with data to classify (default 4)

    Returns:
        DataFrame with ['sku', 'mean_demand', 'std_demand', 'cv', 'xyz_class']
    """
    # Ensure date is datetime
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    # Aggregate to monthly demand per SKU
    df["year_month"] = df[date_col].dt.to_period("M")
    monthly = df.groupby([sku_col, "year_month"])[qty_col].sum().reset_index()

    # Compute mean, std, CV per SKU
    sku_stats = (
        monthly.groupby(sku_col)[qty_col]
        .agg(mean_demand="mean", std_demand="std", n_periods="count")
        .reset_index()
    )
    sku_stats["cv"] = np.where(
        (sku_stats["n_periods"] >= min_periods) & (sku_stats["mean_demand"] > 0),
        sku_stats["std_demand"] / sku_stats["mean_demand"],
        np.nan,
    )

    # Classify
    def _xyz_class(cv):
        if pd.isna(cv):
            return "U"  # Unclassified — insufficient data
        if cv < x_threshold:
            return "X"
        elif cv < y_threshold:
            return "Y"
        else:
            return "Z"

    sku_stats["xyz_class"] = sku_stats["cv"].apply(_xyz_class)

    return sku_stats


def build_abc_xyz_matrix(
    abc_df: pd.DataFrame,
    xyz_df: pd.DataFrame,
    sku_col: str = "sku",
) -> dict:
    """
    Build the ABC-XYZ 9-cell matrix and generate policy recommendations.

    Returns dict with:
    - matrix: 3x3 dict counting SKUs per cell {abc}_{xyz}
    - policy: dict mapping cell code to policy recommendation
    - sku_map: dict mapping each SKU to (abc_class, xyz_class, policy)
    - sku_detail: DataFrame with all SKU classifications
    """
    # Merge ABC and XYZ classifications
    merged = abc_df[[sku_col, "abc_class", "total_value", "pct_of_total"]].merge(
        xyz_df[[sku_col, "xyz_class", "mean_demand", "cv"]],
        on=sku_col,
        how="left",
    )

    # Fill missing XYZ
    merged["xyz_class"] = merged["xyz_class"].fillna("U")

    # Build cell code
    merged["cell"] = merged["abc_class"] + merged["xyz_class"]

    # Count matrix
    matrix = {}
    for abc in ["A", "B", "C"]:
        for xyz in ["X", "Y", "Z", "U"]:
            cell = f"{abc}{xyz}"
            count = len(merged[(merged["abc_class"] == abc) & (merged["xyz_class"] == xyz)])
            if count > 0:
                matrix[cell] = int(count)

    # Policy recommendations (APICS/CPIM standard)
    policy_map = {
        "AX": "Automated replenishment — tight control, frequent small orders, JIT",
        "AY": "Hybrid: forecast-driven with safety stock — moderate review cycle",
        "AZ": "High-value erratic — make-to-order or drop-ship, minimize stock",
        "BX": "Standard replenishment — periodic review, EOQ-based ordering",
        "BY": "Seasonal/buffer stock — forecast-based with higher safety stock",
        "BZ": "Low-value speculative — investigate demand cause, consider elimination",
        "CX": "Simplified reorder — large batch, infrequent review",
        "CY": "Seasonal hold — order for specific campaigns only",
        "CZ": "Discontinue candidate — review profitability, clearance recommended",
        "AU": "Insufficient demand data — classify manually, collect more data",
        "BU": "Insufficient demand data — classify manually",
        "CU": "Review for discontinuation or manual classification",
    }

    policies = {}
    for cell in matrix:
        policies[cell] = policy_map.get(cell, "Manual review recommended")

    # Build SKU-level policy map
    sku_policies = {}
    for _, row in merged.iterrows():
        sku = row[sku_col]
        cell = row["cell"]
        sku_policies[sku] = {
            "abc_class": row["abc_class"],
            "xyz_class": row["xyz_class"],
            "cell": cell,
            "policy": policy_map.get(cell, "Manual review recommended"),
            "pct_of_revenue": row["pct_of_total"],
        }

    return {
        "matrix": matrix,
        "policy_map": policies,
        "sku_policies": sku_policies,
        "sku_detail": merged,
        "executive_note": _matrix_executive_note(matrix),
    }


def _matrix_executive_note(matrix: dict) -> str:
    """Generate a plain-English executive note about the ABC-XYZ matrix."""
    total = sum(matrix.values())
    if total == 0:
        return "No SKU data available for ABC-XYZ matrix."

    a_skus = sum(matrix.get(c, 0) for c in ["AX", "AY", "AZ"])
    c_skus = sum(matrix.get(c, 0) for c in ["CX", "CY", "CZ"])
    z_skus = sum(matrix.get(c, 0) for c in ["AZ", "BZ", "CZ"])

    lines = [f"ABC-XYZ matrix covers {total} SKUs."]
    if a_skus > 0:
        lines.append(f"  {a_skus} high-value SKUs (A) require tight management.")
    if z_skus > 0:
        lines.append(f"  {z_skus} erratic-demand SKUs (Z) need special handling.")
    if c_skus > 0:
        lines.append(f"  {c_skus} low-value SKUs (C) are candidates for simplification or discontinuation.")

    return " ".join(lines)


def run_inventory_classification(
    sales_df: pd.DataFrame,
    products_df: pd.DataFrame,
    value_col: str = "revenue",
    sku_col: str = "sku",
) -> dict:
    """
    Run full ABC-XYZ classification pipeline.

    Args:
        sales_df: Sales transaction DataFrame (must have sku, quantity, date, unit_price[, unit_cost])
        products_df: Products DataFrame (must have sku, unit_cost, unit_price)
        value_col: Which value measure to use for ABC ('revenue' or 'margin')

    Returns:
        Dict with abc_results, xyz_results, matrix_results
    """
    # Prepare sales with revenue per transaction
    df = sales_df.copy()
    df["revenue"] = df["quantity"] * df["unit_price"]

    # Merge cost if available
    if "unit_cost" not in df.columns and "unit_cost" in products_df.columns:
        df = df.merge(products_df[[sku_col, "unit_cost"]], on=sku_col, how="left")
    if "unit_cost" in df.columns:
        df["margin"] = df["quantity"] * (df["unit_price"] - df["unit_cost"].fillna(0))
    else:
        df["margin"] = df["revenue"] * 0.35  # Default margin assumption

    value_column = "margin" if value_col == "margin" else "revenue"

    # Run classifications
    abc = classify_abc(df, value_col=value_column, sku_col=sku_col)
    xyz = classify_xyz(df, sku_col=sku_col)
    matrix = build_abc_xyz_matrix(abc, xyz, sku_col=sku_col)

    return {
        "abc_classification": abc.to_dict(orient="records"),
        "abc_summary": abc["abc_class"].value_counts().to_dict(),
        "xyz_classification": xyz.to_dict(orient="records"),
        "xyz_summary": xyz["xyz_class"].value_counts().to_dict(),
        "abc_xyz_matrix": matrix["matrix"],
        "policy_map": matrix["policy_map"],
        "executive_note": matrix["executive_note"],
        "sku_count": len(abc),
    }
