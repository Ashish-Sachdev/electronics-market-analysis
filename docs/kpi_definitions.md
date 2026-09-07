# Pricing Metrics and KPI Definitions

Because this dataset contains observed listings/prices rather than confirmed sales transactions, use pricing and coverage metrics instead of GMV, revenue or units sold.

| Metric | Definition | Interpretation |
|---|---|---|
| Listing observations | Number of analysis rows | Data coverage, not units sold |
| Unique products | Distinct product identifier count | Number of distinct products represented |
| Unique brands | Distinct `brand_clean` count | Brand coverage |
| Unique merchants | Distinct `merchant_clean` count | Channel coverage |
| Average price | Mean of valid `price` | Sensitive to expensive outliers |
| Median price | Median of valid `price` | Preferred central price summary when skewed |
| Sale-listed share | Mean of Boolean `sale_flag` among known observations | Share of observed listings marked as sale |
| Category coverage | Listing/product/merchant counts by `category_clean` | How much of the captured dataset each category represents |
| Condition price gap | Difference or ratio between median prices by `condition_clean` | Descriptive comparison, not causal effect |

## Do not use
- `units sold` unless the dataset explicitly contains true quantities sold
- revenue/GMV calculated as `price × row count`
- review or delivery KPIs that do not exist in this dataset

For all dashboard metrics, document the denominator and treatment of missing values.