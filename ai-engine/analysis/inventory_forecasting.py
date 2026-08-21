"""
Inventory Demand Forecasting Module — GrowthLabs AI
Classical statistical forecasting methods (statsmodels) for retail SKU-level demand.

Model selection across 4 algorithms using holdout MAE/MAPE:
1. Simple Exponential Smoothing — stable, no trend, no seasonality
2. Holt's Linear Trend — trending, no seasonality
3. Holt-Winters (Triple ES) — trending + seasonal (≥2 seasonal cycles)
4. Croston's Method — intermittent demand (modified for inventory use)

All methods use statsmodels where available; Croston's is implemented as a
standard classical formula (APICS/CPIM standard, not ML).
"""

import pandas as pd
import numpy as np
from typing import Optional, Literal
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt, ExponentialSmoothing


# ── Core Forecasting Methods ────────────────────────────────────────


def ses_forecast(series: np.ndarray, forecast_horizon: int = 12) -> dict:
    """
    Simple Exponential Smoothing forecast.

    Model: F(t+1) = α·D(t) + (1-α)·F(t)
    Uses statsmodels with optimized alpha parameter.

    Args:
        series: Historical demand values (monthly)
        forecast_horizon: Number of periods to forecast

    Returns:
        dict with forecasts, fitted_values, alpha, mae, mape
    """
    if len(series) < 2:
        return _fallback_forecast(series, forecast_horizon, "SES")

    try:
        # Use split for holdout validation if enough data
        if len(series) >= 6:
            train = series[:-3]
            test = series[-3:]
        else:
            train = series
            test = np.array([])

        model = SimpleExpSmoothing(train).fit(optimized=True)
        alpha = model.params.get("smoothing_level", 0.3)

        # Forecast
        forecasts = model.forecast(forecast_horizon)

        # Calculate holdout error if test is available
        if len(test) > 0:
            in_sample = model.fittedvalues
            if len(test) > len(in_sample):
                test_fc = model.forecast(len(test))[:len(test)]
            else:
                test_fc = in_sample[-len(test):]
            mae = np.mean(np.abs(test - test_fc))
            mape = np.mean(np.abs((test - test_fc) / np.maximum(np.abs(test), 1e-10))) * 100
        else:
            mae = None
            mape = None

        return {
            "model": "SES",
            "forecasts": forecasts.tolist(),
            "fitted_values": model.fittedvalues.tolist() if hasattr(model, "fittedvalues") else [],
            "alpha": float(alpha),
            "mae": float(mae) if mae is not None else None,
            "mape": float(mape) if mape is not None else None,
            "aic": float(model.aic) if hasattr(model, "aic") else None,
        }
    except Exception as e:
        return _fallback_forecast(series, forecast_horizon, f"SES-error:{e}")


def holt_forecast(series: np.ndarray, forecast_horizon: int = 12) -> dict:
    """
    Holt's Linear Trend forecast.

    Model with additive trend, optimized parameters.

    Args:
        series: Historical demand values (monthly)
        forecast_horizon: Number of periods to forecast

    Returns:
        dict with forecasts, fitted_values, params, mae, mape
    """
    if len(series) < 3:
        return _fallback_forecast(series, forecast_horizon, "Holt")

    try:
        if len(series) >= 8:
            train = series[:-3]
            test = series[-3:]
        else:
            train = series
            test = np.array([])

        model = Holt(train).fit(optimized=True)

        # Forecast
        forecasts = model.forecast(forecast_horizon)

        # Holdout error
        if len(test) > 0:
            if len(test) <= len(forecasts):
                test_fc = model.forecast(len(test))
            else:
                test_fc = model.forecast(len(test))[:len(test)]
            mae = np.mean(np.abs(test - test_fc))
            mape = np.mean(np.abs((test - test_fc) / np.maximum(np.abs(test), 1e-10))) * 100
        else:
            mae = None
            mape = None

        return {
            "model": "Holt",
            "forecasts": forecasts.tolist(),
            "fitted_values": model.fittedvalues.tolist() if hasattr(model, "fittedvalues") else [],
            "smoothing_level": float(model.params.get("smoothing_level", 0)),
            "smoothing_trend": float(model.params.get("smoothing_trend", 0)),
            "mae": float(mae) if mae is not None else None,
            "mape": float(mape) if mape is not None else None,
            "aic": float(model.aic) if hasattr(model, "aic") else None,
        }
    except Exception as e:
        return _fallback_forecast(series, forecast_horizon, f"Holt-error:{e}")


