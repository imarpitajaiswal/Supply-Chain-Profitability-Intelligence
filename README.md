
# Supply Chain Profitability Intelligence
### Customer, Product & Discount Performance Analytics

**Python | Pandas | Plotly | Streamlit | Business Intelligence**

An end-to-end supply chain profitability analytics project that transforms operational sales records into actionable customer, product, market, and pricing insights.

Developed as part of the Unified Mentor internship project, using an APL Logistics business case.

---

## 1. Executive Overview

This project analyzes 180,519 supply chain sales line items to understand profitability performance across global markets, customer segments, and product categories.

The solution combines:

- Data validation and preparation
- Exploratory data analysis
- Customer profitability segmentation
- Product and category performance diagnostics
- Discount impact analysis
- Interactive pricing scenario simulation
- Executive-level Streamlit dashboards

The objective is to identify profitability risks and support evidence-based commercial decisions.

## 2. Business Problem

Revenue growth does not necessarily translate into stronger profitability.

Discounting practices, product mix, customer contribution, and regional performance can create significant differences between sales volume and actual profit.

This project investigates:

1. Which markets and categories generate the greatest profit?
2. Which customers contribute most to profitability?
3. Which customers and products generate negative aggregate profit?
4. Which high-revenue products underperform on margin?
5. How do observed discounts relate to profit margins?
6. How might alternative discount policies affect profit under fixed-cost assumptions?

## 3. Dataset Overview

| Attribute | Value |
|---|---|
| Dataset records | 180,519 |
| Unique customers | 20,652 |
| Product categories | 50 |
| Global markets | 5 |
| Order regions | 23 |
| Unit of analysis | Sales line item |
| Dataset encoding | Latin-1 |

The original dataset includes commercial, customer, product, and order-related attributes.

The cleaned analytical dataset contains derived revenue, profit, margin, discount, and loss-making indicators.

**Data governance:** Raw and customer-level datasets are excluded from the public repository pending confirmation of redistribution permissions.

## 4. Financial Performance

Full-dataset benchmarks established during initial validation:

| KPI | Value |
|---|---:|
| Gross Revenue | 36,784,734.31 |
| Net Revenue | 33,054,402.04 |
| Total Profit | 3,966,902.97 |
| Total Discounts | 3,730,378.40 |
| Profit Margin | 12.00% |

The source dataset does not specify a currency, so monetary figures are presented without a currency symbol.

### KPI Definitions

**Net Revenue**

Sum of recorded order-item totals after discounts.

**Total Profit**

Sum of recorded order-item profits.

**Weighted Profit Margin**

Total Profit / Total Net Revenue × 100

**Customer Value Index**

Individual Customer Profit / Total Portfolio Profit × 100

**Discount Impact Ratio**

Total Recorded Discounts / Gross Revenue × 100

**Loss-Making Customer**

A customer whose aggregate profit is negative within the selected analysis scope.

## 5. Analytics Architecture

```text
Raw Supply Chain Dataset
          |
          v
   Data Validation
          |
          v
   Data Preparation
          |
          v
  Cleaned Analytical Data
          |
          +-----------------------+
          |                       |
          v                       v
 Exploratory Analysis     Customer Analysis
          |                       |
          +-----------+-----------+
                      |
                      v
              Discount Analysis
                      |
                      v
           Streamlit Dashboard
                      |
                      v
            Business Insights
```

## 6. Dashboard Modules

### Executive Overview

- Net revenue, total profit, margin, and discounts
- Market-level revenue and profit
- Regional profitability
- Interactive global filters

### Customer Intelligence

- Customer Value Index
- High-, medium-, and low-value customer tiers
- Loss-making customer identification
- Top and bottom customers by profit
- Customer segment contribution
- Customer profitability CSV export

### Product Performance

- Product and category profitability
- High-revenue, low-margin product identification
- Loss-making product diagnostics
- Category-by-market profitability heatmap
- Product profitability CSV export

### Discount Impact Analyzer

- Profit margin by observed discount band
- Loss-making line-item rates
- Discount versus margin visualization
- Interactive uniform discount simulation
- Actual versus simulated profit comparison
- Scenario CSV export

## 7. Analytical Methodology

The workflow follows five stages:

1. Validate the original dataset, financial totals, and missing values.
2. Prepare a consistent analytical dataset with derived KPIs.
3. Aggregate performance across markets, segments, customers, and products.
4. Investigate profitability risks and observed discount patterns.
5. Communicate findings through an interactive dashboard.

Margins are calculated from aggregated profit and revenue rather than averaging individual line-item margins.

Negative-profit records are preserved.

## 8. Discount Simulation Assumptions

The discount simulator evaluates hypothetical uniform discounts applied to recorded gross sales.

It assumes:

- Unchanged sales quantities
- Unchanged gross prices
- Unchanged implied historical costs
- No customer demand response
- No changes to product mix

Simulated Net Revenue = Gross Revenue × (1 − Discount Rate)

Implied Historical Cost = Actual Net Revenue − Actual Profit

Simulated Profit = Simulated Net Revenue − Implied Historical Cost

The simulation is illustrative and should not be interpreted as a causal estimate or forecast.

## 9. Technology Stack

| Component | Technology |
|---|---|
| Programming | Python |
| Data manipulation | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Dashboard | Streamlit |
| Supporting analytics | Scikit-learn |
| Development | VS Code |
| Version control | Git and GitHub |

## 10. Project Structure

```text
APL_Logistics_Project/
├── app_v2.py
├── app.py
├── data_validation.py
├── data_preparation.py
├── eda_analysis.py
├── customer_analysis.py
├── discount_analysis.py
├── create_visualizations.py
├── dashboard_qa.py
├── requirements.txt
├── .gitignore
├── data/
├── reports/
└── charts/
```

## 11. Local Installation

Clone the repository and enter the project directory.

```bash
git clone <YOUR_REPOSITORY_URL>
cd APL_Logistics_Project
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Place an authorized copy of the prepared dataset at:

```text
data/APL_Logistics_cleaned.csv
```

Launch the dashboard:

```bash
python -m streamlit run app_v2.py
```

The dashboard requires access to the cleaned dataset, which is not included in the public repository.

## 12. Quality Assurance

The project includes checks for:

- Dataset row count
- Financial benchmark reconciliation
- Missing and duplicate records
- Market-level profit reconciliation
- Category-level revenue reconciliation
- Dashboard filter functionality
- Chart rendering
- Scenario interactivity
- CSV export functionality

Run dataset checks:

```bash
python dashboard_qa.py
```

## 13. Initial Business Findings

- Europe generates the largest absolute market profit.
- USCA has the highest aggregate market profit margin.
- The Consumer segment contributes the largest absolute profit.
- Fishing is the largest category by absolute profit.
- Profitability varies across customers, products, and discount bands.

These findings are descriptive and should be interpreted within the dataset's scope.

## 14. Limitations

- No reliable date field is available for time-series analysis.
- No explicit shipping cost field is available for shipping-cost attribution.
- Dataset currency is unspecified.
- Customer tiers depend on the selected analysis scope.
- Discount scenarios do not model demand elasticity.
- Results do not establish causal relationships.

## 15. Future Enhancements

- Secure, permission-controlled data access
- Automated data refresh
- Customer profitability forecasting
- Advanced pricing optimization
- Data-quality monitoring
- Production deployment and observability

---

**Project Type:** Supply Chain Analytics / Business Intelligence

**Developed for:** Unified Mentor Internship Project

**Status:** Dashboard implemented; documentation and deployment preparation in progress.
