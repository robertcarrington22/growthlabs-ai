"""
Retail Inventory KPIs Module — GrowthLabs AI
Classical retail inventory performance metrics (APICS/CPIM standard).

KPIs computed:
- Inventory Turns (annual COGS / average inventory value)
- Days Sales of Inventory (DSI) = 365 / turns
- Gross Margin Return on Investment (GMROI)
- Sell-Through Rate
- Weeks of Cover
- Stockout Rate
- Dead Stock Identification
- Inventory Velocity (units sold per day per SKU)
"""

import pandas as pd
import numpy as np
from typing import Optional


# ── Core KPI Calculations ────────────────────────────────────────────


def inventory_turns(
    annual_cogs: float,
    average_inventory_value: float,
) -> dict:
    """
    Inventory Turns = Annual COGS / Average Inventory Value

    Benchmark ranges (retail):
    - Grocery: 12–20 turns
    - Apparel: 2–4 turns
    - Electronics: 4–8 turns
    - Furniture: 2–4 turns
    - General: 4–8 turns

    Returns dict with value, benchmark_note, arithmetic.
    """
    if average_inventory_value <= 0:
        return {"error": "Average inventory value must be > 0"}

    turns = annual_cogs / average_inventory_value
    dsi = 365 / turns if turns > 0 else float("inf")

    # Benchmark assessment
    if turns >= 12:
        benchmark = "Excellent (grocery/GNC level)"
    elif turns >= 8:
        benchmark = "Very good (fast-moving retail)"
    elif turns >= 4:
        benchmark = "Average (general retail)"
    elif turns >= 2:
        benchmark = "Below average (slow-moving)"
    else:
        benchmark = "Poor — significant overstock risk"

    return {
        "kpi": "Inventory Turns",
        "value": round(turns, 2),
        "dsi_days": round(dsi, 1),
        "annual_cogs": round(annual_cogs, 2),
        "average_inventory_value": round(average_inventory_value, 2),
        "benchmark": benchmark,
        "arithmetic": f"Turns = COGS({annual_cogs:,.0f}) / AvgInv({average_inventory_value:,.0f}) = {turns:.2f}x",
    }


def days_sales_of_inventory(
    inventory_value: float,
    daily_cogs: float,
) -> dict:
    """
    Days Sales of Inventory (DSI) = Inventory Value / Daily COGS

    Also computed as 365 / Turns.

    Benchmark: < 45 days is healthy for most retail.
    """
    if daily_cogs <= 0:
        return {"error": "Daily COGS must be > 0"}

    dsi = inventory_value / daily_cogs

    if dsi <= 30:
        benchmark = "Very healthy — fast inventory velocity"
    elif dsi <= 45:
        benchmark = "Healthy — within retail norms"
    elif dsi <= 60:
        benchmark = "Elevated — consider promotion or markdown"
    elif dsi <= 90:
        benchmark = "High — investigate slow movers"
    else:
        benchmark = "Critical — overstocked, significant cash trapped"

    return {
        "kpi": "Days Sales of Inventory (DSI)",
        "value": round(dsi, 1),
        "inventory_value": round(inventory_value, 2),
        "daily_cogs": round(daily_cogs, 2),
        "benchmark": benchmark,
        "arithmetic": f"DSI = Inv({inventory_value:,.0f}) / DailyCOGS({daily_cogs:,.2f}) = {dsi:.1f} days",
    }


def gmroi(
    gross_margin: float,
    average_inventory_cost: float,
) -> dict:
    """
    Gross Margin Return on Investment (GMROI) = Gross Margin $ / Avg Inventory at Cost

    For every $1 in inventory, how much gross margin is generated.

    Benchmark:
    - > 3.0: Excellent
    - 2.0–3.0: Good
    - 1.0–2.0: Average
    - < 1.0: Poor — inventory not generating enough margin
    """
    if average_inventory_cost <= 0:
        return {"error": "Average inventory cost must be > 0"}

    ratio = gross_margin / average_inventory_cost

    if ratio >= 3.0:
        benchmark = "Excellent — inventory is highly productive"
    elif ratio >= 2.0:
        benchmark = "Good — healthy return on inventory investment"
    elif ratio >= 1.0:
        benchmark = "Average — inventory covering its cost"
    else:
        benchmark = "Poor — inventory not generating sufficient margin"

    return {
        "kpi": "GMROI",
        "value": round(ratio, 2),
        "gross_margin": round(gross_margin, 2),
        "average_inventory_cost": round(average_inventory_cost, 2),
        "benchmark": benchmark,
        "arithmetic": f"GMROI = GM({gross_margin:,.0f}) / AvgInvCost({average_inventory_cost:,.0f}) = ${ratio:.2f} per $1 inventory",
    }


