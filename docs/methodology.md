# Methodology

1. Preserve the source file unchanged in `data/raw/`.
2. Ingest the supported tabular format into Pandas.
3. Standardize headers to snake_case, trim text and normalize explicit missing tokens.
4. Detect CSV-shifted rows using the unexpected trailing columns and primary-category mismatch.
5. Keep valid offers in interim and quarantine rejected rows with their reasons.
6. Normalize condition, availability, merchant aliases, brand case, currency, timestamps, weight and
   explicit shipping information.
7. Split comma-separated observation dates into individual rows.
8. Remove duplicate observations using product, merchant, price range, currency, sale flag and
   timestamp as the business key.
9. Split products and categories into separate normalized tables.
10. Validate required fields, unique observation IDs, valid currencies, non-negative price ranges
    and `price_min <= price_max`.
11. Write processed CSVs, build DuckDB tables/views and reconcile database row counts.

Rows are not silently deleted because of schema corruption. They are written to the rejected
interim file, where the original values, source row number and rejection reason remain inspectable.
