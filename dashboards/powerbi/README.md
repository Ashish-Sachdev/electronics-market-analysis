# Power BI dashboard

Use `data/processed/price_observations.csv`, `products.csv` and `product_categories.csv`.

Recommended relationships:

- `products[product_id]` 1 → many `price_observations[product_id]`
- `products[product_id]` 1 → many `product_categories[product_id]`

## Page 1 — Price and coverage overview

Cards: products observed, merchants observed, price observations and median observed price.

Charts: observations over time, merchant product coverage, median price by merchant, brand/category
coverage. Filters: currency, year/month, brand, merchant, category and condition.

## Page 2 — Availability and sale observations

Cards: sale-observation rate and known in-stock rate.

Charts: sale rate by merchant, availability status, latest cross-merchant product price spread and
price distributions by condition.

Do not sum observed prices as revenue or GMV. Keep currency in every price visual/filter, and label
observation counts as data coverage—not units sold.
