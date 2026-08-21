"""
Inventory Policy Module — GrowthLabs AI
Classical APICS/CPIM inventory policy calculations.

Policy parameters:
- Safety stock (with and without lead-time variability)
- Reorder point (continuous review + periodic review)
- Economic Order Quantity (EOQ)
- Newsvendor (seasonal/single-period buys)

All methods use standard textbook formulas — no ML, no optimization solvers.
"""

import numpy as np
import pandas as pd
from typing import Optional
from scipy import stats as scipy_stats


# ── Safety Stock ────────────────────────────────────────────────────


def safety_stock_basic(
    daily_demand_std: float,
    lead_time_days: float,
    service_level: float = 0.95,
) -> dict:
    """
    Basic safety stock: SS = z × σ_d × √L

    Args:
        daily_demand_std: Standard deviation of daily demand (σ_d)
        lead_time_days: Lead time in days (L)
        service_level: Target service level (default 0.95 → z=1.645)

    Returns:
        dict with ss, z_score, lead_time_days, service_level, arithmetic
    """
    z = float(scipy_stats.norm.ppf(service_level))
    ss = z * daily_demand_std * np.sqrt(lead_time_days)

    return {
        "method": "Basic (constant lead time)",
        "safety_stock": round(ss, 2),
        "z_score": round(z, 3),
        "service_level": service_level,
        "daily_demand_std": daily_demand_std,
        "lead_time_days": lead_time_days,
        "arithmetic": f"SS = z({z:.3f}) × σ_d({daily_demand_std:.1f}) × √L(√{lead_time_days:.1f}) = {ss:.1f} units",
    }


def safety_stock_variable_lead_time(
    daily_demand_std: float,
    avg_daily_demand: float,
    lead_time_days: float,
    lead_time_std: float,
    service_level: float = 0.95,
) -> dict:
    """
    Safety stock with lead-time variability:
    SS = z × √(L · σ_d² + d̄² · σ_L²)

    Args:
        daily_demand_std: Std dev of daily demand (σ_d)
        avg_daily_demand: Average daily demand (d̄)
        lead_time_days: Average lead time in days (L)
        lead_time_std: Std dev of lead time (σ_L)
        service_level: Target service level (default 0.95)

    Returns:
        dict with ss, components, arithmetic
    """
    z = float(scipy_stats.norm.ppf(service_level))
    demand_variance = lead_time_days * (daily_demand_std ** 2)
    lead_time_variance = (avg_daily_demand ** 2) * (lead_time_std ** 2)
    total_variance = demand_variance + lead_time_variance
    ss = z * np.sqrt(total_variance)

    return {
        "method": "Variable lead time",
        "safety_stock": round(ss, 2),
        "z_score": round(z, 3),
        "service_level": service_level,
        "demand_variance_component": round(demand_variance, 2),
        "lead_time_variance_component": round(lead_time_variance, 2),
        "total_variance": round(total_variance, 2),
        "arithmetic": (
            f"SS = z({z:.3f}) × √[L({lead_time_days:.1f})·σ_d²({daily_demand_std:.1f}²) "
            f"+ d̄²({avg_daily_demand:.1f}²)·σ_L²({lead_time_std:.1f}²)]"
            f" = {ss:.1f} units"
        ),
    }


# ── Reorder Point ───────────────────────────────────────────────────


def reorder_point_continuous(
    avg_daily_demand: float,
    lead_time_days: float,
    safety_stock: float,
) -> dict:
    """
    Continuous review reorder point: ROP = d̄ × L + SS

    Args:
        avg_daily_demand: Average daily demand (d̄)
        lead_time_days: Lead time in days (L)
        safety_stock: Safety stock in units (SS)

    Returns:
        dict with rop, components, arithmetic
    """
    lead_time_demand = avg_daily_demand * lead_time_days
    rop = lead_time_demand + safety_stock

    return {
        "method": "Continuous Review (ROP)",
        "reorder_point": round(rop, 2),
        "lead_time_demand": round(lead_time_demand, 2),
        "safety_stock": round(safety_stock, 2),
        "arithmetic": f"ROP = d̄({avg_daily_demand:.1f}) × L({lead_time_days:.1f}) + SS({safety_stock:.1f}) = {rop:.1f} units",
    }


