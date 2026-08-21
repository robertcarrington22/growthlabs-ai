"""
Data ingestion module for GrowthLabs AI Revenue Analysis Engine.
Accepts CSV transaction/customer data and normalizes it into the analysis schema.
"""

import pandas as pd
import numpy as np
from typing import Optional
import json
import os


class IngestionResult:
    """Container for ingested and validated data."""

    def __init__(
        self,
        transactions: pd.DataFrame,
        customers: pd.DataFrame,
        validation_errors: list[str],
        warnings: list[str],
    ):
        self.transactions = transactions
        self.customers = customers
        self.validation_errors = validation_errors
        self.warnings = warnings

    @property
    def is_valid(self) -> bool:
        return len(self.validation_errors) == 0

    def summary(self) -> dict:
        return {
            "customers_loaded": len(self.customers),
            "transactions_loaded": len(self.transactions),
            "date_range": {
                "min": str(self.transactions["date"].min()) if len(self.transactions) > 0 else None,
                "max": str(self.transactions["date"].max()) if len(self.transactions) > 0 else None,
            },
            "unique_customers_with_txns": self.transactions["customer_id"].nunique(),
            "validation_errors": self.validation_errors,
            "warnings": self.warnings,
        }


def ingest_transactions(filepath: str) -> pd.DataFrame:
    """
    Load and normalize transaction CSV data.

    Expected columns: transaction_id, customer_id, date, service_name, amount, estimated_margin_pct, quantity
    """
    df = pd.read_csv(filepath)

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Ensure required columns exist
    required = {"transaction_id", "customer_id", "date", "amount"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Found columns: {list(df.columns)}")

    # Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop rows with invalid dates
    bad_dates = df["date"].isna().sum()
    if bad_dates > 0:
        df = df.dropna(subset=["date"])
        print(f"⚠️  Dropped {bad_dates} rows with unparseable dates")

    # Ensure amount is numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    bad_amounts = df["amount"].isna().sum()
    if bad_amounts > 0:
        df = df.dropna(subset=["amount"])
        print(f"⚠️  Dropped {bad_amounts} rows with non-numeric amounts")

    # Fill defaults for optional columns
    if "quantity" not in df.columns:
        df["quantity"] = 1
    else:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1).astype(int)

    if "estimated_margin_pct" not in df.columns:
        df["estimated_margin_pct"] = np.nan
    else:
        df["estimated_margin_pct"] = pd.to_numeric(df["estimated_margin_pct"], errors="coerce")

    if "service_name" not in df.columns:
        df["service_name"] = "Unknown"

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    return df


