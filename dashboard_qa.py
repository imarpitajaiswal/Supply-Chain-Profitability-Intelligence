
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "APL_Logistics_cleaned.csv"

df = pd.read_csv(DATA_FILE)

print("\n" + "=" * 55)
print("APL LOGISTICS — DASHBOARD QUALITY ASSURANCE")
print("=" * 55)

# Previously validated dataset benchmarks
EXPECTED_ROWS = 180519
EXPECTED_REVENUE = 33054402.04
EXPECTED_PROFIT = 3966902.97
EXPECTED_DISCOUNTS = 3730378.40

# Actual values
actual_rows = len(df)
actual_revenue = df["Net Revenue"].sum()
actual_profit = df["Profit"].sum()
actual_discounts = df["Order Item Discount"].sum()

checks = {
    "Dataset Row Count": actual_rows == EXPECTED_ROWS,
    "Net Revenue": abs(
        actual_revenue - EXPECTED_REVENUE
    ) < 1,
    "Total Profit": abs(
        actual_profit - EXPECTED_PROFIT
    ) < 1,
    "Total Discounts": abs(
        actual_discounts - EXPECTED_DISCOUNTS
    ) < 1,
    "No Missing Values": df.isna().sum().sum() == 0,
    "No Duplicate Rows": df.duplicated().sum() == 0,
    "Profit Reconciliation": abs(
        df["Profit"].sum()
        - df.groupby("Market")["Profit"].sum().sum()
    ) < 0.01,
    "Revenue Reconciliation": abs(
        df["Net Revenue"].sum()
        - df.groupby("Category Name")["Net Revenue"].sum().sum()
    ) < 0.01,
}

for name, passed in checks.items():
    status = "PASS" if passed else "FAIL"
    print(f"{name:<32} {status}")

print("-" * 55)
print(f"Rows: {actual_rows:,}")
print(f"Net Revenue: {actual_revenue:,.2f}")
print(f"Profit: {actual_profit:,.2f}")
print(f"Discounts: {actual_discounts:,.2f}")

margin = (
    actual_profit / actual_revenue * 100
    if actual_revenue else 0
)

print(f"Profit Margin: {margin:.2f}%")

print("=" * 55)

if all(checks.values()):
    print("RESULT: ALL QA CHECKS PASSED")
else:
    print("RESULT: QA ISSUES DETECTED")