def reorder_point_periodic(
    avg_daily_demand: float,
    review_period_days: float,
    lead_time_days: float,
    daily_demand_std: float,
    service_level: float = 0.95,
) -> dict:
    """
    Periodic review order-up-to level: S = d̄ × (R + L) + z × σ_d × √(R + L)

    Args:
        avg_daily_demand: Average daily demand (d̄)
        review_period_days: Review period length in days (R)
        lead_time_days: Lead time in days (L)
        daily_demand_std: Std dev of daily demand (σ_d)
        service_level: Target service level (default 0.95)

    Returns:
        dict with order_up_to_level, safety_stock, arithmetic
    """
    z = float(scipy_stats.norm.ppf(service_level))
    cycle_lead_time = review_period_days + lead_time_days
    expected_demand = avg_daily_demand * cycle_lead_time
    safety = z * daily_demand_std * np.sqrt(cycle_lead_time)
    order_up_to = expected_demand + safety

    return {
        "method": "Periodic Review (Order-Up-To)",
        "order_up_to_level": round(order_up_to, 2),
        "safety_stock_component": round(safety, 2),
        "expected_demand_over_cycle": round(expected_demand, 2),
        "review_period_days": review_period_days,
        "lead_time_days": lead_time_days,
        "z_score": round(z, 3),
        "arithmetic": (
            f"S = d̄({avg_daily_demand:.1f}) × (R({review_period_days:.0f})+L({lead_time_days:.0f})) "
            f"+ z({z:.3f}) × σ_d({daily_demand_std:.1f}) × √(R+L)(√{cycle_lead_time:.0f})"
            f" = {order_up_to:.1f} units"
        ),
    }


# ── Economic Order Quantity ─────────────────────────────────────────


def economic_order_quantity(
    annual_demand: float,
    order_cost: float,
    unit_cost: float,
    holding_cost_rate: float = 0.25,
) -> dict:
    """
    Economic Order Quantity: EOQ = √(2DS / H)
    where H = unit_cost × holding_cost_rate

    Args:
        annual_demand: Annual demand in units (D)
        order_cost: Cost per order in $ (S)
        unit_cost: Cost per unit in $ (C)
        holding_cost_rate: Annual holding cost as fraction of unit cost (default 0.25)

    Returns:
        dict with eoq, total_annual_cost, components, arithmetic
    """
    holding_cost = unit_cost * holding_cost_rate
    if holding_cost <= 0:
        return {"error": "Holding cost must be > 0"}

    eoq = np.sqrt(2 * annual_demand * order_cost / holding_cost)

    # Total annual inventory cost
    annual_order_cost = (annual_demand / eoq) * order_cost
    annual_holding_cost = (eoq / 2) * holding_cost
    total_cost = annual_order_cost + annual_holding_cost

    # Optimal order frequency
    order_frequency = annual_demand / eoq

    return {
        "method": "EOQ",
        "eoq": round(eoq, 2),
        "annual_order_cost": round(annual_order_cost, 2),
        "annual_holding_cost": round(annual_holding_cost, 2),
        "total_annual_inventory_cost": round(total_cost, 2),
        "order_frequency_per_year": round(order_frequency, 2),
        "order_interval_days": round(365 / order_frequency, 1) if order_frequency > 0 else None,
        "arithmetic": (
            f"EOQ = √(2 × D({annual_demand:.0f}) × S({order_cost:.0f}) / H({unit_cost:.2f}×{holding_cost_rate:.2f}={holding_cost:.2f}))"
            f" = {eoq:.1f} units"
        ),
    }


# ── Newsvendor ──────────────────────────────────────────────────────


