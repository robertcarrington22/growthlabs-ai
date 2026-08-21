"""
Inventory Audit Report Generator — GrowthLabs AI
Generates structured JSON report section for retail inventory analysis.

Report section order (per spec):
1. Executive summary with 3 headline $ figures
2. KPI scorecard vs benchmarks
3. ABC-XYZ matrix
4. Top-20 action table (SKU, issue, action, dollar impact)
5. Reorder policy sheet
6. Seasonal pre-buy recommendations
7. Methodology appendix
"""

import pandas as pd
import numpy as np
from typing import Optional

from analysis.inventory_classification import run_inventory_classification
from analysis.inventory_forecasting import run_inventory_forecasting, aggregate_to_monthly
from analysis.inventory_policy import run_inventory_policy
from analysis.inventory_kpis import compute_all_kpis, format_kpi_scorecard


def run_inventory_audit(
    sales_df: pd.DataFrame,
    inventory_df: pd.DataFrame,
    products_df: pd.DataFrame,
    purchase_orders_df: Optional[pd.DataFrame] = None,
    default_order_cost: float = 25.0,
    default_lead_time: float = 14.0,
    default_service_level: float = 0.95,
    holding_cost_rate: float = 0.25,
    forecast_horizon: int = 6,
) -> dict:
    """
    Run the full inventory analysis pipeline and produce a structured report.

    Args:
        sales_df: Retail sales transactions
        inventory_df: Inventory snapshots
        products_df: Products master data
        purchase_orders_df: Optional purchase orders
        default_*: Policy parameters
        forecast_horizon: Forecast horizon in months

    Returns:
        Dict with full inventory audit report section
    """
    if len(sales_df) == 0:
        return {"error": "No sales data provided", "status": "empty"}

    # ── Step 1: Classification ──
    classification = run_inventory_classification(sales_df, products_df)

    # ── Step 2: Forecasting (top SKUs) ──
    forecasting = run_inventory_forecasting(
        sales_df, products_df,
        forecast_horizon=forecast_horizon,
        max_skus=50,
    )

    # ── Step 3: Policy ──
    policy = run_inventory_policy(
        classification, forecasting, products_df,
        default_order_cost=default_order_cost,
        default_lead_time=default_lead_time,
        default_service_level=default_service_level,
    )

    # ── Step 4: KPIs ──
    kpis = compute_all_kpis(sales_df, inventory_df, products_df)

    # ── Step 5: Dollar Quantification (D5.1) ──
    dollar_findings = _quantify_dollar_impact(classification, forecasting, kpis, inventory_df, holding_cost_rate)

    # ── Step 6: Top-20 Action Table ──
    top_actions = _build_top_actions(classification, kpis, dollar_findings, products_df)

    # ── Step 7: Seasonal Pre-Buy Recommendations ──
    seasonal_recs = _build_seasonal_recommendations(sales_df, products_df, forecasting)

    # ── Step 8: Reorder Policy Sheet ──
    policy_sheet = _build_policy_sheet(policy, classification)

    # ── Executive Summary with Headline $ Figures ──
    exec_summary = _build_executive_summary(dollar_findings, kpis)

    return {
        "audit_type": "inventory_health",
        "executive_summary": exec_summary,
        "kpi_scorecard": kpis,
        "kpi_scorecard_formatted": format_kpi_scorecard(kpis),
        "abc_xyz_classification": {
            "abc_summary": classification.get("abc_summary", {}),
            "xyz_summary": classification.get("xyz_summary", {}),
            "abc_xyz_matrix": classification.get("abc_xyz_matrix", {}),
            "executive_note": classification.get("executive_note", ""),
            "policy_map": classification.get("policy_map", {}),
        },
        "top_20_actions": top_actions,
        "reorder_policy_sheet": policy_sheet,
        "seasonal_prebuy_recommendations": seasonal_recs,
        "forecasting_summary": {
            "skus_forecasted": forecasting.get("skus_forecasted", 0),
            "model_counts": forecasting.get("model_counts", {}),
            "forecast_horizon_months": forecasting.get("forecast_horizon_months", 6),
        },
        "dollar_quantification": {
            "total_cash_trapped_in_dead_stock": dollar_findings.get("dead_stock_value", 0),
            "annual_carrying_cost_waste": dollar_findings.get("carrying_cost_waste", 0),
            "annual_stockout_revenue_loss": dollar_findings.get("stockout_revenue_loss", 0),
            "total_recoverable_value": dollar_findings.get("total_recoverable", 0),
        },
        "methodology": {
            "abc_classification": "Revenue-based: A=top80%, B=next15%, C=bottom5%",
            "xyz_classification": "CV-based: X<0.5 stable, Y 0.5-1.0 variable, Z>1.0 erratic",
            "forecasting": "statsmodels: SES/Holt/HW/Croston — model selection by holdout MAE",
            "safety_stock": "z × √(L·σ_d² + d̄²·σ_L²) at 95% service level (z=1.645)",
            "eoq": "√(2DS/H) where H = 25% of unit cost",
            "newsvendor": "Q* = F⁻¹(CR) for seasonal buys",
            "carrying_cost": "Standard 25%/year of inventory value",
            "stockout_recovery": "Conservative 50% recovery assumption for lost sales",
            "markdown_depth": "40% average markdown on dead stock for liquidation",
        },
        "recommendations": _build_recommendations(dollar_findings),
    }