def holt_winters_forecast(
    series: np.ndarray,
    seasonal_periods: int = 12,
    forecast_horizon: int = 12,
) -> dict:
    """
    Holt-Winters Triple Exponential Smoothing forecast.

    Requires at least 2 full seasonal cycles of data.
    Uses multiplicative seasonality for retail demand data.

    Args:
        series: Historical demand values (monthly)
        seasonal_periods: Number of periods per season (default 12 for yearly)
        forecast_horizon: Number of periods to forecast

    Returns:
        dict with forecasts, fitted_values, params, mae, mape
    """
    min_required = seasonal_periods * 2
    if len(series) < min_required:
        return _fallback_forecast(
            series, forecast_horizon,
            f"HW-needs-{min_required}-periods-got-{len(series)}"
        )

    try:
        # Check for seasonality: try multiplicative first, fall back to additive
        try:
            model = ExponentialSmoothing(
                series,
                trend="add",
                seasonal="mul",
                seasonal_periods=seasonal_periods,
                initialization_method="estimated",
            ).fit(optimized=True)
            seasonal_type = "multiplicative"
        except Exception:
            model = ExponentialSmoothing(
                series,
                trend="add",
                seasonal="add",
                seasonal_periods=seasonal_periods,
                initialization_method="estimated",
            ).fit(optimized=True)
            seasonal_type = "additive"

        forecasts = model.forecast(forecast_horizon)

        # Holdout validation (use last seasonal_periods as test)
        if len(series) >= min_required + seasonal_periods:
            train = series[:-seasonal_periods]
            test = series[-seasonal_periods:]
            try:
                holdout_model = ExponentialSmoothing(
                    train,
                    trend="add",
                    seasonal=seasonal_type,
                    seasonal_periods=seasonal_periods,
                ).fit(optimized=True)
                test_fc = holdout_model.forecast(len(test))
                mae = np.mean(np.abs(test - test_fc))
                mape = np.mean(np.abs((test - test_fc) / np.maximum(np.abs(test), 1e-10))) * 100
            except Exception:
                mae, mape = None, None
        else:
            mae, mape = None, None

        return {
            "model": f"Holt-Winters ({seasonal_type})",
            "forecasts": forecasts.tolist(),
            "fitted_values": model.fittedvalues.tolist() if hasattr(model, "fittedvalues") else [],
            "seasonal_periods": seasonal_periods,
            "seasonal_type": seasonal_type,
            "mae": float(mae) if mae is not None else None,
            "mape": float(mape) if mape is not None else None,
            "aic": float(model.aic) if hasattr(model, "aic") else None,
        }
    except Exception as e:
        return _fallback_forecast(series, forecast_horizon, f"HW-error:{e}")