def newsvendor_quantity(
    unit_cost: float,
    unit_price: float,
    salvage_value: float = 0.0,
    demand_mean: float = 100,
    demand_std: float = 30,
    distribution: str = "normal",
) -> dict:
    """
    Newsvendor (single-period) optimal order quantity: Q* = F⁻¹(CR)

    Critical Ratio: CR = C_u / (C_u + C_o)
    where:
      C_u = underage cost = unit_price - unit_cost (lost profit per unsold)
      C_o = overage cost = unit_cost - salvage_value (loss per leftover unit)

    Args:
        unit_cost: Cost per unit ($)
        unit_price: Selling price per unit ($)
        salvage_value: Salvage/liquidation value per unit ($, default 0)
        demand_mean: Mean forecast demand
        demand_std: Std dev of forecast demand
        distribution: 'normal' (default) — only normal supported

    Returns:
        dict with q_star, cr, costs, risk_metrics
    """
    if unit_price <= unit_cost:
        return {"error": "Unit price must exceed unit cost for positive underage cost"}

    # Costs
    underage_cost = unit_price - unit_cost
    overage_cost = unit_cost - salvage_value
    critical_ratio = underage_cost / (underage_cost + overage_cost)

    if distribution == "normal":
        z = float(scipy_stats.norm.ppf(critical_ratio))
        q_star = demand_mean + z * demand_std
    else:
        return {"error": f"Unsupported distribution: {distribution}"}

    # Risk metrics
    expected_leftover = _expected_leftover_normal(demand_mean, demand_std, q_star)
    expected_stockout = _expected_stockout_normal(demand_mean, demand_std, q_star)
    expected_profit = (
        unit_price * (q_star - expected_leftover)
        + salvage_value * expected_leftover
        - unit_cost * q_star
    )

    return {
        "method": "Newsvendor",
        "optimal_order_qty": round(max(0, q_star), 2),
        "critical_ratio": round(critical_ratio, 4),
        "underage_cost": round(underage_cost, 2),
        "overage_cost": round(overage_cost, 2),
        "service_level_implied": round(critical_ratio, 4),
        "z_score": round(z, 3),
        "expected_leftover_units": round(expected_leftover, 2),
        "expected_stockout_units": round(expected_stockout, 2),
        "expected_profit": round(expected_profit, 2),
        "arithmetic": (
            f"CR = C_u({underage_cost:.2f})/(C_u+C_o)({underage_cost+overage_cost:.2f}) = {critical_ratio:.3f}\n"
            f"Q* = μ({demand_mean:.0f}) + z({z:.3f}) × σ({demand_std:.0f}) = {q_star:.0f} units"
        ),
    }


def _expected_leftover_normal(mean: float, std: float, q: float) -> float:
    """Expected leftover inventory for normal demand (loss function)."""
    z = (q - mean) / std if std > 0 else 0
    return std * (z * scipy_stats.norm.cdf(z) + scipy_stats.norm.pdf(z))


def _expected_stockout_normal(mean: float, std: float, q: float) -> float:
    """Expected stockout (lost sales) for normal demand."""
    z = (q - mean) / std if std > 0 else 0
    return std * (scipy_stats.norm.pdf(z) - z * (1 - scipy_stats.norm.cdf(z)))


# ── Batch Policy Runner ─────────────────────────────────────────────


def generate_policy_sheet(
    sku_info: pd.DataFrame,
    forecast_info: dict,
    product_costs: dict,
    default_order_cost: float = 25.0,
    default_lead_time: float = 14.0,
    default_lead_time_std: float = 3.0,
    default_service_level: float = 0.95,
    default_review_period: float = 7.0,
    default_holding_rate: float = 0.25,
) -> dict:
    """
    Generate full policy sheet for multiple SKUs.

    Args:
        sku_info: DataFrame with sku, abc_class, xyz_class
        forecast_info: Dict mapping sku → forecast data (mean_demand, std_demand)
        product_costs: Dict mapping sku → {unit_cost, unit_price}
        default_*: Default parameters

    Returns:
        dict with per-SKU policy recommendations
    """
    policies = {}

    for _, row in sku_info.iterrows():
        sku = row["sku"]
        costs = product_costs.get(sku, {"unit_cost": 10.0, "unit_price": 20.0})
        fc = forecast_info.get(sku, {})

        if isinstance(fc, dict) and "error" in fc:
            policies[sku] = {"error": fc["error"]}
            continue

        # Extract demand stats from forecast or aggregated sales
        avg_daily = fc.get("mean_monthly", 100) / 30.0 if "mean_monthly" in fc else 3.0
        std_daily = fc.get("std_monthly", 30) / np.sqrt(30) if "std_monthly" in fc else 1.5

        # Safety stock
        ss_basic = safety_stock_basic(
            daily_demand_std=std_daily,
            lead_time_days=default_lead_time,
            service_level=default_service_level,
        )
        ss_variable = safety_stock_variable_lead_time(
            daily_demand_std=std_daily,
            avg_daily_demand=avg_daily,
            lead_time_days=default_lead_time,
            lead_time_std=default_lead_time_std,
            service_level=default_service_level,
        )

        # Reorder point
        rop = reorder_point_continuous(
            avg_daily_demand=avg_daily,
            lead_time_days=default_lead_time,
            safety_stock=ss_variable["safety_stock"],
        )

        # EOQ
        annual_demand = avg_daily * 365
        eoq = economic_order_quantity(
            annual_demand=annual_demand,
            order_cost=default_order_cost,
            unit_cost=costs.get("unit_cost", 10),
            holding_cost_rate=default_holding_rate,
        )

        policies[sku] = {
            "sku": sku,
            "abc_class": row.get("abc_class", "U"),
            "xyz_class": row.get("xyz_class", "U"),
            "safety_stock_basic": ss_basic,
            "safety_stock_variable_lt": ss_variable,
            "reorder_point": rop,
            "eoq": eoq,
            "recommended_policy": _recommend_policy(row.get("abc_class", "C"), row.get("xyz_class", "X")),
        }

    return {
        "policies": policies,
        "default_assumptions": {
            "order_cost": default_order_cost,
            "lead_time_days": default_lead_time,
            "lead_time_std": default_lead_time_std,
            "service_level": default_service_level,
            "review_period_days": default_review_period,
            "holding_cost_rate": default_holding_rate,
        },
    }