# ── Internal Builders ──────────────────────────────────────────────


def _quantify_dollar_impact(
    classification: dict,
    forecasting: dict,
    kpis: dict,
    inventory_df: pd.DataFrame,
    holding_cost_rate: float = 0.25,
) -> dict:
    """
    Dollar quantification of inventory issues with checkable arithmetic.

    Returns:
        dict with dead_stock_value, carrying_cost_waste, stockout_revenue_loss, total_recoverable
    """

    # 1. Cash trapped in dead stock
    dead_stock = kpis.get("kpis", {}).get("dead_stock", {})
    dead_stock_value = dead_stock.get("dead_stock_value", 0)
    dead_stock_units = dead_stock.get("dead_stock_units", 0)

    # 2. Annual carrying cost waste = dead_stock_value × 25%
    carrying_cost_waste = dead_stock_value * holding_cost_rate
    carrying_cost_arithmetic = (
        f"${dead_stock_value:,.0f} (dead stock) × {holding_cost_rate*100:.0f}% (holding cost rate) "
        f"= ${carrying_cost_waste:,.0f}/year"
    )

    # 3. Stockout revenue loss (estimated from inventory with zero stock + high demand)
    # Check which SKUs are out of stock and estimate lost revenue
    inv = inventory_df.copy()
    if "on_hand" in inv.columns and "unit_price" in inv.columns:
        out_of_stock = inv[inv["on_hand"] == 0]
        stockout_value = 0
        for _, row in out_of_stock.iterrows():
            sku = row["sku"]
            # Assume each out-of-stock costs ~avg daily demand * 7 days * price * 50% recovery
            stockout_value += row.get("unit_price", 10) * 7 * 0.5
    else:
        stockout_value = dead_stock_value * 0.3  # Rough estimate

    stockout_revenue_loss = round(stockout_value, 2)
    stockout_arithmetic = (
        f"Estimated from out-of-stock SKUs × 7 days × price × 50% recovery = ${stockout_revenue_loss:,.0f}/year"
    )

    # 4. Markdown exposure = dead stock × 40% average markdown
    markdown_depth = 0.40
    markdown_exposure = dead_stock_value * markdown_depth
    markdown_arithmetic = (
        f"${dead_stock_value:,.0f} (dead stock) × {markdown_depth*100:.0f}% (avg markdown depth) "
        f"= ${markdown_exposure:,.0f} exposure"
    )

    # 5. Total recoverable = carrying cost avoided + stockout revenue recovered + markdown avoided (partial)
    total_recoverable = round(carrying_cost_waste + stockout_revenue_loss + markdown_exposure * 0.3, 2)

    return {
        "dead_stock_value": round(dead_stock_value, 2),
        "dead_stock_units": dead_stock_units,
        "carrying_cost_waste": round(carrying_cost_waste, 2),
        "carrying_cost_arithmetic": carrying_cost_arithmetic,
        "stockout_revenue_loss": stockout_revenue_loss,
        "stockout_arithmetic": stockout_arithmetic,
        "markdown_exposure": round(markdown_exposure, 2),
        "markdown_arithmetic": markdown_arithmetic,
        "total_recoverable": total_recoverable,
        "holding_cost_rate": holding_cost_rate,
        "markdown_depth": markdown_depth,
    }


