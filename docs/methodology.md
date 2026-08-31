# Methodology

1. Preserve downloaded Olist files in `data/raw/`.
2. Ingest required CSV tables with explicit date parsing.
3. Standardize product categories and join tables using documented keys.
4. Create analytical fields such as late-delivery and low-review indicators.
5. Run data-quality checks before writing processed outputs.
6. Load processed data into DuckDB.
7. Reconcile KPI calculations in Python/SQL.
8. Perform EDA and time/category comparisons.
9. Train a time-aware classification model for low-review risk.
10. Build two Power BI pages and manually validate important values.

Missing, unavailable and suppressed values must never automatically become zero.