def sell_through_rate(
    units_sold: float,
    units_received: float,
    period_days: int = 30,
) -> dict:
    """
    Sell-Through Rate = Units Sold / Units Received (over a period)

    Measures how quickly inventory is selling relative to what came in.

    Benchmark (monthly):
    - > 80%: Fast-moving — risk of stockout
    - 50–80%: Healthy
    - 20–50%: Slow-moving — review pricing/promotion
    - < 20%: Dead stock risk
    """
    if units_received <= 0:
        return {"error": "Units received must be > 0"}

    rate = (units_sold / units_received) * 100

    if rate >= 80:
        benchmark = "Fast-moving — ensure adequate replenishment"
    elif rate >= 50:
        benchmark = "Healthy — good inventory velocity"
    elif rate >= 20:
        benchmark = "Slow-moving — consider markdown or promotion"
    else:
        benchmark = "Dead stock risk — investigate and clear"

    return {
        "kpi": "Sell-Through Rate",
        "value": round(rate, 1),
        "units_sold": int(units_sold),
        "units_received": int(units_received),
        "period_days": period_days,
        "benchmark": benchmark,
        "arithmetic": f"SellThrough = {units_sold:.0f} / {units_received:.0f} × 100 = {rate:.1f}%",
    }


def weeks_of_cover(
    current_stock_units: float,
    avg_weekly_demand: float,
) -> dict:
    """
    Weeks of Cover = Current Stock / Average Weekly Demand

    Indicates how many weeks current stock will last at current demand rate.

    Target: 4–8 weeks for most retail categories.
    """
    if avg_weekly_demand <= 0:
        return {"error": "Average weekly demand must be > 0"}

    woc = current_stock_units / avg_weekly_demand

    if woc < 2:
        benchmark = "Critical stockout risk — expedite replenishment"
    elif woc < 4:
        benchmark = "Low — buffer stock needed"
    elif woc <= 8:
        benchmark = "Healthy — within target range"
    elif woc <= 12:
        benchmark = "Elevated — review for potential overstock"
    else:
        benchmark = "Overstock — significant excess inventory"

    return {
        "kpi": "Weeks of Cover",
        "value": round(woc, 1),
        "current_stock_units": int(current_stock_units),
        "avg_weekly_demand": round(avg_weekly_demand, 1),
        "benchmark": benchmark,
        "arithmetic": f"WoC = Stock({current_stock_units:.0f}) / WeeklyDemand({avg_weekly_demand:.1f}) = {woc:.1f} weeks",
    }


def stockout_rate(
    days_out_of_stock: int,
    total_trading_days: int,
) -> dict:
    """
    Stockout Rate = Days Out of Stock / Total Trading Days

    Measures inventory availability. Higher values mean lost sales.
    """
    if total_trading_days <= 0:
        return {"error": "Total trading days must be > 0"}

    rate = (days_out_of_stock / total_trading_days) * 100

    if rate <= 1:
        benchmark = "Excellent availability"
    elif rate <= 3:
        benchmark = "Good — within acceptable range"
    elif rate <= 5:
        benchmark = "Moderate — improvement recommended"
    elif rate <= 10:
        benchmark = "Poor — significant lost revenue risk"
    else:
        benchmark = "Critical — frequent stockouts damaging revenue"

    return {
        "kpi": "Stockout Rate",
        "value": round(rate, 1),
        "days_out_of_stock": days_out_of_stock,
        "total_trading_days": total_trading_days,
        "benchmark": benchmark,
        "arithmetic": f"StockoutRate = {days_out_of_stock} / {total_trading_days} × 100 = {rate:.1f}%",
    }


