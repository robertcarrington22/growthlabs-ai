"""Validation tests: data_ingestion must return validation errors, not crash."""

import pandas as pd

from data_ingestion import load_data, load_retail_data


def _write_csv(path, df):
    df.to_csv(path, index=False)
    return str(path)


class TestRevenueIngestion:
    def test_missing_required_columns_is_validation_error(self, tmp_path):
        # No 'amount' column -> validation error, not an exception
        bad = pd.DataFrame({
            "transaction_id": ["T1"],
            "customer_id": ["C1"],
            "date": ["2025-01-01"],
        })
        result = load_data(_write_csv(tmp_path / "txns.csv", bad))
        assert not result.is_valid
        assert any("amount" in e for e in result.validation_errors)

    def test_missing_file_is_validation_error(self, tmp_path):
        result = load_data(str(tmp_path / "does_not_exist.csv"))
        assert not result.is_valid
        assert any("not found" in e.lower() for e in result.validation_errors)

    def test_valid_minimal_file_loads(self, tmp_path):
        good = pd.DataFrame({
            "transaction_id": ["T1", "T2"],
            "customer_id": ["C1", "C2"],
            "date": ["2025-01-01", "2025-02-01"],
            "amount": [100.0, 250.0],
        })
        result = load_data(_write_csv(tmp_path / "txns.csv", good))
        assert result.is_valid
        assert len(result.transactions) == 2
        # Optional columns get defaults
        assert "quantity" in result.transactions.columns
        assert "service_name" in result.transactions.columns

    def test_bad_customers_file_downgrades_to_warning(self, tmp_path):
        txns = pd.DataFrame({
            "transaction_id": ["T1"],
            "customer_id": ["C1"],
            "date": ["2025-01-01"],
            "amount": [100.0],
        })
        bad_customers = pd.DataFrame({"company_name": ["Acme"]})  # no customer_id
        result = load_data(
            _write_csv(tmp_path / "txns.csv", txns),
            _write_csv(tmp_path / "customers.csv", bad_customers),
        )
        # Transactions still valid; customers failure is a warning, not fatal
        assert result.is_valid
        assert any("customers" in w.lower() for w in result.warnings)


class TestRetailIngestion:
    def _good_paths(self, tmp_path):
        sales = pd.DataFrame({
            "date": ["2025-01-01", "2025-01-02"],
            "sku": ["SKU-1", "SKU-2"],
            "quantity": [3, 5],
            "unit_price": [10.0, 20.0],
        })
        inventory = pd.DataFrame({
            "date": ["2025-01-02", "2025-01-02"],
            "sku": ["SKU-1", "SKU-2"],
            "on_hand": [10, 0],
            "unit_cost": [6.0, 12.0],
        })
        products = pd.DataFrame({
            "sku": ["SKU-1", "SKU-2"],
            "product_name": ["One", "Two"],
            "unit_cost": [6.0, 12.0],
            "unit_price": [10.0, 20.0],
        })
        return (
            _write_csv(tmp_path / "sales.csv", sales),
            _write_csv(tmp_path / "inventory.csv", inventory),
            _write_csv(tmp_path / "products.csv", products),
        )

    def test_valid_bundle_loads(self, tmp_path):
        s, i, p = self._good_paths(tmp_path)
        bundle = load_retail_data(s, i, p)
        assert bundle.is_valid
        assert len(bundle.sales) == 2
        assert len(bundle.products) == 2

    def test_sales_missing_sku_is_validation_error(self, tmp_path):
        _, i, p = self._good_paths(tmp_path)
        bad_sales = pd.DataFrame({
            "date": ["2025-01-01"],
            "quantity": [3],
            "unit_price": [10.0],
        })
        bundle = load_retail_data(_write_csv(tmp_path / "bad_sales.csv", bad_sales), i, p)
        assert not bundle.is_valid
        assert any("sales" in e.lower() for e in bundle.validation_errors)

    def test_missing_sales_file_is_validation_error(self, tmp_path):
        _, i, p = self._good_paths(tmp_path)
        bundle = load_retail_data(str(tmp_path / "nope.csv"), i, p)
        assert not bundle.is_valid
        assert any("not found" in e.lower() for e in bundle.validation_errors)

    def test_inventory_missing_on_hand_downgrades_to_warning(self, tmp_path):
        s, _, p = self._good_paths(tmp_path)
        bad_inv = pd.DataFrame({"date": ["2025-01-02"], "sku": ["SKU-1"]})  # no on_hand
        bundle = load_retail_data(s, _write_csv(tmp_path / "bad_inv.csv", bad_inv), p)
        # Sales are still usable; inventory failure is a warning, not fatal
        assert bundle.is_valid
        assert any("inventory" in w.lower() for w in bundle.warnings)
