"""Unit tests: dead-stock detection and core KPI math (analysis/inventory_kpis.py)."""

import pandas as pd
import pytest

from analysis.inventory_kpis import (
    dead_stock_identification,
    inventory_turns,
    weeks_of_cover,
)


class TestDeadStockIdentification:
    def _build_data(self):
        # SKU-LIVE sells throughout; SKU-DEAD last sold 8 months before the latest date;
        # SKU-EMPTY is dead but has zero on-hand (should NOT be flagged).
        sales = pd.DataFrame({
            "date": ["2025-01-10", "2025-06-15", "2025-12-01", "2025-04-01", "2025-04-10"],
            "sku": ["SKU-LIVE", "SKU-LIVE", "SKU-LIVE", "SKU-DEAD", "SKU-EMPTY"],
            "quantity": [5, 3, 4, 2, 1],
        })
        inventory = pd.DataFrame({
            "sku": ["SKU-LIVE", "SKU-DEAD", "SKU-EMPTY"],
            "on_hand": [30, 25, 0],
            "unit_cost": [10.0, 8.0, 5.0],
        })
        return sales, inventory

    def test_dead_sku_with_stock_is_flagged(self):
        sales, inventory = self._build_data()
        result = dead_stock_identification(sales, inventory, no_sale_months=6)
        dead_skus = [d["sku"] for d in result["dead_stock_list_top_20"]]
        assert "SKU-DEAD" in dead_skus

    def test_live_sku_not_flagged(self):
        sales, inventory = self._build_data()
        result = dead_stock_identification(sales, inventory, no_sale_months=6)
        dead_skus = [d["sku"] for d in result["dead_stock_list_top_20"]]
        assert "SKU-LIVE" not in dead_skus

    def test_zero_on_hand_dead_sku_not_flagged(self):
        sales, inventory = self._build_data()
        result = dead_stock_identification(sales, inventory, no_sale_months=6)
        dead_skus = [d["sku"] for d in result["dead_stock_list_top_20"]]
        assert "SKU-EMPTY" not in dead_skus

    def test_dead_stock_value_arithmetic(self):
        sales, inventory = self._build_data()
        result = dead_stock_identification(sales, inventory, no_sale_months=6)
        # Only SKU-DEAD: 25 units * $8.00 = $200
        assert result["dead_sku_count"] == 1
        assert result["dead_stock_units"] == 25
        assert result["dead_stock_value"] == pytest.approx(200.0)

    def test_no_dead_stock_when_all_recently_sold(self):
        sales = pd.DataFrame({
            "date": ["2025-11-01", "2025-11-15"],
            "sku": ["SKU-A", "SKU-B"],
            "quantity": [1, 1],
        })
        inventory = pd.DataFrame({
            "sku": ["SKU-A", "SKU-B"],
            "on_hand": [10, 10],
            "unit_cost": [5.0, 5.0],
        })
        result = dead_stock_identification(sales, inventory, no_sale_months=6)
        assert result["dead_sku_count"] == 0
        assert result["dead_stock_value"] == pytest.approx(0.0)


class TestKpiMath:
    def test_inventory_turns(self):
        result = inventory_turns(annual_cogs=120000.0, average_inventory_value=20000.0)
        assert result["value"] == pytest.approx(6.0)
        assert result["dsi_days"] == pytest.approx(365 / 6.0, abs=0.1)

    def test_inventory_turns_zero_inventory_errors(self):
        assert "error" in inventory_turns(120000.0, 0.0)

    def test_weeks_of_cover(self):
        result = weeks_of_cover(current_stock_units=120.0, avg_weekly_demand=20.0)
        assert result["value"] == pytest.approx(6.0)