def dead_stock_identification(
    sku_sales: pd.DataFrame,
    current_inventory: pd.DataFrame,
    no_sale_months: int = 6,
) -> dict:
    """
    Identify dead stock — SKUs with zero sales in recent N months.

    Args:
        sku_sales: DataFrame with sku, quantity, date columns
        current_inventory: DataFrame with sku, on_hand, unit_cost columns
        no_sale_months: Months without a sale to classify as dead (default 6)

    Returns:
        dict with dead_stock_list, count, total_value, total_units
    """
    # Find the latest date in the data
    latest = pd.to_datetime(sku_sales["date"]).max()
    cutoff = latest - pd.DateOffset(months=no_sale_months)

    # Get SKUs with recent sales
    recent_sales = sku_sales[pd.to_datetime(sku_sales["date"]) >= cutoff]
    skus_with_sales = set(recent_sales["sku"].unique())

    # Get all SKUs on hand
    all_stocked = set(current_inventory["sku"].unique())
    dead_skus = all_stocked - skus_with_sales

    # Calculate value of dead stock
    dead_details = []
    total_units = 0
    total_value = 0.0

    for _, row in current_inventory.iterrows():
        if row["sku"] in dead_skus and row["on_hand"] > 0:
            unit_cost = row.get("unit_cost", 0)
            value = row["on_hand"] * unit_cost
            total_units += int(row["on_hand"])
            total_value += value
            dead_details.append({
                "sku": row["sku"],
                "on_hand": int(row["on_hand"]),
                "unit_cost": float(unit_cost),
                "total_value": round(value, 2),
                "months_without_sale": no_sale_months,
            })

    # Sort by value descending
    dead_details.sort(key=lambda x: x["total_value"], reverse=True)

    return {
        "kpi": "Dead Stock",
        "dead_sku_count": len(dead_details),
        "dead_stock_units": total_units,
        "dead_stock_value": round(total_value, 2),
        "dead_stock_list_top_20": dead_details[:20],
        "total_stocked_skus": len(all_stocked),
        "dead_stock_pct_of_skus": round(len(dead_details) / len(all_stocked) * 100, 1) if all_stocked else 0,
        "no_sale_months_threshold": no_sale_months,
        "arithmetic": f"DeadStockValue = Σ(SKU_on_hand × unit_cost) = ${total_value:,.2f}",
    }


# ── Aggregate KPI Runner ────────────────────────────────────────────


