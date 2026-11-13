
import streamlit as st

st.set_page_config(
    page_title="APL Logistics | Profitability Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("APL Logistics")
st.subheader("Enterprise Profitability Intelligence")

st.caption(
    "Customer • Product • Market • Financial Analytics"
)

st.divider()


# ==================================================
# DATA LOADING AND GLOBAL FILTERS
# ==================================================

from pathlib import Path
import pandas as pd
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "APL_Logistics_cleaned.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)


df = load_data()

st.sidebar.title("Analytics Control Center")


def create_filter(label, column):
    options = sorted(
        df[column].dropna().unique().tolist()
    )

    return st.sidebar.multiselect(
        label,
        options=options,
        default=options
    )


markets = create_filter("Global Markets", "Market")
regions = create_filter("Order Regions", "Order Region")
segments = create_filter("Customer Segments", "Customer Segment")
categories = create_filter("Product Categories", "Category Name")
products = create_filter("Products", "Product Name")

filtered = df[
    df["Market"].isin(markets)
    & df["Order Region"].isin(regions)
    & df["Customer Segment"].isin(segments)
    & df["Category Name"].isin(categories)
    & df["Product Name"].isin(products)
].copy()


def profitability_summary(data, column):
    summary = (
        data.groupby(column)
        .agg(
            Revenue=("Net Revenue", "sum"),
            Profit=("Profit", "sum"),
            Records=("Profit", "size")
        )
        .reset_index()
    )

    summary["Margin (%)"] = (
        summary["Profit"]
        .div(summary["Revenue"].replace(0, float("nan")))
        * 100
    ).round(2)

    return summary


if filtered.empty:
    st.warning(
        "No records match the selected filters. "
        "Please adjust your selections."
    )
    st.stop()

tabs = st.tabs([
    "📊 Executive Overview",
    "👥 Customer Intelligence",
    "📦 Product Performance",
    "💰 Discount Analyzer"
])


with tabs[0]:
    st.header("Executive Performance Overview")

    revenue = filtered["Net Revenue"].sum()
    profit = filtered["Profit"].sum()
    discounts = filtered["Order Item Discount"].sum()

    margin = (
        profit / revenue * 100
        if revenue != 0 else 0
    )

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Net Revenue", f"{revenue:,.0f}")
    k2.metric("Total Profit", f"{profit:,.0f}")
    k3.metric("Profit Margin", f"{margin:.2f}%")
    k4.metric("Total Discounts", f"{discounts:,.0f}")

    st.caption(
        f"{len(filtered):,} line items | "
        f"{filtered['Customer Id'].nunique():,} customers"
    )

    st.divider()

    # Global market profitability
    st.subheader("Global Market Performance")

    market = profitability_summary(filtered, "Market")

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            market,
            x="Market",
            y="Revenue",
            color="Market",
            title="Revenue by Global Market",
            template="plotly_white"
        )

        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="stretch")

    with right:
        fig = px.bar(
            market,
            x="Market",
            y="Profit",
            color="Margin (%)",
            color_continuous_scale="Blues",
            title="Profit by Global Market",
            template="plotly_white"
        )

        st.plotly_chart(fig, width="stretch")

    st.dataframe(
        market,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # Regional profitability
    st.subheader("Regional Profitability")

    region = profitability_summary(
        filtered, "Order Region"
    )

    fig = px.bar(
        region.sort_values("Profit", ascending=False),
        x="Order Region",
        y="Profit",
        color="Margin (%)",
        color_continuous_scale="Teal",
        title="Profit Contribution by Region",
        template="plotly_white"
    )

    st.plotly_chart(fig, width="stretch")


# ==================================================
# TAB 2: CUSTOMER INTELLIGENCE
# ==================================================

with tabs[1]:
    st.header("Customer Value Intelligence")

    st.caption(
        "Identify high-value customers, loss-making accounts, "
        "and customer profitability patterns."
    )

    # STEP 1: Aggregate customer financial performance
    customers = (
        filtered.groupby("Customer Id")
        .agg(
            Revenue=("Net Revenue", "sum"),
            Profit=("Profit", "sum"),
            Line_Items=("Profit", "size")
        )
        .reset_index()
    )

    # STEP 2: Calculate profitability metrics
    customers["Margin (%)"] = (
        customers["Profit"]
        / customers["Revenue"].replace(0, float("nan"))
        * 100
    )

    total_customer_profit = customers["Profit"].sum()

    customers["Customer Value Index (%)"] = (
        customers["Profit"] / total_customer_profit * 100
        if abs(total_customer_profit) > 1e-9
        else float("nan")
    )

    customers["Loss Making"] = customers["Profit"] < 0

    # STEP 3: Classify customers by profit
    customers = customers.sort_values(
        "Profit", ascending=False
    ).reset_index(drop=True)

    profitable = customers[
        customers["Profit"] >= 0
    ].copy()

    loss_making = customers[
        customers["Profit"] < 0
    ].copy()

    # Percentile-based value segmentation
    profitable["Profit Rank (%)"] = (
        profitable["Profit"].rank(
            pct=True,
            ascending=False,
            method="first"
        )
    )

    profitable["Value Tier"] = "Low Value"

    profitable.loc[
        profitable["Profit Rank (%)"] <= 0.30,
        "Value Tier"
    ] = "Medium Value"

    profitable.loc[
        profitable["Profit Rank (%)"] <= 0.10,
        "Value Tier"
    ] = "High Value"

    loss_making["Value Tier"] = "Loss Making"

    customers = pd.concat(
        [profitable, loss_making],
        ignore_index=True
    )

    # STEP 4: Customer KPI cards
    st.subheader("Customer Performance KPIs")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Total Customers",
        f"{len(customers):,}"
    )

    k2.metric(
        "High-Value Customers",
        f"{(customers['Value Tier'] == 'High Value').sum():,}"
    )

    k3.metric(
        "Loss-Making Customers",
        f"{customers['Loss Making'].sum():,}"
    )

    loss_rate = (
        customers["Loss Making"].mean() * 100
        if len(customers) else 0
    )

    k4.metric(
        "Loss-Making Customer Rate",
        f"{loss_rate:.2f}%"
    )

    st.divider()

    # STEP 5: Top and bottom customers
    left, right = st.columns(2)

    with left:
        st.subheader("Top 10 Customers by Profit")

        top_customers = customers.nlargest(
            10, "Profit"
        ).copy()

        top_customers["Customer"] = (
            top_customers["Customer Id"].astype(str)
        )

        fig = px.bar(
            top_customers.sort_values("Profit"),
            x="Profit",
            y="Customer",
            orientation="h",
            color="Margin (%)",
            color_continuous_scale="Blues",
            title="Highest Profit Contributors",
            template="plotly_white"
        )

        st.plotly_chart(
            fig, width="stretch"
        )

    with right:
        st.subheader("Bottom 10 Customers by Profit")

        bottom_customers = customers.nsmallest(
            10, "Profit"
        ).copy()

        bottom_customers["Customer"] = (
            bottom_customers["Customer Id"].astype(str)
        )

        fig = px.bar(
            bottom_customers.sort_values("Profit"),
            x="Profit",
            y="Customer",
            orientation="h",
            color="Profit",
            color_continuous_scale="RdYlGn",
            title="Lowest Profit Contributors",
            template="plotly_white"
        )

        st.plotly_chart(
            fig, width="stretch"
        )

    st.divider()

    # STEP 6: Customer value segmentation
    st.subheader("Customer Value Segmentation")

    tier_summary = (
        customers.groupby("Value Tier")
        .agg(
            Customers=("Customer Id", "count"),
            Revenue=("Revenue", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    fig = px.bar(
        tier_summary,
        x="Value Tier",
        y="Profit",
        color="Value Tier",
        title="Profit Contribution by Customer Tier",
        template="plotly_white"
    )

    st.plotly_chart(
        fig, width="stretch"
    )

    st.dataframe(
        tier_summary.round(2),
        width="stretch",
        hide_index=True
    )

    st.divider()

    # STEP 7: Customer segment contribution
    st.subheader("Customer Segment Performance")

    segment_summary = profitability_summary(
        filtered, "Customer Segment"
    )

    fig = px.bar(
        segment_summary,
        x="Customer Segment",
        y="Profit",
        color="Margin (%)",
        color_continuous_scale="Teal",
        title="Profit Contribution by Customer Segment",
        template="plotly_white"
    )

    st.plotly_chart(
        fig, width="stretch"
    )

    st.dataframe(
        segment_summary,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # STEP 8: Customer profitability details
    st.subheader("Customer Profitability Details")

    st.dataframe(
        customers.round(2),
        width="stretch",
        hide_index=True
    )

    # STEP 9: Download customer analytics
    st.download_button(
        label="Download Customer Profitability Report",
        data=customers.to_csv(index=False),
        file_name="customer_profitability_report.csv",
        mime="text/csv",
        key="customer_download"
    )

    st.caption(
        "Customer tiers are based on aggregate profit "
        "within the currently selected filters. "
        "The Customer Value Index represents each customer's "
        "percentage contribution to total filtered profit."
    )


# ==================================================
# TAB 3: PRODUCT & CATEGORY PERFORMANCE
# ==================================================

with tabs[2]:
    st.header("Product & Category Performance")

    st.caption(
        "Analyze category profitability, identify margin "
        "risks, and prioritize product-level opportunities."
    )

    # STEP 1: Aggregate product and category performance
    product_summary = profitability_summary(
        filtered, "Product Name"
    )

    category_summary = profitability_summary(
        filtered, "Category Name"
    )

    # STEP 2: Identify low-margin and loss-making products
    portfolio_revenue = filtered["Net Revenue"].sum()
    portfolio_profit = filtered["Profit"].sum()

    portfolio_margin = (
        portfolio_profit / portfolio_revenue * 100
        if portfolio_revenue != 0 else 0
    )

    median_product_revenue = product_summary["Revenue"].median()

    high_revenue_low_margin = product_summary[
        (product_summary["Revenue"] >= median_product_revenue)
        & (product_summary["Margin (%)"] < portfolio_margin)
    ].sort_values("Revenue", ascending=False)

    loss_making_products = product_summary[
        product_summary["Profit"] < 0
    ].sort_values("Profit")

    # STEP 3: Product KPIs
    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Products Analyzed",
        f"{len(product_summary):,}"
    )

    k2.metric(
        "Product Categories",
        f"{len(category_summary):,}"
    )

    k3.metric(
        "Low-Margin Products",
        f"{len(high_revenue_low_margin):,}"
    )

    k4.metric(
        "Loss-Making Products",
        f"{len(loss_making_products):,}"
    )

    st.divider()

    # STEP 4: Category profitability
    st.subheader("Category Profitability")

    top_categories = category_summary.nlargest(
        10, "Profit"
    )

    fig = px.bar(
        top_categories.sort_values("Profit"),
        x="Profit",
        y="Category Name",
        orientation="h",
        color="Margin (%)",
        color_continuous_scale="Blues",
        title="Top 10 Categories by Profit",
        template="plotly_white"
    )

    st.plotly_chart(fig, width="stretch")

    st.dataframe(
        category_summary.sort_values(
            "Profit", ascending=False
        ),
        width="stretch",
        hide_index=True
    )

    st.divider()

    # STEP 5: High-revenue, low-margin products
    st.subheader("High-Revenue, Low-Margin Products")

    st.caption(
        "Products with revenue at or above the median "
        "product revenue, but margin below the overall "
        "filtered portfolio margin."
    )

    if high_revenue_low_margin.empty:
        st.success(
            "No products meet the selected risk criteria."
        )
    else:
        st.dataframe(
            high_revenue_low_margin.round(2),
            width="stretch",
            hide_index=True
        )

    st.divider()

    # STEP 6: Loss-making products
    st.subheader("Loss-Making Products")

    st.caption(
        "Products with negative aggregate profit across "
        "the currently selected records."
    )

    if loss_making_products.empty:
        st.info(
            "No products have negative aggregate profit "
            "under the current filters."
        )
    else:
        st.dataframe(
            loss_making_products.round(2),
            width="stretch",
            hide_index=True
        )

    st.divider()

    # STEP 7: Category-by-market profitability heatmap
    st.subheader("Category Profitability Heatmap")

    heatmap_data = (
        filtered.groupby(["Category Name", "Market"])
        .agg(
            Revenue=("Net Revenue", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    heatmap_data["Margin (%)"] = (
        heatmap_data["Profit"]
        .div(
            heatmap_data["Revenue"].replace(
                0, float("nan")
            )
        )
        * 100
    )

    heatmap_pivot = heatmap_data.pivot(
        index="Category Name",
        columns="Market",
        values="Margin (%)"
    )

    fig = px.imshow(
        heatmap_pivot,
        color_continuous_scale="RdYlGn",
        color_continuous_midpoint=0,
        aspect="auto",
        labels={
            "x": "Global Market",
            "y": "Product Category",
            "color": "Margin (%)"
        },
        title="Category Profit Margins Across Markets"
    )

    fig.update_layout(height=900)

    st.plotly_chart(fig, width="stretch")

    st.caption(
        "Heatmap margins use aggregate profit divided "
        "by aggregate net revenue. Missing combinations "
        "represent categories without matching records."
    )

    st.divider()

    # STEP 8: Product profitability details
    st.subheader("Product Profitability Details")

    st.dataframe(
        product_summary.sort_values(
            "Profit", ascending=False
        ).round(2),
        width="stretch",
        hide_index=True
    )

    # STEP 9: Download report
    st.download_button(
        label="Download Product Profitability Report",
        data=product_summary.to_csv(index=False),
        file_name="product_profitability_report.csv",
        mime="text/csv",
        key="product_download"
    )


# ==================================================
# TAB 4: DISCOUNT IMPACT ANALYZER
# ==================================================

with tabs[3]:
    st.header("Discount Impact Analyzer")

    st.caption(
        "Explore historical discount patterns and simulate "
        "alternative discount policies."
    )

    # STEP 1: Prepare discount bands
    discount_data = filtered.copy()

    discount_bins = [
        -0.001, 0, 5, 10, 15, 20, 25, float("inf")
    ]

    discount_labels = [
        "0%", ">0–5%", ">5–10%", ">10–15%",
        ">15–20%", ">20–25%", ">25%"
    ]

    discount_data["Discount Band"] = pd.cut(
        discount_data["Discount (%)"],
        bins=discount_bins,
        labels=discount_labels,
        include_lowest=True
    )

    discount_summary = (
        discount_data.groupby(
            "Discount Band", observed=True
        )
        .agg(
            Line_Items=("Profit", "size"),
            Revenue=("Net Revenue", "sum"),
            Profit=("Profit", "sum"),
            Loss_Making_Items=("Is Loss Making", "sum")
        )
        .reset_index()
    )

    discount_summary["Margin (%)"] = (
        discount_summary["Profit"]
        .div(
            discount_summary["Revenue"].replace(
                0, float("nan")
            )
        )
        * 100
    )

    discount_summary["Loss Rate (%)"] = (
        discount_summary["Loss_Making_Items"]
        / discount_summary["Line_Items"] * 100
    )

    # STEP 2: Observed discount performance
    st.subheader("Observed Discount Performance")

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            discount_summary,
            x="Discount Band",
            y="Margin (%)",
            color="Loss Rate (%)",
            color_continuous_scale="RdYlGn_r",
            title="Profit Margin by Discount Band",
            template="plotly_white"
        )
        st.plotly_chart(
            fig, width="stretch"
        )

    with right:
        fig = px.bar(
            discount_summary,
            x="Discount Band",
            y="Loss Rate (%)",
            color="Margin (%)",
            color_continuous_scale="RdYlGn",
            title="Loss-Making Line-Item Rate",
            template="plotly_white"
        )
        st.plotly_chart(
            fig, width="stretch"
        )

    st.dataframe(
        discount_summary.round(2),
        width="stretch",
        hide_index=True
    )

    st.divider()

    # STEP 3: Interactive what-if simulator
    st.subheader("Interactive Discount What-If Simulator")

    st.info(
        "The simulation assumes unchanged gross prices, "
        "quantities, and implied historical costs. "
        "It does not forecast customer demand."
    )

    selected_discount = st.slider(
        "Simulated Uniform Discount Rate (%)",
        min_value=0,
        max_value=50,
        value=10,
        step=1,
        key="discount_simulator"
    )

    gross_sales = discount_data["Gross Revenue"].sum()
    actual_revenue = discount_data["Net Revenue"].sum()
    actual_profit = discount_data["Profit"].sum()

    implied_cost = actual_revenue - actual_profit

    simulated_revenue = (
        gross_sales * (1 - selected_discount / 100)
    )

    simulated_profit = (
        simulated_revenue - implied_cost
    )

    simulated_margin = (
        simulated_profit / simulated_revenue * 100
        if simulated_revenue > 0 else 0
    )

    profit_difference = (
        simulated_profit - actual_profit
    )

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Simulated Revenue",
        f"{simulated_revenue:,.0f}",
        delta=f"{simulated_revenue - actual_revenue:,.0f}"
    )

    k2.metric(
        "Simulated Profit",
        f"{simulated_profit:,.0f}",
        delta=f"{profit_difference:,.0f}"
    )

    k3.metric(
        "Simulated Margin",
        f"{simulated_margin:.2f}%"
    )

    k4.metric(
        "Profit Difference",
        f"{profit_difference:,.0f}"
    )

    st.divider()

    # STEP 4: Generate discount scenarios
    scenario_results = []

    for rate in range(0, 51):
        scenario_revenue = (
            gross_sales * (1 - rate / 100)
        )

        scenario_profit = (
            scenario_revenue - implied_cost
        )

        scenario_margin = (
            scenario_profit / scenario_revenue * 100
            if scenario_revenue > 0 else 0
        )

        scenario_results.append({
            "Discount Rate (%)": rate,
            "Simulated Revenue": scenario_revenue,
            "Simulated Profit": scenario_profit,
            "Simulated Margin (%)": scenario_margin
        })

    scenarios_df = pd.DataFrame(scenario_results)

    fig = px.line(
        scenarios_df,
        x="Discount Rate (%)",
        y="Simulated Profit",
        title="Simulated Profit Across Discount Rates",
        template="plotly_white"
    )

    fig.add_hline(
        y=actual_profit,
        line_dash="dash",
        annotation_text="Actual Recorded Profit"
    )

    fig.add_vline(
        x=selected_discount,
        line_dash="dot",
        annotation_text="Selected Scenario"
    )

    st.plotly_chart(
        fig, width="stretch"
    )

    # STEP 5: Observed discount-margin relationship
    st.subheader("Discount Rate vs Profit Margin")

    scatter_data = discount_data.sample(
        n=min(5000, len(discount_data)),
        random_state=42
    )

    fig = px.scatter(
        scatter_data,
        x="Discount (%)",
        y="Profit Margin (%)",
        color="Is Loss Making",
        opacity=0.45,
        title="Observed Discount and Profit Margin Relationship",
        template="plotly_white"
    )

    st.plotly_chart(
        fig, width="stretch"
    )

    st.caption(
        "The scatter plot uses a reproducible sample "
        "of up to 5,000 line items for responsiveness."
    )

    st.divider()

    # STEP 6: Download scenarios
    st.subheader("Export Discount Analysis")

    st.download_button(
        label="Download Discount Scenario Analysis",
        data=scenarios_df.to_csv(index=False),
        file_name="discount_what_if_scenarios.csv",
        mime="text/csv",
        key="discount_download"
    )

    st.caption(
        "What-if results are illustrative, not causal "
        "estimates or demand forecasts."
    )
