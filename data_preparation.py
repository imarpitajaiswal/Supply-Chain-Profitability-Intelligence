
from pathlib import Path
import pandas as pd
import numpy as np

# STEP 1: Set up file paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "APL_Logistics.csv"
OUTPUT_FILE = BASE_DIR / "data" / "APL_Logistics_cleaned.csv"

# STEP 2: Load original dataset
df = pd.read_csv(
    INPUT_FILE,
    encoding="latin-1",
    low_memory=False
)

print("\n========== DATA PREPARATION ==========")
print(f"Original records: {len(df):,}")

# STEP 3: Select columns needed for analysis
# Exclude names, addresses, ZIP codes, and coordinates.
columns = [
    "Customer Id",
    "Customer Segment",
    "Market",
    "Order Region",
    "Order Country",
    "Department Name",
    "Category Name",
    "Product Name",
    "Order Status",
    "Shipping Mode",
    "Sales",
    "Order Item Total",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Profit Per Order",
    "Order Item Quantity"
]

cleaned = df[columns].copy()

# STEP 4: Clean text columns
text_columns = [
    "Customer Segment",
    "Market",
    "Order Region",
    "Order Country",
    "Department Name",
    "Category Name",
    "Product Name",
    "Order Status",
    "Shipping Mode"
]

for col in text_columns:
    cleaned[col] = cleaned[col].astype("string").str.strip()

# STEP 5: Validate financial data
financial_columns = [
    "Sales",
    "Order Item Total",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Profit Per Order"
]

if cleaned[financial_columns].isna().any().any():
    raise ValueError("Missing financial values detected!")

if (cleaned["Order Item Total"] <= 0).any():
    raise ValueError("Invalid net revenue detected!")

difference = (
    cleaned["Sales"]
    - cleaned["Order Item Discount"]
    - cleaned["Order Item Total"]
)

if (difference.abs() > 0.02).any():
    raise ValueError("Financial reconciliation failed!")

# STEP 6: Create business analytics features
cleaned["Gross Revenue"] = cleaned["Sales"]

cleaned["Net Revenue"] = cleaned["Order Item Total"]

cleaned["Profit"] = cleaned["Order Profit Per Order"]

cleaned["Profit Margin (%)"] = (
    cleaned["Profit"] / cleaned["Net Revenue"] * 100
).round(2)

cleaned["Discount (%)"] = (
    cleaned["Order Item Discount Rate"] * 100
).round(2)

cleaned["Is Loss Making"] = cleaned["Profit"] < 0

# STEP 7: Save analysis-ready dataset
cleaned.to_csv(OUTPUT_FILE, index=False)

# STEP 8: Display final summary
print(f"Cleaned records: {len(cleaned):,}")
print(f"Columns: {len(cleaned.columns)}")
print(f"Missing values: {cleaned.isna().sum().sum():,}")
print(f"Loss-making records: {cleaned['Is Loss Making'].sum():,}")

print(f"Net Revenue: {cleaned['Net Revenue'].sum():,.2f}")
print(f"Total Profit: {cleaned['Profit'].sum():,.2f}")

overall_margin = (
    cleaned["Profit"].sum()
    / cleaned["Net Revenue"].sum()
    * 100
)

print(f"Overall Profit Margin: {overall_margin:.2f}%")
print(f"\nSaved file: {OUTPUT_FILE.name}")
print("========== PREPARATION COMPLETED ==========")