def ingest_customers(filepath: str) -> pd.DataFrame:
    """
    Load and normalize customer CSV data.

    Expected columns: customer_id, company_name, industry, acquisition_channel,
                      acquisition_date, churn_date, is_churned, annual_revenue, employees
    """
    df = pd.read_csv(filepath)

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Ensure required columns exist
    required = {"customer_id"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Found columns: {list(df.columns)}")

    # Parse dates
    for col in ["acquisition_date", "churn_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Ensure is_churned is boolean
    if "is_churned" in df.columns:
        df["is_churned"] = df["is_churned"].astype(bool)
    else:
        df["is_churned"] = False

    # Ensure numeric
    if "annual_revenue" in df.columns:
        df["annual_revenue"] = pd.to_numeric(df["annual_revenue"], errors="coerce")

    if "employees" in df.columns:
        df["employees"] = pd.to_numeric(df["employees"], errors="coerce").fillna(0).astype(int)

    return df


def load_data(
    transactions_path: str,
    customers_path: Optional[str] = None,
) -> IngestionResult:
    """
    Full ingestion pipeline: load, validate, and normalize data.

    Args:
        transactions_path: Path to transactions CSV
        customers_path: Optional path to customers CSV

    Returns:
        IngestionResult with validated dataframes and any issues found.
    """
    errors = []
    warnings = []

    # ── Load transactions ──
    if not os.path.exists(transactions_path):
        return IngestionResult(
            pd.DataFrame(), pd.DataFrame(),
            [f"File not found: {transactions_path}"], []
        )

    try:
        transactions = ingest_transactions(transactions_path)
    except Exception as e:
        return IngestionResult(
            pd.DataFrame(), pd.DataFrame(),
            [f"Failed to load transactions: {e}"], []
        )

    if len(transactions) == 0:
        errors.append("Transactions file is empty after parsing")

    # ── Load customers ──
    customers = pd.DataFrame()
    if customers_path and os.path.exists(customers_path):
        try:
            customers = ingest_customers(customers_path)
        except Exception as e:
            warnings.append(f"Failed to load customers: {e}. Proceeding with transactions only.")

    # ── Validation ──
    if len(customers) > 0:
        # Check for orphan transactions
        txn_custs = set(transactions["customer_id"].unique())
        cust_ids = set(customers["customer_id"].unique())
        orphans = txn_custs - cust_ids
        if orphans:
            warnings.append(
                f"{len(orphans)} customers in transactions have no matching customer record"
            )

        # Flag customers with no transactions
        inactive = cust_ids - txn_custs
        if inactive:
            warnings.append(f"{len(inactive)} customer records have zero transactions")

    # ── Negative amounts check ──
    negatives = transactions[transactions["amount"] < 0]
    if len(negatives) > 0:
        warnings.append(f"Found {len(negatives)} transactions with negative amounts (credits/refunds?)")

    return IngestionResult(
        transactions=transactions,
        customers=customers,
        validation_errors=errors,
        warnings=warnings,
    )


# ── Retail / Inventory Data Ingestion ────────────────────────────────


class RetailDataBundle:
    """
    Container for retail inventory data.
    Mirrors IngestionResult but for the inventory analysis pipeline.
    """

    def __init__(
        self,
        sales: pd.DataFrame,
        inventory_snapshots: pd.DataFrame,
        products: pd.DataFrame,
        purchase_orders: pd.DataFrame,
        validation_errors: list[str],
        warnings: list[str],
    ):
        self.sales = sales
        self.inventory_snapshots = inventory_snapshots
        self.products = products
        self.purchase_orders = purchase_orders
        self.validation_errors = validation_errors
        self.warnings = warnings

    @property
    def is_valid(self) -> bool:
        return len(self.validation_errors) == 0

    def summary(self) -> dict:
        return {
            "sales_loaded": len(self.sales),
            "products_loaded": len(self.products),
            "inventory_snapshots": len(self.inventory_snapshots),
            "purchase_orders": len(self.purchase_orders),
            "unique_skus_sold": int(self.sales["sku"].nunique()) if len(self.sales) > 0 else 0,
            "unique_skus_in_inventory": int(self.inventory_snapshots["sku"].nunique()) if len(self.inventory_snapshots) > 0 else 0,
            "date_range_sales": {
                "min": str(self.sales["date"].min()) if len(self.sales) > 0 else None,
                "max": str(self.sales["date"].max()) if len(self.sales) > 0 else None,
            },
            "validation_errors": self.validation_errors,
            "warnings": self.warnings,
        }


def ingest_retail_sales(filepath: str) -> pd.DataFrame:
    """
    Load and normalize retail sales CSV data.

    Expected columns: date, sku, quantity, unit_price, [unit_cost, order_id, location]
    """
    df = pd.read_csv(filepath)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    required = {"date", "sku", "quantity"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in sales: {missing}. Found: {list(df.columns)}")

    # Parse date
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    bad_dates = df["date"].isna().sum()
    if bad_dates > 0:
        df = df.dropna(subset=["date"])

    # Ensure quantity and price are numeric
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    if "unit_price" in df.columns:
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0)
    else:
        df["unit_price"] = 0.0

    if "unit_cost" in df.columns:
        df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce")
    if "order_id" not in df.columns:
        df["order_id"] = ""

    return df.sort_values("date").reset_index(drop=True)


def ingest_inventory_snapshots(filepath: str) -> pd.DataFrame:
    """
    Load and normalize inventory snapshot CSV.

    Expected columns: date, sku, on_hand, [unit_cost, location]
    """
    df = pd.read_csv(filepath)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    required = {"sku", "on_hand"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in inventory: {missing}. Found: {list(df.columns)}")

    # Parse optional date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    else:
        df["date"] = pd.Timestamp.now()

    df["on_hand"] = pd.to_numeric(df["on_hand"], errors="coerce").fillna(0).astype(int)
    if "unit_cost" in df.columns:
        df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce")

    return df


def ingest_products(filepath: str) -> pd.DataFrame:
    """
    Load and normalize product master CSV.

    Expected columns: sku, product_name, [category, unit_cost, unit_price]
    """
    df = pd.read_csv(filepath)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    required = {"sku"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required column 'sku' in products. Found: {list(df.columns)}")

    # Ensure numeric fields
    for col in ["unit_cost", "unit_price"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            df[col] = 0.0

    if "product_name" not in df.columns:
        df["product_name"] = df["sku"]
    if "category" not in df.columns:
        df["category"] = "Uncategorized"

    return df


def ingest_purchase_orders(filepath: str) -> pd.DataFrame:
    """
    Load and normalize purchase order CSV (optional).

    Expected columns: po_id, sku, order_date, [received_date, quantity, unit_cost]
    """
    df = pd.read_csv(filepath)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    required = {"po_id", "sku", "order_date"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in purchase_orders: {missing}. Found: {list(df.columns)}")

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    if "received_date" in df.columns:
        df["received_date"] = pd.to_datetime(df["received_date"], errors="coerce")

    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    else:
        df["quantity"] = 0

    return df


def load_retail_data(
    sales_path: str,
    inventory_path: str,
    products_path: str,
    purchase_orders_path: Optional[str] = None,
) -> RetailDataBundle:
    """
    Full retail inventory ingestion pipeline.

    Args:
        sales_path: Path to retail sales CSV
        inventory_path: Path to inventory snapshots CSV
        products_path: Path to products master CSV
        purchase_orders_path: Optional path to purchase orders CSV

    Returns:
        RetailDataBundle with validated dataframes
    """
    errors = []
    warnings = []

    # Check required files exist
    for path, name in [(sales_path, "sales"), (inventory_path, "inventory"), (products_path, "products")]:
        if not os.path.exists(path):
            return RetailDataBundle(
                pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),
                [f"File not found: {path}"], []
            )

    # Load each dataset
    try:
        sales = ingest_retail_sales(sales_path)
    except Exception as e:
        return RetailDataBundle(
            pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),
            [f"Failed to load sales: {e}"], []
        )

    try:
        inventory = ingest_inventory_snapshots(inventory_path)
    except Exception as e:
        warnings.append(f"Failed to load inventory: {e}")
        inventory = pd.DataFrame()

    try:
        products = ingest_products(products_path)
    except Exception as e:
        warnings.append(f"Failed to load products: {e}")
        products = pd.DataFrame()

    purchase_orders = pd.DataFrame()
    if purchase_orders_path and os.path.exists(purchase_orders_path):
        try:
            purchase_orders = ingest_purchase_orders(purchase_orders_path)
        except Exception as e:
            warnings.append(f"Failed to load purchase orders: {e}")

    # ── Validation ──
    if len(sales) == 0:
        errors.append("Sales file is empty after parsing")

    # Check for orphan SKUs (sales items not in product master)
    if len(products) > 0:
        sold_skus = set(sales["sku"].unique())
        product_skus = set(products["sku"].unique())
        orphans = sold_skus - product_skus
        if orphans:
            warnings.append(f"{len(orphans)} SKUs in sales have no matching product record")

    # Check for inventory items not in products
    if len(inventory) > 0 and len(products) > 0:
        inv_skus = set(inventory["sku"].unique())
        inv_orphans = inv_skus - product_skus
        if inv_orphans:
            warnings.append(f"{len(inv_orphans)} SKUs in inventory have no matching product record")

    # Negative quantities
    neg = sales[sales["quantity"] < 0]
    if len(neg) > 0:
        warnings.append(f"Found {len(neg)} sales with negative quantities (returns?)")

    return RetailDataBundle(
        sales=sales,
        inventory_snapshots=inventory,
        products=products,
        purchase_orders=purchase_orders,
        validation_errors=errors,
        warnings=warnings,
    )
