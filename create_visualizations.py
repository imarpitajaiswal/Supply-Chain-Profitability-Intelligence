
from pathlib import Path
import pandas as pd
import plotly.express as px

# STEP 1: Define project folders
BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
CHART_DIR = BASE_DIR / "charts"

CHART_DIR.mkdir(exist_ok=True)

# STEP 2: Load EDA reports
market = pd.read_csv(REPORT_DIR / "market_profitability.csv")
category = pd.read_csv(REPORT_DIR / "category_profitability.csv")
segment = pd.read_csv(REPORT_DIR / "customer_segments.csv")

print("\n========== CREATING VISUALIZATIONS ==========")

# STEP 3: Market profitability chart
fig1 = px.bar(
    market,
    x="Market",
    y="Profit",
    color="Profit Margin (%)",
    text="Profit",
    color_continuous_scale="Blues",
    title="Global Market Profitability",
    hover_data=["Revenue", "Profit Margin (%)"]
)

fig1.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
fig1.update_layout(
    template="plotly_white",
    yaxis_title="Total Profit (dataset units)",
    xaxis_title="Global Market"
)

fig1.write_html(CHART_DIR / "market_profitability.html")
print("1. Market profitability chart created")

# STEP 4: Top 10 profitable categories
top_categories = category.nlargest(10, "Profit")
top_categories = top_categories.sort_values("Profit")

fig2 = px.bar(
    top_categories,
    x="Profit",
    y="Category Name",
    orientation="h",
    color="Profit Margin (%)",
    text="Profit",
    color_continuous_scale="Teal",
    title="Top 10 Most Profitable Product Categories",
    hover_data=["Revenue", "Profit Margin (%)"]
)

fig2.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
fig2.update_layout(
    template="plotly_white",
    xaxis_title="Total Profit (dataset units)",
    yaxis_title="Product Category"
)

fig2.write_html(CHART_DIR / "category_profitability.html")
print("2. Category profitability chart created")

# STEP 5: Customer segment margins
fig3 = px.bar(
    segment,
    x="Customer Segment",
    y="Profit Margin (%)",
    color="Customer Segment",
    text="Profit Margin (%)",
    title="Customer Segment Profit Margins",
    hover_data=["Revenue", "Profit"]
)

fig3.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig3.update_layout(
    template="plotly_white",
    yaxis_title="Profit Margin (%)",
    xaxis_title="Customer Segment",
    showlegend=False,
    yaxis_range=[0, 15]
)

fig3.write_html(CHART_DIR / "customer_segments.html")
print("3. Customer segment chart created")

print("\nAll charts saved in the charts folder!")
print("========== VISUALIZATIONS COMPLETED ==========")
