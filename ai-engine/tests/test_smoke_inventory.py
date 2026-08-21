"""End-to-end smoke test: retail inventory audit pipeline."""

import json

import pandas as pd
import pytest

from sample_data_generator import generate_retail_sample_data
from data_ingestion import load_retail_data
from analysis.inventory_report import run_inventory_audit


@pytest.fixture(scope="module")
def inventory_result(tmp_path_factory):
    """Generate retail sample data, ingest it, and run the full inventory audit once."""
    tmp = tmp_path_factory.mktemp("inventory_smoke")
    sales_path, inv_path, prods_path = generate_retail_sample_data(
        num_sales=4000,
        output_dir=str(tmp / "retail_data"),
    )
    bundle = load_retail_data(sales_path, inv_path, prods_path)
    assert bundle.is_valid, f"Retail ingestion failed: {bundle.validation_errors}"
    result = run_inventory_audit(bundle.sales, bundle.inventory_snapshots, bundle.products)
    assert "error" not in result, f"Inventory audit returned error: {result.get('error')}"
    return result


def test_executive_summary_with_headline(inventory_result):
    exec_summary = inventory_result.get("executive_summary")
    assert isinstance(exec_summary, dict) and exec_summary
    headline = exec_summary.get("headline")
    assert isinstance(headline, str) and len(headline) > 0
    # Headline should carry dollar figures for the US market
    assert "$" in headline


def test_top_20_actions_non_empty(inventory_result):
    actions = inventory_result.get("top_20_actions")
    assert isinstance(actions, list)
    assert len(actions) > 0, "top_20_actions is empty"
    assert len(actions) <= 20
    for action in actions:
        assert "sku" in action
        assert "issue" in action
        assert "action" in action


def test_reorder_policy_sheet_present(inventory_result):
    sheet = inventory_result.get("reorder_policy_sheet")
    assert isinstance(sheet, dict)
    assert sheet.get("policy_count", 0) > 0
    policies = sheet.get("policies", [])
    assert len(policies) > 0
    for pol in policies[:5]:
        assert "reorder_point" in pol
        assert "eoq" in pol
        assert "safety_stock" in pol


def test_dollar_quantification_has_4_keys(inventory_result):
    dq = inventory_result.get("dollar_quantification")
    assert isinstance(dq, dict)
    expected_keys = {
        "total_cash_trapped_in_dead_stock",
        "annual_carrying_cost_waste",
        "annual_stockout_revenue_loss",
        "total_recoverable_value",
    }
    assert expected_keys == set(dq.keys())
    for key in expected_keys:
        assert isinstance(dq[key], (int, float)), f"{key} is not numeric"


def test_methodology_present(inventory_result):
    methodology = inventory_result.get("methodology")
    assert isinstance(methodology, dict) and methodology
    assert "abc_classification" in methodology
    assert "eoq" in methodology


def test_no_euro_symbol_anywhere(inventory_result):
    serialized = json.dumps(inventory_result, default=str, ensure_ascii=False)
    assert "€" not in serialized


def test_audit_works_without_demand_pattern_column():
    """Real client product CSVs have no 'demand_pattern' column — the audit must not crash.

    Regression guard for analysis/inventory_report.py:_build_seasonal_recommendations,
    which previously indexed products_df['demand_pattern'] unconditionally.
    """
    dates = pd.date_range("2025-01-01", periods=180, freq="D")
    sales = pd.DataFrame({
        "date": list(dates) * 2,
        "sku": ["SKU-A"] * 180 + ["SKU-B"] * 180,
        "quantity": [3] * 180 + [1] * 180,
        "unit_price": [20.0] * 180 + [10.0] * 180,
    })
    inventory = pd.DataFrame({
        "date": [dates[-1]] * 2,
        "sku": ["SKU-A", "SKU-B"],
        "on_hand": [40, 15],
        "unit_cost": [12.0, 6.0],
    })
    products = pd.DataFrame({
        "sku": ["SKU-A", "SKU-B"],
        "product_name": ["Widget A", "Widget B"],
        "unit_cost": [12.0, 6.0],
        "unit_price": [20.0, 10.0],
    })

    result = run_inventory_audit(sales, inventory, products)
    assert "error" not in result
    assert result.get("seasonal_prebuy_recommendations") == []
    assert "executive_summary" in result