def _recommend_policy(abc: str, xyz: str) -> str:
    """Generate plain-language policy recommendation from ABC-XYZ class."""
    policies = {
        ("A", "X"): "Automated JIT replenishment. Frequent small orders, tight monitoring.",
        ("A", "Y"): "Forecast-driven with safety stock. Moderate review, seasonal pre-buys.",
        ("A", "Z"): "Make-to-order or drop-ship. Minimize on-hand stock. Investigate demand.",
        ("B", "X"): "Standard EOQ periodic review. Set-and-monitor monthly.",
        ("B", "Y"): "Seasonal buffer stock. Forecast-based ordering. Review before peak seasons.",
        ("B", "Z"): "Review cost-to-serve. Consider eliminating or switching to MTO.",
        ("C", "X"): "Simplified two-bin system. Large batch, infrequent orders.",
        ("C", "Y"): "Order for specific campaigns only. No speculative stock.",
        ("C", "Z"): "Discontinue candidate. Run clearance. Do not reorder.",
    }
    return policies.get((abc, xyz), "Manual review recommended. Collect more data.")


def run_inventory_policy(
    classification_result: dict,
    forecasting_result: dict,
    products_df: pd.DataFrame,
    default_order_cost: float = 25.0,
    default_lead_time: float = 14.0,
    default_service_level: float = 0.95,
) -> dict:
    """
    Run full policy generation for classified + forecasted SKUs.

    Args:
        classification_result: Output from inventory_classification.run_inventory_classification()
        forecasting_result: Output from inventory_forecasting.run_inventory_forecasting()
        products_df: Products master DataFrame
        default_*: Default policy parameters

    Returns:
        dict with per-SKU policies and summary
    """
    # Build product cost map
    costs = {}
    for _, row in products_df.iterrows():
        costs[row["sku"]] = {
            "unit_cost": row.get("unit_cost", 10),
            "unit_price": row.get("unit_price", row.get("unit_cost", 10) * 2),
        }

    # Build sku_info from classification
    sku_detail = classification_result.get("abc_xyz_matrix", {}).get("sku_detail")
    if sku_detail is None or len(sku_detail) == 0:
        # Fallback: use ABC detail
        sku_list = classification_result.get("abc_classification", [])
        if isinstance(sku_list, list):
            sku_detail = pd.DataFrame(sku_list)
        else:
            sku_detail = pd.DataFrame()

    # Build forecast info
    fc_info = {}
    for sku, fc in forecasting_result.get("forecasts", {}).items():
        if "error" not in fc:
            fc_info[sku] = fc

    policy_result = generate_policy_sheet(
        sku_info=sku_detail,
        forecast_info=fc_info,
        product_costs=costs,
        default_order_cost=default_order_cost,
        default_lead_time=default_lead_time,
        default_service_level=default_service_level,
    )

    return policy_result
