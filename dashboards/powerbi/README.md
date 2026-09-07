# Power BI Dashboard — Electronics Pricing Analysis

The dashboard should answer the same questions as `notebooks/electronics_pricing_analysis.ipynb`. This is a pricing/listing dataset, not a sales-transaction dataset.

## Page 1 — Pricing & Market Position
Suggested KPI cards:
- Number of listing observations
- Unique products
- Unique brands
- Unique merchants
- Median observed price
- Average observed price

Suggested visuals:
- Median price by `brand_clean`
- Median/average price by `category_clean`
- Price distribution by `condition_clean`
- Price distribution by category
- Price trend over `date_seen` where coverage is sufficient

Useful slicers:
- Brand
- Merchant
- Category
- Condition
- Sale flag
- Shipping type
- Date

## Page 2 — Discount & Channel Strategy
Suggested KPI cards:
- Sale-listed share (`sale_flag`)
- Number of merchants
- Number of categories
- Median price for new products
- Median price for used/refurbished products, when those groups have enough observations

Suggested visuals:
- Sale share by merchant
- Sale share by brand
- Merchant coverage by category
- Category × merchant matrix
- Price by shipping type
- New vs used/refurbished price comparison

## Optional Page 3 — Predictive Model
Only add this after the model has been evaluated.

Show:
- Baseline MAE vs model MAE
- RMSE and R²
- Actual vs predicted price chart
- Top model features or permutation importance
- Clear note that predictions reproduce historical listing-price patterns; they are not guaranteed future market prices

## Interpretation rules
- One row is an observed listing/price record, **not one sold unit**.
- Do not label row count as units sold.
- Do not calculate revenue/GMV by multiplying listing prices by row count.
- `sale_flag` indicates a listing marked as sale; it does not by itself prove a specific discount percentage.
- Missing values should remain missing unless the team documents an imputation rule.