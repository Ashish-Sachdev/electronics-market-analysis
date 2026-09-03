# Electronics Pricing Analysis — Project Plan

## Objective

Build a reproducible analytics pipeline for the uploaded historical electronics pricing file.
Compare merchant coverage, observed price levels, availability, sale activity, brands and product
categories while keeping currencies separate.

## Business questions

1. Which merchants and brands have the broadest product coverage?
2. How do observed prices and sale rates change over time?
3. Which products show the widest merchant price differences?
4. How do availability and item condition differ across merchants?
5. Which categories and brands are represented in the dataset?

## Core metrics

- Price observations = count of unique product/merchant/price/date combinations.
- Products observed = distinct product IDs.
- Merchant coverage = distinct products per merchant.
- Median observed price = median price midpoint, grouped by currency.
- Sale-observation rate = sale-flagged observations / eligible observations.
- In-stock rate = explicitly in-stock observations / observations with known stock status.

## Pipeline

1. Preserve the source file in `data/raw/`.
2. Read the file without changing values.
3. Standardize headers, text, brands, merchants, condition, availability, currency, dates and units.
4. Quarantine structurally shifted rows with reasons.
5. Split repeated date/category lists into normalized tables.
6. Deduplicate price observations using the documented business key.
7. Stop on failed data-quality checks.
8. Export processed CSVs and build DuckDB tables/views.
9. Reconcile SQL results against the quality report before dashboard work.

## Definition of done

The one-command pipeline reruns from the untouched source; rejected records remain auditable;
processed tables have documented grains and keys; tests and lint pass; DuckDB row counts equal CSV
row counts; currency is included in price aggregations; missing values are never replaced with zero;
and limitations are visible in the README and dashboard.

## Current limitation

The uploaded file has no transactions, quantities, customers, review scores or delivery fields.
Therefore, it cannot support GMV, units sold, review-risk modelling or delivery KPIs. Those analyses
need a compatible order-level dataset such as Olist and belong in a separate pipeline adapter.