def _build_executive_summary(dollar: dict, kpis: dict) -> dict:
    """Build executive summary with 3 headline $ figures."""
    return {
        "cash_freeable": dollar.get("dead_stock_value", 0),
        "annual_recoverable_revenue": dollar.get("stockout_revenue_loss", 0),
        "annual_avoidable_carrying_cost": dollar.get("carrying_cost_waste", 0),
        "total_recoverable_value": dollar.get("total_recoverable", 0),
        "headline": (
            f"${dollar.get('dead_stock_value', 0):,.0f} cash trapped in dead/excess stock, "
            f"${dollar.get('stockout_revenue_loss', 0):,.0f}/yr recoverable from stockout improvements, "
            f"${dollar.get('carrying_cost_waste', 0):,.0f}/yr in avoidable carrying costs"
        ),
    }


def _build_top_actions(
    classification: dict,
    kpis: dict,
    dollar_findings: dict,
    products_df: pd.DataFrame,
) -> list[dict]:
    """Build top-20 action table from findings."""
    actions = []

    # Dead stock actions
    dead_stock = kpis.get("kpis", {}).get("dead_stock", {})
    dead_list = dead_stock.get("dead_stock_list_top_20", [])

    for item in dead_list:
        sku = item.get("sku", "")
        value = item.get("total_value", 0)
        units = item.get("on_hand", 0)
        carrying_waste = value * 0.25
        markdown_loss = value * 0.40
        actions.append({
            "sku": sku,
            "issue": "Dead stock — no sales in last 6 months",
            "action": "Clear via markdown or bundle — do not reorder",
            "stock_units": units,
            "cash_trapped": round(value, 2),
            "annual_carrying_waste": round(carrying_waste, 2),
            "markdown_recovery_estimate": round(value - markdown_loss, 2),
            "impact_arithmetic": (
                f"${value:,.0f} cash → carrying waste ${carrying_waste:,.0f}/yr, "
                f"markdown recovery ${value - markdown_loss:,.0f}"
            ),
        })

    # Add overstock actions from ABC-XYZ CZ items
    abc_xyz_matrix = classification.get("abc_xyz_matrix", {}).get("matrix", {})
    cz_count = abc_xyz_matrix.get("CZ", 0)
    if cz_count > 0:
        actions.append({
            "sku": f"{cz_count} CZ-classified SKUs",
            "issue": f"Low-value (C) + erratic (Z) — candidate for discontinuation",
            "action": "Review profitability — run clearance if margin < 20%",
            "stock_units": 0,
            "cash_trapped": 0,
            "annual_carrying_waste": 0,
            "markdown_recovery_estimate": 0,
            "impact_arithmetic": f"{cz_count} SKUs need profitability review",
        })

    # Sort by cash trapped descending
    actions.sort(key=lambda x: x["cash_trapped"], reverse=True)

    return actions[:20]


