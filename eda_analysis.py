
from pathlib import Path
import pandas as pd

# STEP 1: Define project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "APL_Logistics_cleaned.csv"
REPORT_DIR = BASE_DIR / "reports"

# Create reports folder automatically
REPORT_DIR.mkdir(exist_ok=True)

# STEP 2: Load cleaned dataset
df = pd.read_csv(DATA_FILE)

print("\n========== APL LOGISTICS EDA ==========")
print(f"Total Records: {len(df):,}")

# STEP 3: Create reusable profitability function
def analyze_profitability(column):
    result = (
        df.groupby(column)
        .agg(
            Records=("Profit", "size"),
            Revenue=("Net Revenue", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    # Weighted profit margin, not average row margin
    result["Profit Margin (%)"] = (
        result["Profit"] / result["Revenue"] * 100
    ).round(2)

    return result

# STEP 4: Analyze global markets
market_analysis = analyze_profitability("Market")
market_analysis = market_analysis.sort_values(
    by="Profit", ascending=False
)

print("\n1. MARKET PROFITABILITY")
print(market_analysis.round(2).to_string(index=False))

# STEP 5: Analyze product categories
category_analysis = analyze_profitability("Category Name")
category_analysis = category_analysis.sort_values(
    by="Profit", ascending=False
)

print("\n2. TOP 5 PROFITABLE CATEGORIES")
print(category_analysis.head(5).round(2).to_string(index=False))

print("\n3. BOTTOM 5 CATEGORIES BY PROFIT")
print(category_analysis.tail(5).round(2).to_string(index=False))

# STEP 6: Analyze customer segments
segment_analysis = analyze_profitability("Customer Segment")
segment_analysis = segment_analysis.sort_values(
    by="Profit", ascending=False
)

print("\n4. CUSTOMER SEGMENT PERFORMANCE")
print(segment_analysis.round(2).to_string(index=False))

# STEP 7: Export analytics reports
market_analysis.to_csv(
    REPORT_DIR / "market_profitability.csv", index=False
)

category_analysis.to_csv(
    REPORT_DIR / "category_profitability.csv", index=False
)

segment_analysis.to_csv(
    REPORT_DIR / "customer_segments.csv", index=False
)

print("\nEDA reports saved successfully!")
print("========== ANALYSIS COMPLETED ==========")