def croston_forecast(series: np.ndarray, forecast_horizon: int = 12) -> dict:
    """
    Croston's Method for intermittent demand forecasting.

    Separately smooths non-zero demand sizes and inter-demand intervals.
    Standard APICS/CPIM method for lumpy/sporadic demand.

    Args:
        series: Historical demand values (monthly)
        forecast_horizon: Number of periods to forecast

    Returns:
        dict with forecasts, fitted_values, params
    """
    if len(series) < 4:
        return _fallback_forecast(series, forecast_horizon, "Croston")

    try:
        # Identify non-zero periods
        non_zero = series[series > 0]
        demand_mask = series > 0
        intervals = []

        last_idx = -1
        for i, val in enumerate(series):
            if val > 0:
                if last_idx >= 0:
                    intervals.append(i - last_idx)
                last_idx = i

        if len(non_zero) < 2:
            return _fallback_forecast(series, forecast_horizon, "Croston")

        # Croston's smoothing (alpha = 0.1 standard for intermittent)
        alpha = 0.1
        smooth_demand = np.mean(non_zero[:3]) if len(non_zero) >= 3 else non_zero[0]
        smooth_interval = np.mean(intervals[:3]) if len(intervals) >= 3 else intervals[0] if intervals else 1

        # Smooth through all observed data
        fitted = np.zeros(len(series))
        demand_idx = 0
        for i in range(len(series)):
            if series[i] > 0:
                smooth_demand = alpha * series[i] + (1 - alpha) * smooth_demand
                if demand_idx < len(intervals):
                    smooth_interval = alpha * intervals[demand_idx] + (1 - alpha) * smooth_interval
                    demand_idx += 1
            # Fitted value is the Croston estimate
            fitted[i] = smooth_demand / smooth_interval if smooth_interval > 0 else 0

        # Forecast: constant = smoothed_demand / smoothed_interval
        croston_rate = smooth_demand / smooth_interval if smooth_interval > 0 else 0
        forecasts = np.full(forecast_horizon, croston_rate)

        # MAE on fitted vs actual
        mae = float(np.mean(np.abs(series - fitted)))
        mape = float(np.mean(np.abs((series - fitted) / np.maximum(np.abs(series), 1e-10))) * 100)

        return {
            "model": "Croston",
            "forecasts": forecasts.tolist(),
            "fitted_values": fitted.tolist(),
            "smoothed_demand": float(smooth_demand),
            "smoothed_interval": float(smooth_interval),
            "croston_rate": float(croston_rate),
            "mae": mae,
            "mape": mape,
            "aic": None,  # Croston has no information criterion
        }
    except Exception as e:
        return _fallback_forecast(series, forecast_horizon, f"Croston-error:{e}")


# ── Model Selection ─────────────────────────────────────────────────


def select_best_model(
    series: np.ndarray,
    seasonal_periods: int = 12,
    forecast_horizon: int = 12,
    prefer_parsimony: bool = True,
) -> dict:
    """
    Select the best forecasting model for a given demand series.

    Runs all applicable models and selects by holdout MAE (primary) or
    in-sample MAPE (secondary). Prefers simpler models when errors are close
    (parsimony principle).

    Args:
        series: Historical monthly demand values
        seasonal_periods: Seasonal period length
        forecast_horizon: Number of steps to forecast
        prefer_parsimony: If True, penalize HW by 10% to prefer Holt/SES

    Returns:
        dict with 'best_model' name, all model results, and selected forecasts
    """
    results = {}

    # SES (always applicable)
    results["SES"] = ses_forecast(series, forecast_horizon)

    # Holt (≥3 data points)
    if len(series) >= 3:
        results["Holt"] = holt_forecast(series, forecast_horizon)

    # Holt-Winters (≥2 seasonal cycles)
    min_hw = seasonal_periods * 2
    if len(series) >= min_hw:
        results["Holt-Winters"] = holt_winters_forecast(series, seasonal_periods, forecast_horizon)

    # Croston (≥4 data points, some zeros)
    if len(series) >= 4 and np.any(series == 0):
        results["Croston"] = croston_forecast(series, forecast_horizon)

    if not results:
        return {
            "best_model": "Fallback",
            "all_models": {},
            "forecasts": np.full(forecast_horizon, np.mean(series) if len(series) > 0 else 0).tolist(),
            "mae": None,
            "mape": None,
        }

    # Score models by holdout MAE (lower is better), fall back to MAPE
    def _score(result_dict: dict) -> float:
        """Lower score is better. Prefer MAE over MAPE."""
        if result_dict.get("mae") is not None and not np.isnan(result_dict["mae"]):
            score = result_dict["mae"]
        elif result_dict.get("mape") is not None and not np.isnan(result_dict["mape"]):
            score = result_dict["mape"]
        else:
            return float("inf")

        # Parsimony penalty: prefer simpler models if errors are close
        if prefer_parsimony:
            model_name = result_dict.get("model", "")
            if "Holt-Winters" in model_name:
                score *= 1.10  # 10% penalty for complexity
            elif "Holt" in model_name:
                score *= 1.03  # 3% penalty

        return score

    # Find best model
    best_name = min(results.keys(), key=lambda k: _score(results[k]))
    best = results[best_name]

    return {
        "best_model": best.get("model", best_name),
        "all_models": {k: {"mae": v.get("mae"), "mape": v.get("mape"), "aic": v.get("aic")} for k, v in results.items()},
        "forecasts": best.get("forecasts", []),
        "fitted_values": best.get("fitted_values", []),
        "mae": best.get("mae"),
        "mape": best.get("mape"),
    }


