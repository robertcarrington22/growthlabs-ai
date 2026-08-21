"""Regression tests for ABC and XYZ classification (analysis/inventory_classification.py).

classify_xyz previously broke on pandas 2.x groupby — these tests pin its contract.
"""

import pandas as pd
import pytest

from analysis.inventory_classification import classify_abc, classify_xyz


def _monthly_sales(sku: str, monthly_quantities: list[int]) -> pd.DataFrame:
    """One sales row per month for a SKU, starting Jan 2025."""
    dates = pd.date_range("2025-01-15", periods=len(monthly_quantities), freq="MS")
    return pd.DataFrame({
        "sku": [sku] * len(monthly_quantities),
        "date": dates,
        "quantity": monthly_quantities,
    })


class TestClassifyXYZ:
    def _build_df(self):
        # Stable: CV = 0                       -> X (CV < 0.5)
        stable = _monthly_sales("SKU-STABLE", [10, 10, 10, 10, 10, 10])
        # Variable: mean 6, sample std ~4.38, CV ~0.73 -> Y (0.5 <= CV < 1.0)
        variable = _monthly_sales("SKU-VARIABLE", [10, 2, 10, 2, 10, 2])
        # Erratic: mean ~4.17, sample std ~7.76, CV ~1.86 -> Z (CV >= 1.0)
        erratic = _monthly_sales("SKU-ERRATIC", [20, 1, 1, 1, 1, 1])
        # Insufficient history: only 2 periods -> U (below min_periods=4)
        sparse = _monthly_sales("SKU-SPARSE", [5, 5])
        return pd.concat([stable, variable, erratic, sparse], ignore_index=True)

    def test_returns_dataframe_with_expected_columns(self):
        result = classify_xyz(self._build_df())
        assert isinstance(result, pd.DataFrame)
        for col in ["sku", "mean_demand", "std_demand", "cv", "xyz_class"]:
            assert col in result.columns, f"missing column: {col}"

    def test_class_assignment(self):
        result = classify_xyz(self._build_df())
        classes = result.set_index("sku")["xyz_class"].to_dict()
        assert classes["SKU-STABLE"] == "X"
        assert classes["SKU-VARIABLE"] == "Y"
        assert classes["SKU-ERRATIC"] == "Z"
        assert classes["SKU-SPARSE"] == "U"

    def test_cv_values(self):
        result = classify_xyz(self._build_df()).set_index("sku")
        assert result.loc["SKU-STABLE", "cv"] == pytest.approx(0.0)
        assert result.loc["SKU-VARIABLE", "cv"] == pytest.approx(0.7303, abs=1e-3)
        assert result.loc["SKU-ERRATIC", "cv"] == pytest.approx(1.8616, abs=1e-3)

    def test_multiple_transactions_per_month_are_aggregated(self):
        # 2 rows of 5 units in each month == one row of 10 -> CV 0 -> X
        dates = pd.date_range("2025-01-01", periods=6, freq="MS")
        rows = []
        for d in dates:
            rows.append({"sku": "SKU-SPLIT", "date": d, "quantity": 5})
            rows.append({"sku": "SKU-SPLIT", "date": d + pd.Timedelta(days=10), "quantity": 5})
        result = classify_xyz(pd.DataFrame(rows))
        assert result.iloc[0]["xyz_class"] == "X"
        assert result.iloc[0]["mean_demand"] == pytest.approx(10.0)


class TestClassifyABC:
    def _build_df(self):
        # Revenue distribution (total 100):
        # SKU1=60 (cum .60 A), SKU2=15 (cum .75 A), SKU3=15 (cum .90 B),
        # SKU4=6 (cum .96 C), SKU5=4 (cum 1.00 C)
        return pd.DataFrame({
            "sku": ["SKU1", "SKU2", "SKU3", "SKU4", "SKU5"],
            "revenue": [60.0, 15.0, 15.0, 6.0, 4.0],
        })

    def test_abc_split(self):
        result = classify_abc(self._build_df())
        classes = result.set_index("sku")["abc_class"].to_dict()
        assert classes["SKU1"] == "A"
        assert classes["SKU2"] == "A"
        assert classes["SKU3"] == "B"
        assert classes["SKU4"] == "C"
        assert classes["SKU5"] == "C"

    def test_sorted_descending_and_cumulative(self):
        result = classify_abc(self._build_df())
        assert list(result["total_value"]) == sorted(result["total_value"], reverse=True)
        assert result["cumulative_pct"].iloc[-1] == pytest.approx(1.0)
        assert result["pct_of_total"].sum() == pytest.approx(1.0)

    def test_aggregates_multiple_rows_per_sku(self):
        df = pd.DataFrame({
            "sku": ["SKU1", "SKU1", "SKU2"],
            "revenue": [30.0, 30.0, 40.0],
        })
        result = classify_abc(df)
        assert result[result["sku"] == "SKU1"]["total_value"].iloc[0] == pytest.approx(60.0)
        assert len(result) == 2