def compute_all_kpis(
    sales_df: pd.DataFrame,
    inventory_df: pd.DataFrame,
    products_df: pd.DataFrame,
    annual_cogs_override: Optional[float] = None,
    avg_inventory_override: Optional[float] = None,
    total_trading_days: int = 365,
) -> dict:
    """
    Compute all retail inventory KPIs from sales, inventory, and product data.

    Args:
        sales_df: Sales transactions (sku, quantity, date, unit_price[, unit_cost])
        inventory_df: Inventory snapshots (sku, on_hand, date[, unit_cost])
        products_df: Products (sku, unit_cost, unit_price[, category])
        annual_cogs_override: If provided, use instead of computing from data
        avg_inventory_override: If provided, use instead of computing from data
        total_trading_days: Days in analysis period for stockout rate

    Returns:
        dict with all KPI results and executive summary
    """
    df = sales_df.copy()
    inv = inventory_df.copy()
    prods = products_df.copy()

    # Merge product cost/price into sales if not already present
    if "unit_cost" not in df.columns and "unit_cost" in prods.columns:
        df = df.merge(prods[["sku", "unit_cost", "unit_price"]], on="sku", suffixes=("", "_prod"), how="left")
        # Use product price if sales doesn't have it
        if "unit_price" not in df.columns or "unit_price" in df.columns and "_prod" in df.columns:
            pass  # Already handled

    # Ensure cost and revenue columns
    if "unit_cost" not in df.columns:
        # Estimate cost as 60% of price
        df["unit_cost"] = df.get("unit_price", 20) * 0.6
    if "unit_price" not in df.columns:
        df["unit_price"] = df.get("unit_cost", 10) * 1.67

    # Compute revenue and COGS per transaction
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["cogs"] = df["quantity"] * df["unit_cost"]
    df["margin"] = df["revenue"] - df["cogs"]

    # ── Aggregate values ──
    total_revenue = df["revenue"].sum()
    total_cogs = df["cogs"].sum()
    total_margin = df["margin"].sum()

    # Average inventory value
    if avg_inventory_override:
        avg_inv_value = avg_inventory_override
    else:
        # Merge cost into inventory
        if "unit_cost" not in inv.columns and "unit_cost" in prods.columns:
            inv = inv.merge(prods[["sku", "unit_cost"]], on="sku", how="left")
        elif "unit_cost" not in inv.columns:
            inv["unit_cost"] = 10.0
        inv["inv_value"] = inv["on_hand"] * inv["unit_cost"]
        avg_inv_value = float(inv["inv_value"].mean()) if len(inv) > 0 else 0

    annual_cogs = annual_cogs_override or total_cogs

    # ── Compute KPIs ──
    turns = inventory_turns(annual_cogs, avg_inv_value)
    dsi = days_sales_of_inventory(avg_inv_value, total_cogs / total_trading_days if total_trading_days > 0 else 1)
    gmi = gmroi(total_margin, avg_inv_value)

    # Sell-through (monthly)
    latest_month = pd.to_datetime(df["date"]).max()
    month_ago = latest_month - pd.DateOffset(days=30)
    recent = df[pd.to_datetime(df["date"]) >= month_ago]
    total_sold_month = int(recent["quantity"].sum()) if len(recent) > 0 else 0
    total_received = int(inv["on_hand"].sum()) if len(inv) > 0 else 1
    sell_through = sell_through_rate(total_sold_month, max(total_received, 1), 30)

    # Weeks of cover (overall)
    avg_weekly_demand = (total_sold_month / 4.33) if total_sold_month > 0 else 1
    stock_units = int(inv["on_hand"].sum()) if len(inv) > 0 else 0
    woc = weeks_of_cover(stock_units, avg_weekly_demand)

    # Dead stock
    ds = dead_stock_identification(df, inv)

    # ── Inventory velocity per SKU ──
    daily_sales = df.groupby("sku")["quantity"].sum() / max(total_trading_days, 1)
    velocity = daily_sales.to_dict()

    return {
        "kpis": {
            "inventory_turns": turns,
            "days_sales_of_inventory": dsi,
            "gmroi": gmi,
            "sell_through_rate_30day": sell_through,
            "weeks_of_cover": woc,
            "dead_stock": ds,
        },
        "aggregates": {
            "total_revenue": round(total_revenue, 2),
            "total_cogs": round(total_cogs, 2),
            "total_margin": round(total_margin, 2),
            "average_inventory_value": round(avg_inv_value, 2),
            "total_stock_units": stock_units,
            "total_trading_days": total_trading_days,
        },
        "inventory_velocity": velocity,
        "kpi_count": 6,
    }


def format_kpi_scorecard(kpi_results: dict) -> str:
    """Format KPI results as a readable scorecard string."""
    kpis = kpi_results.get("kpis", {})
    agg = kpi_results.get("aggregates", {})

    lines = [
        "=" * 60,
        "  INVENTORY KPI SCORECARD",
        "=" * 60,
        "",
        f"  Revenue Analyzed:  ${agg.get('total_revenue', 0):,.2f}",
        f"  COGS:              ${agg.get('total_cogs', 0):,.2f}",
        f"  Gross Margin:      ${agg.get('total_margin', 0):,.2f}",
        f"  Avg Inventory:     ${agg.get('average_inventory_value', 0):,.2f}",
        "",
    ]

    for key, result in kpis.items():
        if isinstance(result, dict) and "error" not in result:
            val = result.get("value", "N/A")
            bench = result.get("benchmark", "")
            lines.append(f"  {result.get('kpi', key)}: {val}")
            lines.append(f"    → {bench}")
            lines.append("")

    # Dead stock summary
    ds = kpis.get("dead_stock", {})
    if isinstance(ds, dict) and "error" not in ds:
        lines.append(f"  DEAD STOCK: {ds.get('dead_sku_count', 0)} SKUs, "
                     f"{ds.get('dead_stock_units', 0)} units, "
                     f"${ds.get('dead_stock_value', 0):,.2f} trapped cash")
        lines.append(f"    → {ds.get('dead_sku_count', 0)} of {ds.get('total_stocked_skus', 0)} "
                     f"SKUs ({ds.get('dead_stock_pct_of_skus', 0)}%) have had zero sales in "
                     f"{ds.get('no_sale_months_threshold', 6)} months")

    return "\n".join(lines)