# ── Helpers ─────────────────────────────────────────────────────────


def _fallback_forecast(series: np.ndarray, horizon: int, reason: str) -> dict:
    """Fallback: use simple moving average when model can't be fit."""
    mean_val = float(np.mean(series)) if len(series) > 0 else 0
    forecasts = [mean_val] * horizon
    mae = float(np.mean(np.abs(series - mean_val))) if len(series) > 0 else None
    return {
        "model": f"Fallback-MA ({reason})",
        "forecasts": forecasts,
        "fitted_values": [mean_val] * len(series) if len(series) > 0 else [],
        "mae": mae,
        "mape": None,
        "aic": None,
        "fallback_reason": reason,
    }


def aggregate_to_monthly(sales_df: pd.DataFrame, sku: str) -> np.ndarray:
    """Aggregate daily SKU sales to monthly time series."""
    df = sales_df[sales_df["sku"] == sku].copy()
    df["date"] = pd.to_datetime(df["date"])
    df["year_month"] = df["date"].dt.to_period("M")
    monthly = df.groupby("year_month")["quantity"].sum()
    return monthly.values


def run_inventory_forecasting(
    sales_df: pd.DataFrame,
    products_df: pd.DataFrame,
    sku_list: Optional[list[str]] = None,
    seasonal_periods: int = 12,
    forecast_horizon: int = 6,
    max_skus: int = 50,
) -> dict:
    """
    Run demand forecasting for the top N SKUs.

    Args:
        sales_df: Sales transactions with sku, quantity, date, unit_price
        products_df: Products master data
        sku_list: Optional list of SKUs to forecast (if None, picks top by revenue)
        seasonal_periods: Seasonal cycle length
        forecast_horizon: Forecast horizon in months
        max_skus: Maximum number of SKUs to forecast

    Returns:
        dict with per-SKU forecasts and model selection summary
    """
    # Determine which SKUs to forecast
    if sku_list:
        skus = sku_list[:max_skus]
    else:
        # Pick top SKUs by revenue
        sku_revenue = sales_df.groupby("sku")["quantity"].sum()
        skus = sku_revenue.nlargest(max_skus).index.tolist()

    forecasts = {}
    model_counts = {}

    for sku in skus:
        series = aggregate_to_monthly(sales_df, sku)
        if len(series) < 2:
            forecasts[sku] = {"error": f"Insufficient data ({len(series)} months)"}
            continue

        result = select_best_model(
            series,
            seasonal_periods=seasonal_periods,
            forecast_horizon=forecast_horizon,
        )
        forecasts[sku] = result

        # Track model usage
        model_name = result.get("best_model", "Unknown")
        model_counts[model_name] = model_counts.get(model_name, 0) + 1

    return {
        "forecasts": forecasts,
        "model_counts": model_counts,
        "forecast_horizon_months": forecast_horizon,
        "seasonal_periods": seasonal_periods,
        "skus_forecasted": len(forecasts),
    }
