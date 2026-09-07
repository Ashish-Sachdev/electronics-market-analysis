# Electronics Pricing Analysis — Current Project Plan

## Objective
Analyze historical electronics listing prices and explain how price differs across brand, merchant, product category, condition, discount status, shipping type and time. The team's cleaned dataset and `notebooks/electronics_pricing_analysis.ipynb` are the centre of the project.

## Current workflow

```text
Original dataset
  -> team cleaning completed manually
  -> electronics_pricing_clean.csv
  -> Jupyter/Colab analysis notebook
  -> charts + business findings
  -> reports + Power BI
  -> optional predictive price model
```

There is **no DuckDB step and no automated cleaning pipeline in the current workflow**.

## Business questions
1. Does actual brand pricing match the intended market position?
2. Which brands and merchants depend most on discounts?
3. Where are the strongest channel-coverage opportunities and risks?
4. Which categories offer less noisy competitive space?
5. What value do used and refurbished products offer relative to new products?

## Main analytical fields
- `price` — cleaned observed listing price
- `brand_clean` — standardized brand
- `merchant_clean` — standardized merchant/channel
- `category_clean` — standardized category
- `condition_clean` — standardized product condition
- `availability_clean` — standardized availability
- `shipping_type` — grouped shipping type
- `sale_flag` — whether the source identifies the listing as a sale
- `date_seen` — parsed observation date

## Important interpretation rule
A row is a **listing/price observation**, not proof that one unit was sold. Therefore this project should discuss observed prices, discount/sale presence and merchant/category coverage. It should not call row counts `units sold`, should not calculate GMV/revenue from row counts, and should not invent ratings or delivery KPIs that are not in this dataset.

## Deliverables
- Completed pricing-analysis notebook
- Data dictionary and methodology
- Written analysis summary in `reports/`
- Exported figures in `reports/figures/` when needed
- Power BI dashboard aligned with the notebook
- Optional price-prediction model with documented assumptions and evaluation

## Optional machine learning
The recommended target is `price`, so this is a **regression** problem. Compare:
1. Median-price baseline
2. Linear Regression
3. Random Forest Regressor

Use MAE, RMSE and R². Prefer a chronological split using `date_seen` so earlier observations train the model and later observations test it.

Avoid leakage: if `price` was created from `prices.amountMin` and `prices.amountMax`, do not use those source-price columns to predict `price`. Do not use product `id` or full product `name` as ordinary features because repeated products can make the test artificially easy.

## Team roles
| Role | Responsibility |
|---|---|
| Data cleaning | Own and document the final cleaned CSV |
| Data understanding | Verify columns, missingness, duplicate meaning and observation grain |
| Pricing EDA | Brand/category/condition price comparisons |
| Discount analysis | Sale dependence by brand and merchant |
| Channel analysis | Merchant/category coverage and shipping analysis |
| Visualization/Power BI | Build dashboard from agreed metrics |
| Predictive modelling | Build and evaluate optional price model |
| QA/documentation | Recheck notebook claims and keep README/reports consistent |

## Definition of done
The notebook runs with the documented cleaned dataset; every chart has a clear business question; reports match the notebook; no sales/revenue claims are made from listing observations; dashboard calculations can be reproduced in Pandas; model evaluation includes a simple baseline and leakage discussion; and every teammate can explain the part they contributed.