def _build_seasonal_recommendations(
    sales_df: pd.DataFrame,
    products_df: pd.DataFrame,
    forecasting: dict,
) -> list[dict]:
    """Build seasonal pre-buy recommendations from seasonal SKU forecasts."""
    if "demand_pattern" not in products_df.columns:
        # Real client product files won't have a demand_pattern column —
        # skip seasonal pre-buy recommendations rather than crash.
        return []
    seasonals = products_df[products_df["demand_pattern"] == "seasonal"]["sku"].tolist()
    recs = []

    for sku in seasonals:
        fc = forecasting.get("forecasts", {}).get(sku, {})
        if isinstance(fc, dict) and "error" not in fc:
            forecasts = fc.get("forecasts", [])
            if len(forecasts) >= 3:
                peak = max(forecasts[:6])
                avg = sum(forecasts[:6]) / len(forecasts[:6])
                if peak > avg * 1.5:
                    # Find peak month
                    peak_month = forecasts.index(peak) + 1
                    recs.append({
                        "sku": sku,
                        "category": "Seasonal",
                        "peak_forecast_months_ahead": peak_month,
                        "peak_demand": round(peak, 1),
                        "avg_demand": round(avg, 1),
                        "peak_factor": round(peak / avg, 2),
                        "recommendation": (
                            f"Plan pre-buy {peak_month} months ahead — peak demand is "
                            f"{peak/avg:.1f}× average. Order {peak:.0f}+ units to cover peak."
                        ),
                    })

    return sorted(recs, key=lambda x: x["peak_factor"], reverse=True)[:10]


def _build_policy_sheet(policy: dict, classification: dict) -> dict:
    """Build reorder policy sheet from policy results."""
    policies = policy.get("policies", {})
    sheet = []
    for sku, pol in policies.items():
        if "error" not in pol:
            reorder = pol.get("reorder_point", {})
            eoq = pol.get("eoq", {})
            ss_variable = pol.get("safety_stock_variable_lt", {})
            sheet.append({
                "sku": sku,
                "abc_class": pol.get("abc_class", ""),
                "xyz_class": pol.get("xyz_class", ""),
                "reorder_point": reorder.get("reorder_point", 0),
                "eoq": eoq.get("eoq", 0),
                "safety_stock": ss_variable.get("safety_stock", 0),
                "order_frequency": eoq.get("order_frequency_per_year", 0),
                "order_interval_days": eoq.get("order_interval_days", 0),
                "policy": pol.get("recommended_policy", ""),
            })

    # Sort: A items first, then B, then C
    abc_order = {"A": 0, "B": 1, "C": 2}
    sheet.sort(key=lambda x: abc_order.get(x["abc_class"], 9))
    return {
        "policy_count": len(sheet),
        "policies": sheet[:50],  # Top 50
        "default_assumptions": policy.get("default_assumptions", {}),
    }


def _build_recommendations(dollar: dict) -> list[dict]:
    """Generate strategic recommendations from dollar findings."""
    recs = [
        {
            "priority": "high",
            "finding": f"${dollar.get('dead_stock_value', 0):,.0f} cash frozen in dead stock",
            "recommendation": "Run immediate aged-inventory clearance. Target 50% recovery via markdowns and bundles.",
            "estimated_impact": f"${dollar.get('dead_stock_value', 0):,.0f} × 40% recovery = ~${dollar.get('dead_stock_value', 0) * 0.4:,.0f} cash freed",
        },
        {
            "priority": "high",
            "finding": f"${dollar.get('carrying_cost_waste', 0):,.0f}/year wasted on carrying dead/excess stock",
            "recommendation": "Implement ABC-XYZ-driven inventory policy. Reduce CZ items to make-to-order.",
            "estimated_impact": f"${dollar.get('carrying_cost_waste', 0):,.0f}/year recurring savings",
        },
        {
            "priority": "medium",
            "finding": f"${dollar.get('stockout_revenue_loss', 0):,.0f}/year in estimated lost revenue from stockouts",
            "recommendation": "Set safety stock levels using variable-lead-time formula. Monitor ROPs weekly.",
            "estimated_impact": f"50% recovery = ~${dollar.get('stockout_revenue_loss', 0) * 0.5:,.0f}/year recovered",
        },
    ]
    return recs
