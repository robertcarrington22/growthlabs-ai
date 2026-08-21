"""
Retainer pricing calculator for GrowthLabs AI.
Estimates the Growth Retainer price based on client revenue tiers.

Formula (from business plan):
    Growth Retainer = Base Retainer + Performance Bonus (optional)

Base Retainer (by revenue tier):
    $500K–$2M:  $1,000/month
    $2M–$5M:    $2,000/month
    $5M–$10M:   $3,500/month

Performance Bonus (optional):
    Up to 10% of measured new revenue attributable to recommendations
"""

from typing import Optional

# Revenue tier boundaries and their base retainers
TIERS = [
    ("$500K–$2M", 500_000, 2_000_000, 1_000),
    ("$2M–$5M", 2_000_000, 5_000_000, 2_000),
    ("$5M–$10M", 5_000_000, 10_000_000, 3_500),
]

FLOOR = 1_000
TYPICAL_RANGE = "$1,000–$4,000+/month"


def _estimate_annual_revenue(report: dict) -> float:
    """Estimate annual revenue from the audit report."""
    rev = report.get("revenue_analysis", {}).get("summary", {})
    avg_monthly = rev.get("avg_monthly_revenue", 0)
    if avg_monthly:
        return avg_monthly * 12
    return report.get("executive_summary", {}).get("key_metrics", {}).get("total_revenue_analyzed", 0)


def _find_tier(annual_revenue: float) -> tuple[str, int]:
    """
    Find the matching revenue tier and base retainer.

    Returns (tier_label, base_retainer).
    Clients below $500K get the floor ($1,000).
    Clients above $10M get $3,500 (top bracket).
    """
    for label, lo, hi, retainer in TIERS:
        if lo <= annual_revenue < hi:
            return (label, retainer)
    if annual_revenue < 500_000:
        return ("Starter (under $500K)", 1_000)
    return ("Enterprise ($10M+)", 3_500)


def calculate_base_retainer(annual_revenue: float) -> dict:
    """
    Calculate the base retainer from annual revenue.

    Args:
        annual_revenue: Client's estimated annual revenue

    Returns:
        dict with tier, base_retainer, and label
    """
    label, retainer = _find_tier(annual_revenue)
    return {
        "tier_label": label,
        "base_retainer": retainer,
        "annual_revenue_estimated": round(annual_revenue, 2),
    }


def calculate_performance_bonus(report: dict) -> dict:
    """
    Estimate the optional performance bonus.

    Uses the midpoint of the revenue impact estimate from nlp_summary
    as the "measured new revenue" baseline. Up to 10% of that.

    Returns:
        dict with bonus estimate, pct, and explanation
    """
    from nlp_summary import generate_revenue_impact_estimate

    impact = generate_revenue_impact_estimate(report)
    mid_impact = impact.get("mid", 0)

    # Performance bonus: up to 10% of measured new revenue
    pct = 10
    bonus_annual = round(mid_impact * (pct / 100))
    bonus_monthly = round(bonus_annual / 12)

    return {
        "bonus_pct": pct,
        "estimated_annual_bonus": bonus_annual,
        "estimated_monthly_bonus": bonus_monthly,
        "measured_new_revenue_annual": round(mid_impact),
        "note": f"Up to {pct}% of measured new revenue (estimated at ${mid_impact:,}/year)",
    }


def calculate_retainer(
    report: dict,
    annual_revenue: Optional[float] = None,
    include_bonus: bool = True,
) -> dict:
    """
    Calculate the recommended Growth Retainer price.

    Formula:
        Growth Retainer = Base Retainer (by revenue tier)
        + Performance Bonus (optional, up to 10% of measured new revenue)

    Args:
        report: The full audit report dictionary
        annual_revenue: Optional override for client's annual revenue
        include_bonus: Whether to include the performance bonus estimate

    Returns:
        dict with full pricing proposal
    """
    if annual_revenue is None:
        annual_revenue = _estimate_annual_revenue(report)

    # Base retainer
    base_info = calculate_base_retainer(annual_revenue)
    base_retainer = base_info["base_retainer"]

    # Performance bonus
    bonus_info = calculate_performance_bonus(report) if include_bonus else {
        "bonus_pct": 0,
        "estimated_annual_bonus": 0,
        "estimated_monthly_bonus": 0,
        "measured_new_revenue_annual": 0,
        "note": "Performance bonus is optional — discussed during audit delivery call.",
    }

    total_with_bonus = base_retainer + bonus_info["estimated_monthly_bonus"]

    return {
        "base_retainer_monthly": base_retainer,
        "base_retainer_annual": base_retainer * 12,
        "tier": base_info["tier_label"],
        "annual_revenue_estimated": base_info["annual_revenue_estimated"],
        "performance_bonus": bonus_info,
        "total_with_bonus_monthly": total_with_bonus,
        "total_with_bonus_annual": total_with_bonus * 12,
        "typical_range": TYPICAL_RANGE,
        "disclaimer": "This is an estimated retainer based on audit data. Final pricing is determined during the audit delivery call and may vary based on scope and client discussion.",
    }


def format_retainer_summary(proposal: dict) -> str:
    """Format the pricing proposal as a readable markdown string."""
    base = proposal["base_retainer_monthly"]
    tier = proposal["tier"]
    bonus = proposal["performance_bonus"]
    total = proposal["total_with_bonus_monthly"]

    lines = [
        "## 💼 Recommended Growth Retainer",
        "",
        f"**Revenue Tier:** {tier}",
        f"**Estimated Annual Revenue:** ${proposal['annual_revenue_estimated']:,.0f}",
        "",
        "### Base Retainer",
        f"| Component | Amount |",
        f"|-----------|--------|",
        f"| Base retainer ({tier}) | **${base:,}/month** (${proposal['base_retainer_annual']:,}/year) |",
        "",
        "### Performance Bonus (Optional)",
        f"| Component | Amount |",
        f"|-----------|--------|",
        f"| Up to {bonus['bonus_pct']}% of measured new revenue | Up to **${bonus['estimated_monthly_bonus']:,}/month** (${bonus['estimated_annual_bonus']:,}/year) |",
        f"| Measured new revenue baseline | ${bonus['measured_new_revenue_annual']:,}/year |",
        "",
        "### Total (with Performance Bonus)",
        f"| Component | Amount |",
        f"|-----------|--------|",
        f"| Base retainer | ${base:,}/month |",
        f"| + Performance bonus | +${bonus['estimated_monthly_bonus']:,}/month |",
        f"| **Total** | **${total:,}/month** (${proposal['total_with_bonus_annual']:,}/year) |",
        "",
        f"> Typical range for your profile: **{proposal['typical_range']}**",
        "",
        f"*{bonus['note']}*",
        "",
        f"*{proposal['disclaimer']}*",
    ]
    return "\n".join(lines)