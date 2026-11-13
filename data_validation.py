
from pathlib import Path
import pandas as pd

# STEP 1: Locate and load the dataset
BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "data" / "APL_Logistics.csv"

df = pd.read_csv(file_path, encoding="latin-1", low_memory=False)

print("\n========== APL LOGISTICS DATA VALIDATION ==========")

# STEP 2: Check dataset dimensions
print("\n1. DATASET OVERVIEW")
print(f"Total Rows: {df.shape[0]:,}")
print(f"Total Columns: {df.shape[1]}")

# STEP 3: Display the first five records
print("\n2. FIRST FIVE RECORDS")
print(df.head().to_string())

# STEP 4: Check missing values
print("\n3. MISSING VALUES")
missing = df.isnull().sum()
print(missing[missing > 0].to_string())

# STEP 5: Check duplicate records
print("\n4. DUPLICATE RECORDS")
print(f"Duplicate Rows: {df.duplicated().sum():,}")

# STEP 6: Check important business dimensions
print("\n5. BUSINESS DIMENSIONS")
print(f"Unique Customers: {df['Customer Id'].nunique():,}")
print(f"Product Categories: {df['Category Name'].nunique()}")
print(f"Markets: {df['Market'].nunique()}")
print(f"Order Regions: {df['Order Region'].nunique()}")

# STEP 7: Validate financial metrics
print("\n6. FINANCIAL OVERVIEW")

gross_sales = df["Sales"].sum()
net_revenue = df["Order Item Total"].sum()
total_profit = df["Order Profit Per Order"].sum()
discounts = df["Order Item Discount"].sum()

profit_margin = (
    (total_profit / net_revenue) * 100
    if net_revenue != 0 else 0
)

print(f"Gross Sales: {gross_sales:,.2f}")
print(f"Net Revenue: {net_revenue:,.2f}")
print(f"Total Profit: {total_profit:,.2f}")
print(f"Total Discounts: {discounts:,.2f}")
print(f"Net Profit Margin: {profit_margin:.2f}%")

# STEP 8: Check discount reconciliation
difference = (
    df["Sales"]
    - df["Order Item Discount"]
    - df["Order Item Total"]
)

inconsistent_rows = (difference.abs() > 0.02).sum()

print("\n7. FINANCIAL VALIDATION")
print(f"Rows with inconsistent sales/discounts: {inconsistent_rows:,}")

print("\n========== VALIDATION COMPLETED ==========")
