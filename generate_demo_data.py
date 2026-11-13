
from pathlib import Path

import numpy as np
import pandas as pd

# ==================================================
# SYNTHETIC DEMO DATA GENERATOR
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "demo_data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "APL_Logistics_demo.csv"

rng = np.random.default_rng(42)
n = 12000

# Entirely fictional customer and product records
customer_ids = np.arange(10001, 11201)

markets = [
    "Europe", "LATAM", "Pacific Asia", "USCA", "Africa"
]

market_regions = {
    "Europe": ["Western Europe", "Northern Europe"],
    "LATAM": ["Central America", "South America"],
    "Pacific Asia": ["Southeast Asia", "Oceania"],
    "USCA": ["US East", "US West"],
    "Africa": ["North Africa", "Southern Africa"],
}

market_countries = {
    "Europe": ["France", "Germany"],
    "LATAM": ["Brazil", "Mexico"],
    "Pacific Asia": ["Australia", "Singapore"],
    "USCA": ["United States", "Canada"],
    "Africa": ["South Africa", "Morocco"],
}

product_catalog = {
    "Fishing": [
        "Demo Fishing Rod",
        "Demo Fishing Reel",
        "Demo Tackle Kit",
    ],
    "Camping & Hiking": [
        "Demo Hiking Backpack",
        "Demo Camping Tent",
        "Demo Sleeping Bag",
    ],
    "Cleats": [
        "Demo Football Cleats",
        "Demo Training Cleats",
    ],
    "Cardio Equipment": [
        "Demo Exercise Bike",
        "Demo Fitness Tracker",
    ],
    "Women's Apparel": [
        "Demo Running Jacket",
        "Demo Training Leggings",
    ],
    "Accessories": [
        "Demo Sports Bottle",
        "Demo Gym Bag",
    ],
}

product_prices = {
    product: price
    for products, prices in [
        (product_catalog["Fishing"], [110, 85, 35]),
        (product_catalog["Camping & Hiking"], [95, 240, 75]),
        (product_catalog["Cleats"], [120, 90]),
        (product_catalog["Cardio Equipment"], [450, 160]),
        (product_catalog["Women's Apparel"], [80, 55]),
        (product_catalog["Accessories"], [25, 45]),
    ]
    for product, price in zip(products, prices)
}

categories = list(product_catalog)

# Customer-level attributes remain consistent
customer_segments = rng.choice(
    ["Consumer", "Corporate", "Home Office"],
    size=len(customer_ids),
    p=[0.52, 0.30, 0.18],
)

customer_segment_map = dict(
    zip(customer_ids, customer_segments)
)

records = []

for i in range(n):
    customer_id = int(rng.choice(customer_ids))
    market = str(rng.choice(markets))

    region = str(rng.choice(market_regions[market]))
    country = str(rng.choice(market_countries[market]))

    category = str(rng.choice(categories))
    product = str(rng.choice(product_catalog[category]))

    quantity = int(rng.integers(1, 5))

    unit_price = product_prices[product]

    gross_revenue = float(unit_price * quantity)

    discount_rate = float(
        rng.choice(
            [0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
            p=[0.18, 0.15, 0.20, 0.17, 0.15, 0.10, 0.05],
        )
    )

    discount_amount = gross_revenue * discount_rate
    net_revenue = gross_revenue - discount_amount

    # Invented cost assumptions, not actual costs
    cost_ratio = float(rng.uniform(0.65, 0.98))
    implied_cost = gross_revenue * cost_ratio

    profit = net_revenue - implied_cost

    margin = (
        profit / net_revenue * 100
        if net_revenue else 0
    )

    records.append({
        "Customer Id": customer_id,
        "Customer Segment": customer_segment_map[customer_id],
        "Market": market,
        "Order Region": region,
        "Order Country": country,
        "Department Name": "Demo Retail Operations",
        "Category Name": category,
        "Product Name": product,
        "Order Status": "COMPLETE",
        "Shipping Mode": str(
            rng.choice(["Standard", "Second Class", "First Class"])
        ),
        "Sales": gross_revenue,
        "Order Item Total": net_revenue,
        "Order Item Discount": discount_amount,
        "Order Item Discount Rate": discount_rate,
        "Order Profit Per Order": profit,
        "Order Item Quantity": quantity,
        "Gross Revenue": gross_revenue,
        "Net Revenue": net_revenue,
        "Profit": profit,
        "Profit Margin (%)": margin,
        "Discount (%)": discount_rate * 100,
        "Is Loss Making": profit < 0,
    })

df = pd.DataFrame(records)

df.to_csv(OUTPUT_FILE, index=False)

print("=" * 55)
print("SYNTHETIC DEMO DATA GENERATED")
print("=" * 55)
print(f"File: {OUTPUT_FILE}")
print(f"Line items: {len(df):,}")
print(f"Customers: {df['Customer Id'].nunique():,}")
print(f"Categories: {df['Category Name'].nunique():,}")
print(f"Markets: {df['Market'].nunique():,}")
print(f"Net Revenue: {df['Net Revenue'].sum():,.2f}")
print(f"Profit: {df['Profit'].sum():,.2f}")
print("=" * 55)
print("All records are synthetic and fictional.")
