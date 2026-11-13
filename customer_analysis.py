
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px

# STEP 1: Define paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "APL_Logistics_cleaned.csv"
REPORT_DIR = BASE_DIR / "reports"
CHART_DIR = BASE_DIR / "charts"

REPORT_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(exist_ok=True)

# STEP 2: Load cleaned dataset
df = pd.read_csv(DATA_FILE)

print("\n========== CUSTOMER PROFITABILITY ANALYSIS ==========")

# STEP 3: Aggregate customer performance
customers = (
    df.groupby("Customer Id")
    .agg(
        Revenue=("Net Revenue", "sum"),
        Profit=("Profit", "sum"),
        Transactions=("Profit", "size")
    )
    .reset_index()
)

# STEP 4: Calculate customer-level metrics
customers["Profit Margin (%)"] = np.where(
    customers["Revenue"] != 0,
    customers["Profit"] / customers["Revenue"] * 100,
    np.nan
)

total_profit = customers["Profit"].sum()

# Customer Value Index:
# Share of total portfolio profit, expressed as a percentage.
customers["Customer Value Index (%)"] = (
    customers["Profit"] / total_profit * 100
    if total_profit != 0 else np.nan
)

# STEP 5: Identify loss-making customers
customers["Loss Making"] = customers["Profit"] < 0

# STEP 6: Assign customer value tiers
# Rank by aggregate profit, not revenue.
customers = customers.sort_values(
    "Profit", ascending=False
).reset_index(drop=True)

customer_count = len(customers)

customers["Value Tier"] = np.select(
    [
        customers.index < customer_count * 0.10,
        customers.index < customer_count * 0.30,
        customers["Profit"] < 0
    ],
    [
        "High Value",
        "Medium Value",
        "Loss Making"
    ],
    default="Low Value"
)

# STEP 7: Display top and bottom customers
print(f"\nUnique Customers: {customer_count:,}")

print("\nTOP 10 CUSTOMERS BY PROFIT")
print(
    customers.head(10)[
        ["Customer Id", "Revenue", "Profit",
         "Profit Margin (%)", "Value Tier"]
    ].round(2).to_string(index=False)
)

print("\nBOTTOM 10 CUSTOMERS BY PROFIT")
print(
    customers.nsmallest(10, "Profit")[
        ["Customer Id", "Revenue", "Profit",
         "Profit Margin (%)", "Value Tier"]
    ].round(2).to_string(index=False)
)

print("\nCUSTOMER VALUE DISTRIBUTION")
print(customers["Value Tier"].value_counts().to_string())

print(
    f"\nLoss-making Customers: "
    f"{customers['Loss Making'].sum():,}"
)

# STEP 8: Save reports
customers.to_csv(
    REPORT_DIR / "customer_profitability.csv",
    index=False
)

customers.head(10).to_csv(
    REPORT_DIR / "top_10_customers.csv",
    index=False
)

customers.nsmallest(10, "Profit").to_csv(
    REPORT_DIR / "bottom_10_customers.csv",
    index=False
)

# STEP 9: Customer profitability visualization
top_10 = customers.head(10).copy()
top_10["Customer"] = top_10["Customer Id"].astype(str)

fig = px.bar(
    top_10.sort_values("Profit"),
    x="Profit",
    y="Customer",
    orientation="h",
    color="Profit Margin (%)",
    color_continuous_scale="Blues",
    title="Top 10 Customers by Profit",
    hover_data=["Revenue", "Customer Value Index (%)"]
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Total Profit (dataset units)",
    yaxis_title="Customer ID"
)

fig.write_html(
    CHART_DIR / "top_customers.html"
)

print("\nCustomer reports and chart saved!")
print("========== CUSTOMER ANALYSIS COMPLETED ==========")
