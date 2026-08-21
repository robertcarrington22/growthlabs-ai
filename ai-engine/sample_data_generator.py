"""
Sample data generator for GrowthLabs AI Revenue Analysis Engine.
Generates realistic synthetic business data for demo and testing purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os


def generate_sample_data(
    num_customers: int = 200,
    num_transactions: int = 5000,
    start_date: str = "2024-01-01",
    end_date: str = "2025-12-31",
    seed: int = 42,
    output_dir: str = "sample_data",
) -> tuple[str, str]:
    """
    Generate synthetic customer and transaction CSV files.

    Args:
        num_customers: Number of customers to generate
        num_transactions: Number of transactions to generate
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        seed: Random seed for reproducibility
        output_dir: Directory to write CSV files

    Returns:
        Tuple of (customers_filepath, transactions_filepath)
    """
    np.random.seed(seed)
    random.seed(seed)

    os.makedirs(output_dir, exist_ok=True)

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_range_days = (end - start).days

    # ── Customer Data ────────────────────────────────────────────
    industries = [
        "Digital Agency",
        "Consulting",
        "SaaS",
        "Legal Services",
        "Healthcare",
        "E-commerce",
        "Real Estate",
        "Education",
    ]
    acquisition_channels = [
        "Google Ads",
        "LinkedIn",
        "Referral",
        "Organic Search",
        "Email Campaign",
        "Conference",
        "Cold Outreach",
        "Partner",
    ]

    customers = []
    for i in range(1, num_customers + 1):
        acquisition_date = start + timedelta(
            days=int(np.random.exponential(scale=date_range_days * 0.3))
        )
        acquisition_date = min(acquisition_date, end - timedelta(days=30))

        is_churned = np.random.random() < 0.15 + 0.1 * np.sin(i / 10)
        if is_churned:
            churn_date = acquisition_date + timedelta(
                days=int(np.random.gamma(shape=3, scale=60))
            )
            churn_date = min(churn_date, end)
        else:
            churn_date = None

        industry = np.random.choice(industries, p=[0.2, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1])
        channel = np.random.choice(acquisition_channels, p=[0.15, 0.12, 0.2, 0.18, 0.1, 0.08, 0.07, 0.1])

        customers.append(
            {
                "customer_id": f"CUST-{i:04d}",
                "company_name": f"{random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Omega', 'Prime', 'Nova', 'Apex', 'Core', 'Edge'])} {random.choice(['Solutions', 'Group', 'Partners', 'Technologies', 'Consulting', 'Labs', 'Collective', 'Ventures'])}",
                "industry": industry,
                "acquisition_channel": channel,
                "acquisition_date": acquisition_date.strftime("%Y-%m-%d"),
                "churn_date": churn_date.strftime("%Y-%m-%d") if churn_date else "",
                "is_churned": is_churned,
                "annual_revenue": round(
                    np.random.lognormal(mean=11.5, sigma=1.0), 2
                ),
                "employees": int(np.random.choice([5, 10, 15, 25, 50, 100, 200], p=[0.1, 0.2, 0.2, 0.2, 0.15, 0.1, 0.05])),
            }
        )

    customers_df = pd.DataFrame(customers)

    # ── Transaction Data ─────────────────────────────────────────
    services = {
        "Digital Agency": [
            ("Website Development", 5000, 50000, 0.25),
            ("SEO Package", 1500, 8000, 0.20),
            ("Social Media Mgmt", 2000, 12000, 0.22),
            ("PPC Campaign", 3000, 25000, 0.18),
        ],
        "Consulting": [
            ("Strategy Session", 2000, 15000, 0.30),
            ("Market Analysis", 5000, 30000, 0.28),
            ("Process Optimization", 8000, 60000, 0.22),
            ("Executive Coaching", 3000, 20000, 0.35),
        ],
        "SaaS": [
            ("Monthly Subscription", 50, 500, 0.40),
            ("Annual Subscription", 500, 5000, 0.45),
            ("Enterprise License", 5000, 50000, 0.35),
            ("Implementation Fee", 3000, 20000, 0.20),
        ],
        "Legal Services": [
            ("Hourly Consultation", 300, 3000, 0.35),
            ("Contract Review", 2000, 10000, 0.30),
            ("Litigation Support", 5000, 100000, 0.25),
            ("Retainer", 5000, 25000, 0.28),
        ],
        "Healthcare": [
            ("Patient Consultation", 100, 500, 0.30),
            ("Wellness Program", 2000, 15000, 0.25),
            ("Telemedicine Plan", 500, 3000, 0.28),
            ("Corporate Health", 5000, 50000, 0.22),
        ],
        "E-commerce": [
            ("Product Sale", 20, 500, 0.15),
            ("Subscription Box", 30, 200, 0.20),
            ("Premium Membership", 100, 1000, 0.18),
            ("Bulk Order", 1000, 50000, 0.12),
        ],
        "Real Estate": [
            ("Property Listing", 500, 5000, 0.30),
            ("Property Management", 1000, 10000, 0.25),
            ("Valuation Report", 1000, 5000, 0.35),
            ("Consultation Fee", 500, 3000, 0.32),
        ],
        "Education": [
            ("Course Enrollment", 200, 3000, 0.20),
            ("Workshop Ticket", 100, 1500, 0.25),
            ("Corporate Training", 3000, 30000, 0.22),
            ("Annual Subscription", 500, 5000, 0.28),
        ],
    }

    transactions = []
    for i in range(1, num_transactions + 1):
        customer = customers_df.sample(1).iloc[0]
        cust_id = customer["customer_id"]
        industry = customer["industry"]
        acq_date = datetime.strptime(customer["acquisition_date"], "%Y-%m-%d")
        churn = customer["is_churned"]
        churn_dt = (
            datetime.strptime(customer["churn_date"], "%Y-%m-%d")
            if customer["churn_date"]
            else None
        )

        # Pick a service for this industry
        svc = random.choice(services[industry])
        service_name, min_price, max_price, margin = svc

        # Transaction date: between acquisition and (churn or end)
        max_date = churn_dt if churn and churn_dt else end
        if max_date <= acq_date:
            max_date = acq_date + timedelta(days=30)
        txn_date = acq_date + timedelta(
            days=int(np.random.uniform(0, (max_date - acq_date).days))
        )
        txn_date = min(txn_date, end)

        # Price with some noise
        base_price = np.random.uniform(min_price, max_price)
        price = round(base_price * np.random.uniform(0.8, 1.2), 2)

        transactions.append(
            {
                "transaction_id": f"TXN-{i:05d}",
                "customer_id": cust_id,
                "date": txn_date.strftime("%Y-%m-%d"),
                "service_name": service_name,
                "amount": price,
                "estimated_margin_pct": round(margin * 100, 1),
                "quantity": int(np.random.choice([1, 1, 1, 2, 3], p=[0.6, 0.2, 0.1, 0.07, 0.03])),
            }
        )

    transactions_df = pd.DataFrame(transactions)

    # ── Write files ──────────────────────────────────────────────
    customers_path = os.path.join(output_dir, "customers.csv")
    transactions_path = os.path.join(output_dir, "transactions.csv")

    customers_df.to_csv(customers_path, index=False)
    transactions_df.to_csv(transactions_path, index=False)

    print(f"✅ Generated {len(customers_df)} customers → {customers_path}")
    print(f"✅ Generated {len(transactions_df)} transactions → {transactions_path}")

    return customers_path, transactions_path


# ── Retail / Inventory Sample Data ──────────────────────────────────


RETAIL_PRODUCTS = [
    # (sku, category, name, unit_cost, unit_price, demand_pattern)
    # Seasonal (Y): high during holiday periods
    ("SEA-001", "Seasonal", "Holiday Decor Set", 8.00, 19.99, "seasonal"),
    ("SEA-002", "Seasonal", "Gift Wrap Bundle", 3.50, 9.99, "seasonal"),
    ("SEA-003", "Seasonal", "Advent Calendar", 12.00, 29.99, "seasonal"),
    ("SEA-004", "Seasonal", "Summer Grill Kit", 15.00, 34.99, "seasonal"),
    ("SEA-005", "Seasonal", "Winter Boots", 25.00, 59.99, "seasonal"),
    ("SEA-006", "Seasonal", "Umbrella", 5.00, 14.99, "seasonal"),
    ("SEA-007", "Seasonal", "Sunscreen Pack", 4.00, 11.99, "seasonal"),
    ("SEA-008", "Seasonal", "Holiday Ornaments", 2.00, 5.99, "seasonal"),
    ("SEA-009", "Seasonal", "Halloween Costume", 10.00, 24.99, "seasonal"),
    ("SEA-010", "Seasonal", "Easter Basket", 6.00, 14.99, "seasonal"),
    # Stable (X): consistent demand year-round
    ("STB-001", "Staples", "Paper Towels 12pk", 4.00, 9.99, "stable"),
    ("STB-002", "Staples", "Toilet Paper 24pk", 6.00, 14.99, "stable"),
    ("STB-003", "Staples", "Laundry Detergent", 5.00, 12.99, "stable"),
    ("STB-004", "Staples", "Dish Soap 3pk", 3.00, 7.99, "stable"),
    ("STB-005", "Staples", "All-Purpose Cleaner", 2.50, 6.99, "stable"),
    ("STB-006", "Staples", "Trash Bags 40pk", 3.00, 7.99, "stable"),
    ("STB-007", "Staples", "Bottled Water 24pk", 2.00, 5.99, "stable"),
    ("STB-008", "Staples", "Bread Loaf", 1.50, 3.99, "stable"),
    ("STB-009", "Staples", "Milk Gallon", 2.50, 4.99, "stable"),
    ("STB-010", "Staples", "Eggs 12pk", 1.50, 4.49, "stable"),
    # Trending (Holt): demand increasing over time
    ("TRD-001", "Trending", "Wireless Earbuds", 15.00, 39.99, "trending"),
    ("TRD-002", "Trending", "Phone Case", 5.00, 19.99, "trending"),
    ("TRD-003", "Trending", "USB-C Hub", 12.00, 29.99, "trending"),
    ("TRD-004", "Trending", "LED Desk Lamp", 10.00, 24.99, "trending"),
    ("TRD-005", "Trending", "Smart Water Bottle", 8.00, 19.99, "trending"),
    ("TRD-006", "Trending", "Yoga Mat", 10.00, 24.99, "trending"),
    ("TRD-007", "Trending", "Standing Desk Mat", 15.00, 39.99, "trending"),
    ("TRD-008", "Trending", "Blue Light Glasses", 3.00, 14.99, "trending"),
    # Intermittent (Z / Croston): sporadic demand
    ("INT-001", "Intermittent", "Snow Shovel", 8.00, 19.99, "intermittent"),
    ("INT-002", "Intermittent", "Tent 4-person", 40.00, 99.99, "intermittent"),
    ("INT-003", "Intermittent", "Camping Stove", 25.00, 59.99, "intermittent"),
    ("INT-004", "Intermittent", "Espresso Machine", 60.00, 149.99, "intermittent"),
    ("INT-005", "Intermittent", "Air Purifier", 45.00, 119.99, "intermittent"),
    ("INT-006", "Intermittent", "Electric Scooter", 80.00, 199.99, "intermittent"),
    ("INT-007", "Intermittent", "Home Projector", 70.00, 179.99, "intermittent"),
    ("INT-008", "Intermittent", "VR Headset", 100.00, 299.99, "intermittent"),
    # Dead stock candidates (will receive no sales in last 6 months)
    ("DED-001", "Dead", "VHS Adapter", 2.00, 4.99, "dead"),
    ("DED-002", "Dead", "MiniDV Tape 5pk", 3.00, 8.99, "dead"),
    ("DED-003", "Dead", "Floppy Disk USB Reader", 5.00, 12.99, "dead"),
    ("DED-004", "Dead", "Nintendo DS Game", 4.00, 9.99, "dead"),
    ("DED-005", "Dead", "Landline Phone", 10.00, 24.99, "dead"),
]


def generate_retail_sample_data(
    num_products: int = 45,
    num_sales: int = 10000,
    start_date: str = "2024-01-01",
    end_date: str = "2025-12-31",
    seed: int = 123,
    output_dir: str = "sample_retail_data",
) -> tuple[str, str, str]:
    """
    Generate synthetic retail inventory data with diverse demand patterns.

    Creates SKUs with seasonal, stable, trending, intermittent, and dead demand
    so every code path in the inventory analysis engine is exercised.

    Args:
        num_products: Number of products to generate (default all 45)
        num_sales: Number of sales transactions
        start_date/end_date: Date range
        seed: Random seed
        output_dir: Directory to write CSV files

    Returns:
        Tuple of (sales_path, inventory_path, products_path)
    """
    np.random.seed(seed)
    random.seed(seed)

    os.makedirs(output_dir, exist_ok=True)

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_range_days = (end - start).days

    if date_range_days <= 0:
        date_range_days = 365
        end = start + timedelta(days=365)

    # Pick products (up to num_products)
    products = RETAIL_PRODUCTS[:min(num_products, len(RETAIL_PRODUCTS))]

    # ── Products DataFrame ──
    products_df = pd.DataFrame([
        {"sku": p[0], "category": p[1], "product_name": p[2],
         "unit_cost": p[3], "unit_price": p[4], "demand_pattern": p[5]}
        for p in products
    ])

    # ── Generate Sales ──
    sales = []
    sku_patterns = {p[0]: p[5] for p in products}

    for i in range(num_sales):
        sku = random.choice([p[0] for p in products])
        pattern = sku_patterns[sku]

        # Determine quantity based on pattern
        if pattern == "dead":
            # Dead stock: no sales in last 6 months
            # Only generate sales in the first half
            half_date = start + timedelta(days=date_range_days // 2)
            sale_date = start + timedelta(days=int(np.random.uniform(0, date_range_days // 2 - 60)))
        elif pattern == "intermittent":
            # 70% chance of zero on any given day, but we sample across the whole period
            # Give these a lower probability to simulate sporadic demand
            if random.random() < 0.85:
                continue  # Skip most intermittent sales to make them truly sparse
            sale_date = start + timedelta(days=int(np.random.uniform(0, date_range_days)))
        else:
            sale_date = start + timedelta(days=int(np.random.uniform(0, date_range_days)))

        # Seasonal pattern: demand varies by month
        if pattern == "seasonal":
            month = sale_date.month
            # Strong Q4 (holiday), weak Q1/Q3
            seasonality_factor = {
                11: 2.5, 12: 3.0,  # Nov-Dec peak
                10: 1.8,            # Oct
                1: 0.6, 2: 0.5, 3: 0.7,  # Q1 low
                4: 1.0, 5: 1.2, 6: 1.5,  # Spring/summer rise
                7: 1.8, 8: 1.5, 9: 1.2,
            }.get(month, 1.0)
            base_qty = np.random.poisson(5 * seasonality_factor)
        elif pattern == "trending":
            # Demand increases over time
            days_since_start = (sale_date - start).days
            trend_factor = 1.0 + 0.6 * (days_since_start / date_range_days)
            base_qty = int(np.random.poisson(4 * trend_factor))
        elif pattern == "intermittent":
            base_qty = max(1, int(np.random.poisson(3)))
        elif pattern == "dead" or pattern == "stable":
            base_qty = int(np.random.poisson(3))
        else:
            base_qty = int(np.random.poisson(2))

        if base_qty < 1:
            base_qty = 1

        if base_qty > 100:
            base_qty = 100

        sales.append({
            "order_id": f"ORD-{i+1:06d}",
            "date": sale_date.strftime("%Y-%m-%d"),
            "sku": sku,
            "quantity": base_qty,
            "unit_price": products_df[products_df["sku"] == sku]["unit_price"].iloc[0],
            "unit_cost": products_df[products_df["sku"] == sku]["unit_cost"].iloc[0],
        })

    sales_df = pd.DataFrame(sales)

    # Sort by date
    if len(sales_df) > 0:
        sales_df["date"] = pd.to_datetime(sales_df["date"])
        sales_df = sales_df.sort_values("date").reset_index(drop=True)
        sales_df["date"] = sales_df["date"].dt.strftime("%Y-%m-%d")

    # ── Generate Inventory Snapshots ──
    inventory_rows = []
    for _, prod in products_df.iterrows():
        sku = prod["sku"]
        pattern = prod["demand_pattern"]

        # Estimate on-hand inventory based on demand pattern
        if pattern == "dead":
            # Dead stock: significant overstock
            on_hand = int(np.random.uniform(20, 100))
        elif pattern == "seasonal":
            # Seasonal: moderate stock, may be overstock after season
            on_hand = int(np.random.uniform(10, 60))
        elif pattern == "intermittent":
            # Intermittent: occasional stock
            on_hand = int(np.random.uniform(5, 30))
        elif pattern == "trending":
            # Trending: could be out of stock (growing demand)
            on_hand = int(np.random.uniform(0, 20))
        else:
            # Stable: steady moderate stock
            on_hand = int(np.random.uniform(15, 50))

        inventory_rows.append({
            "date": end.strftime("%Y-%m-%d"),
            "sku": sku,
            "on_hand": on_hand,
            "unit_cost": prod["unit_cost"],
        })

    inventory_df = pd.DataFrame(inventory_rows)

    # ── Write Files ──
    sales_path = os.path.join(output_dir, "retail_sales.csv")
    inventory_path = os.path.join(output_dir, "inventory_snapshots.csv")
    products_path = os.path.join(output_dir, "products.csv")

    sales_df.to_csv(sales_path, index=False)
    inventory_df.to_csv(inventory_path, index=False)
    products_df.to_csv(products_path, index=False)

    print(f"✅ Generated {len(products_df)} products → {products_path}")
    print(f"✅ Generated {len(inventory_df)} inventory records → {inventory_path}")
    print(f"✅ Generated {len(sales_df)} sales transactions → {sales_path}")
    print(f"   Demand patterns: {products_df['demand_pattern'].value_counts().to_dict()}")

    return sales_path, inventory_path, products_path


if __name__ == "__main__":
    generate_sample_data()
