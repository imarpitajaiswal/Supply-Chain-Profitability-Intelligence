
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px

# STEP 1: Define project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "APL_Logistics_cleaned.csv"
REPORT_DIR = BASE_DIR / "reports"
CHART_DIR = BASE_DIR / "charts"

REPORT_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(exist_ok=True)

# STEP 2: Load cleaned data
df = pd.read_csv(DATA_FILE)

print("\n========== DISCOUNT IMPACT ANALYSIS ==========")

# STEP 3: Define discount bands
# These intervals do not overlap.
bins = [-0.001, 0, 5, 10, 15, 20, 25, np.inf]

labels = [
    "0%",
    ">0-5%",
    ">5-10%",
    ">10-15%",
    ">15-20%",
    ">20-25%",
    ">25%"
]

df["Discount Band"] = pd.cut(
    df["Discount (%)"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

# STEP 4: Aggregate profitability by discount band
discount_summary = (
    df.groupby("Discount Band", observed=True)
    .agg(
        Records=("Profit", "size"),
        Gross_Revenue=("Gross Revenue", "sum"),
        Net_Revenue=("Net Revenue", "sum"),
        Total_Discount=("Order Item Discount", "sum"),
        Total_Profit=("Profit", "sum"),
        Loss_Making_Records=("Is Loss Making", "sum")
    )
    .reset_index()
)

discount_summary["Profit Margin (%)"] = (
    discount_summary["Total_Profit"]
    / discount_summary["Net_Revenue"] * 100
)

discount_summary["Loss Rate (%)"] = (
    discount_summary["Loss_Making_Records"]
    / discount_summary["Records"] * 100
)

print("\n1. DISCOUNT BAND PERFORMANCE")
print(discount_summary.round(2).to_string(index=False))

# STEP 5: Discount and profit-margin relationship
correlation = df["Discount (%)"].corr(
    df["Profit Margin (%)"]
)

print("\n2. DISCOUNT-MARGIN CORRELATION")
print(f"Pearson correlation: {correlation:.4f}")

# STEP 6: Baseline financial metrics
gross_revenue = df["Gross Revenue"].sum()
net_revenue = df["Net Revenue"].sum()
total_profit = df["Profit"].sum()
total_discount = df["Order Item Discount"].sum()

actual_margin = total_profit / net_revenue * 100

print("\n3. BASELINE FINANCIAL METRICS")
print(f"Gross Revenue: {gross_revenue:,.2f}")
print(f"Net Revenue: {net_revenue:,.2f}")
print(f"Total Discounts: {total_discount:,.2f}")
print(f"Total Profit: {total_profit:,.2f}")
print(f"Actual Profit Margin: {actual_margin:.2f}%")

# STEP 7: Simulate alternative discount rates
# Assumptions:
# - Same quantities and gross selling prices
# - Same implied costs
# - No changes in customer demand
# - No additional costs or taxes

implied_cost = net_revenue - total_profit

scenario_rows = []

for discount_rate in range(0, 26, 5):
    scenario_discount = gross_revenue * discount_rate / 100
    scenario_revenue = gross_revenue - scenario_discount
    scenario_profit = scenario_revenue - implied_cost

    scenario_margin = (
        scenario_profit / scenario_revenue * 100
        if scenario_revenue > 0 else np.nan
    )

    scenario_rows.append({
        "Discount Rate (%)": discount_rate,
        "Scenario Revenue": scenario_revenue,
        "Scenario Profit": scenario_profit,
        "Scenario Margin (%)": scenario_margin,
        "Profit Change": scenario_profit - total_profit
    })

scenarios = pd.DataFrame(scenario_rows)

print("\n4. WHAT-IF DISCOUNT SCENARIOS")
print(scenarios.round(2).to_string(index=False))

# STEP 8: Export reports
discount_summary.to_csv(
    REPORT_DIR / "discount_performance.csv",
    index=False
)

scenarios.to_csv(
    REPORT_DIR / "discount_scenarios.csv",
    index=False
)

# STEP 9: Discount band profitability chart
fig1 = px.bar(
    discount_summary,
    x="Discount Band",
    y="Profit Margin (%)",
    color="Loss Rate (%)",
    text="Profit Margin (%)",
    color_continuous_scale="RdYlGn_r",
    title="Profit Margin by Discount Band",
    hover_data=["Records", "Total_Profit", "Net_Revenue"]
)

fig1.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig1.update_layout(
    template="plotly_white",
    xaxis_title="Discount Band",
    yaxis_title="Weighted Profit Margin (%)"
)

fig1.write_html(CHART_DIR / "discount_profitability.html")

# STEP 10: What-if scenario chart
fig2 = px.line(
    scenarios,
    x="Discount Rate (%)",
    y="Scenario Profit",
    markers=True,
    title="What-If Analysis: Discount Rate vs Profit",
    hover_data=[
        "Scenario Revenue",
        "Scenario Margin (%)",
        "Profit Change"
    ]
)

fig2.add_hline(
    y=total_profit,
    line_dash="dash",
    annotation_text="Actual Recorded Profit"
)

fig2.update_layout(
    template="plotly_white",
    xaxis_title="Simulated Uniform Discount (%)",
    yaxis_title="Simulated Total Profit (dataset units)"
)

fig2.write_html(CHART_DIR / "discount_scenarios.html")

print("\nReports and interactive charts saved!")
print("========== DISCOUNT ANALYSIS COMPLETED ==========")
