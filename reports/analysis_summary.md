# Electronics Pricing Analysis — Report Summary

## Dataset used by the notebook
The saved notebook run loads **7,235 rows and 35 columns** from a cleaned file named `electronics_pricing_clean.csv`.

The analysis includes cleaned fields such as:
- `price`
- `brand_clean`
- `merchant_clean`
- `category_clean`
- `condition_clean`
- `availability_clean`
- `shipping_type`
- `date_seen_clean`

It also creates:
- `date_seen` — parsed datetime version of `date_seen_clean`
- `sale_flag` — Boolean version of `prices.isSale`

## Business questions
1. Does actual brand pricing match the intended market position?
2. Which brands and merchants depend most on discounts?
3. Where are the strongest channel-coverage opportunities and risks?
4. Which categories offer less noisy competitive space?
5. What value do used and refurbished products offer relative to new products?

## What the notebook is doing
The notebook combines data-quality inspection, cleaning/normalization checks, descriptive statistics, outlier analysis, correlation checks and visual comparisons. The goal is to turn individual listing observations into understandable pricing and channel insights.

## How to interpret the data correctly
This dataset contains **observed product/listing prices**. A row should not automatically be interpreted as a completed sale.

Therefore:
- row count is not `units sold`
- `price × row count` is not revenue or GMV
- `sale_flag` means a source listing was marked as a sale; it does not automatically tell us the exact discount percentage
- brands/products that appear many times may have more influence on row-level averages than products observed only once
- merchant coverage reflects the listings captured by the source dataset, not necessarily the merchant's complete inventory

## Recommended descriptive measures
For skewed price data, report **median price** alongside average price. Useful summaries include:
- median/average price by brand
- median/average price by category
- price distribution by condition
- sale-listed share by merchant and brand
- merchant count/coverage by category
- observed price trends over time

## Current reproducibility issue
The notebook currently points to a personal Google Drive path, while the GitHub repository does not currently contain `data/processed/electronics_pricing_clean.csv`. Before final submission, the team should either add the cleaned CSV to the documented project location (if sharing/licensing permits) or provide exact download/copy instructions and a relative path.

## Predictive extension
A useful optional extension is to predict `price` from non-price attributes such as brand, merchant, category, condition, shipping type, sale status and date-derived features. This is a regression task. See `predictive_model_guide.md` for the workflow.

## Final-report checklist
Before presenting, replace this section with verified notebook findings: the strongest brand/category price differences, merchants with the highest sale-listed share, important channel gaps, condition-related price differences, and any time trends that have enough observations to support interpretation.