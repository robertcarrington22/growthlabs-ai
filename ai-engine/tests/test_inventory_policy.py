"""Unit tests: safety stock, EOQ, and reorder point formulas (analysis/inventory_policy.py).

All expected values are hand-computed from the textbook formulas:
  SS  = z * sigma_d * sqrt(L)
  EOQ = sqrt(2DS / H)
  ROP = d_bar * L + SS
"""

import math

import pytest
from scipy import stats as scipy_stats

from analysis.inventory_policy import (
    safety_stock_basic,
    safety_stock_variable_lead_time,
    reorder_point_continuous,
    economic_order_quantity,
)

Z_95 = float(scipy_stats.norm.ppf(0.95))  # ~1.6449


class TestSafetyStock:
    def test_basic_formula(self):
        # SS = 1.6449 * 10 * sqrt(16) = 1.6449 * 40 = 65.79
        result = safety_stock_basic(daily_demand_std=10.0, lead_time_days=16.0, service_level=0.95)
        expected = Z_95 * 10.0 * math.sqrt(16.0)
        assert result["safety_stock"] == pytest.approx(expected, abs=0.01)
        assert result["z_score"] == pytest.approx(1.645, abs=0.001)

    def test_basic_zero_variability_gives_zero_ss(self):
        result = safety_stock_basic(daily_demand_std=0.0, lead_time_days=14.0)
        assert result["safety_stock"] == pytest.approx(0.0)

    def test_higher_service_level_needs_more_stock(self):
        low = safety_stock_basic(10.0, 16.0, service_level=0.90)["safety_stock"]
        high = safety_stock_basic(10.0, 16.0, service_level=0.99)["safety_stock"]
        assert high > low

    def test_variable_lead_time_formula(self):
        # SS = z * sqrt(L*sigma_d^2 + d_bar^2*sigma_L^2)
        #    = 1.6449 * sqrt(16*100 + 25*4) = 1.6449 * sqrt(1700)
        result = safety_stock_variable_lead_time(
            daily_demand_std=10.0,
            avg_daily_demand=5.0,
            lead_time_days=16.0,
            lead_time_std=2.0,
            service_level=0.95,
        )
        expected = Z_95 * math.sqrt(16 * 10.0**2 + 5.0**2 * 2.0**2)
        assert result["safety_stock"] == pytest.approx(expected, abs=0.01)
        assert result["demand_variance_component"] == pytest.approx(1600.0)
        assert result["lead_time_variance_component"] == pytest.approx(100.0)

    def test_variable_lt_reduces_to_basic_when_lt_std_zero(self):
        basic = safety_stock_basic(8.0, 9.0, 0.95)["safety_stock"]
        variable = safety_stock_variable_lead_time(8.0, 4.0, 9.0, 0.0, 0.95)["safety_stock"]
        assert variable == pytest.approx(basic, abs=0.01)


class TestReorderPoint:
    def test_continuous_review(self):
        # ROP = 5 * 10 + 20 = 70
        result = reorder_point_continuous(avg_daily_demand=5.0, lead_time_days=10.0, safety_stock=20.0)
        assert result["reorder_point"] == pytest.approx(70.0)
        assert result["lead_time_demand"] == pytest.approx(50.0)

    def test_zero_safety_stock(self):
        result = reorder_point_continuous(3.0, 7.0, 0.0)
        assert result["reorder_point"] == pytest.approx(21.0)


class TestEOQ:
    def test_eoq_formula(self):
        # H = 8 * 0.25 = 2; EOQ = sqrt(2*1000*50/2) = sqrt(50000) = 223.61
        result = economic_order_quantity(
            annual_demand=1000.0, order_cost=50.0, unit_cost=8.0, holding_cost_rate=0.25
        )
        assert result["eoq"] == pytest.approx(math.sqrt(50000), abs=0.01)

    def test_eoq_cost_components_balance(self):
        # At EOQ, annual ordering cost == annual holding cost
        result = economic_order_quantity(1000.0, 50.0, 8.0, 0.25)
        assert result["annual_order_cost"] == pytest.approx(result["annual_holding_cost"], abs=0.01)
        # Total is rounded from unrounded components, so allow 2-cent slack
        assert result["total_annual_inventory_cost"] == pytest.approx(
            result["annual_order_cost"] + result["annual_holding_cost"], abs=0.02
        )

    def test_eoq_order_frequency(self):
        result = economic_order_quantity(1000.0, 50.0, 8.0, 0.25)
        assert result["order_frequency_per_year"] == pytest.approx(1000.0 / math.sqrt(50000), abs=0.01)

    def test_zero_holding_cost_returns_error_not_crash(self):
        result = economic_order_quantity(1000.0, 50.0, unit_cost=0.0)
        assert "error" in result
