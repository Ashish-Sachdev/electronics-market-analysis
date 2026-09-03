# Pipeline and DuckDB Guide

## Why there are three data stages

| Stage | Purpose | Rule |
|---|---|---|
| `data/raw/` | Original evidence from the source | Never edit in place |
| `data/interim/` | Cleaned working data and rejected-row audit trail | May be rebuilt at any time |
| `data/processed/` | Stable, analysis-ready tables and DuckDB | Only written after quality checks pass |

The separation makes errors traceable. If a processed price looks wrong, `source_row_number` links it
to interim and raw data without changing the original file.

## One-command automation

```powershell
python scripts/run_pipeline.py
```

The command performs these steps:

1. Finds the only supported file in `data/raw/`, unless `--input` is supplied.
2. Loads it without editing the source.
3. Detects the electronics pricing schema.
4. Cleans offer rows and quarantines malformed records.
5. Creates normalized product, category and price-observation tables.
6. Runs blocking quality checks.
7. Writes interim/processed CSVs, a preview and a JSON quality report.
8. Builds DuckDB and verifies that database row counts match the CSVs.

Useful options:

```powershell
python scripts/run_pipeline.py --help
python scripts/run_pipeline.py --input data/raw/my_file.csv --mode generic
python scripts/run_pipeline.py --database data/processed/my_analysis.duckdb
python scripts/run_pipeline.py --report reports/my_quality_report.json
```

`--mode auto` is the default. It selects the specialized electronics transformer when its required
columns exist and otherwise uses generic cleaning. `--mode electronics` requires the known schema.
`--mode generic` disables dataset-specific rules.

## Exact cleaning performed on the electronics file

- Changes headers from dotted/camelCase labels such as `prices.amountMin` to clear snake_case names.
- Trims text and treats explicit placeholders such as blank, `N/A`, `null` and `undefined` as missing
  where generic cleaning applies.
- Quarantines records whose values spill into unexpected `Unnamed` columns. These rows also have
  impossible primary-category values caused by CSV field shifting.
- Normalizes case-only brand variants by using the most frequent source spelling.
- Combines known merchant aliases such as `Bestbuy.com`/`Best Buy`, `Walmart.com`/`Walmart`, and
  `bhphotovideo.com`/`B&H Photo Video`.
- Maps item condition to `new`, `used`, `refurbished` or `other`.
- Maps availability to `in_stock`, `out_of_stock`, `limited_or_special_order` or `unknown`.
- Uppercases currency codes and keeps CAD separate from USD.
- Converts source timestamps to timezone-aware UTC values.
- Converts the first stated pounds/ounces/grams/kilograms weight to kilograms while retaining the
  original `weight_text`.
- Extracts a shipping price only when the source explicitly states an amount such as `USD 6.65`.
- Explodes each comma-separated `prices.dateSeen` list into individual observations.
- Removes duplicate observations using product, normalized merchant, price range, currency, sale
  flag and timestamp as the business key.
- Splits product metadata, categories and price observations into separate relational tables.

Unknown values remain missing. The code does not impute zero because zero has a real numerical
meaning and would distort analysis.

## Generic cleaning for another dataset

The generic transformer safely automates structural work:

- snake_case and unique column names;
- whitespace cleanup;
- standard missing tokens;
- removal of entirely empty columns;
- exact duplicate-row removal;
- boolean conversion when every non-missing value is an obvious yes/no token;
- numeric or UTC datetime conversion only when the column name suggests the type and at least 95%
  of non-missing values convert.

It deliberately does not guess domain rules such as whether age 150 is invalid, how categories
should be grouped, or what makes a record unique. Add a dataset-specific transformer for those
decisions, following `transform/products.py` as the example.

## Python file map

| File | Responsibility |
|---|---|
| `scripts/run_pipeline.py` | Command-line entry point; resolves arguments and runs the pipeline |
| `scripts/query_duckdb.py` | Opens the generated database read-only and prints a SQL result |
| `scripts/train_model.py` | Explains why supervised modelling is deferred for this unlabeled source |
| `src/electronics_market/ingest/load.py` | Finds and loads CSV/TSV/JSON/JSONL/XLSX/XLS files |
| `src/electronics_market/transform/generic.py` | Reusable conservative cleaning for unfamiliar tables |
| `src/electronics_market/transform/products.py` | Electronics-specific validation, mapping and relational normalization |
| `src/electronics_market/pipeline.py` | Coordinates every stage, writes outputs and assembles the report |
| `src/electronics_market/quality.py` | Validates structures, required values, price ranges, IDs and currencies |
| `src/electronics_market/db.py` | Creates DuckDB tables and analysis views |
| `src/electronics_market/transform/orders.py` | Retained legacy helper for an eventual order-level/Olist adapter |
| `src/electronics_market/models/train.py` | Retained model components for a future labeled order dataset |

Tests under `tests/` verify generic cleaning, electronics normalization, quality rules, the full
generic pipeline and DuckDB output. GitHub Actions runs both lint and tests on every push/PR.

## DuckDB setup and use

DuckDB is installed by `python -m pip install -e ".[dev]"`; no database server, account or password
is required. Running the pipeline creates `data/processed/electronics_market.duckdb` with:

- table `products`;
- table `product_categories`;
- table `price_observations`;
- view `latest_product_prices`;
- view `monthly_price_summary`.

Inspect all objects:

```powershell
python scripts/query_duckdb.py
```

Run a query:

```powershell
python scripts/query_duckdb.py --query "SELECT currency, MEDIAN(price_midpoint) AS median_price FROM price_observations GROUP BY currency"
```

Use DuckDB from a notebook:

```python
import duckdb

connection = duckdb.connect("data/processed/electronics_market.duckdb", read_only=True)
result = connection.sql("SELECT * FROM monthly_price_summary LIMIT 20").df()
connection.close()
```

Power BI can read the processed CSVs directly. This is usually simpler on Windows than depending on
an additional DuckDB ODBC driver; use DuckDB for validation, SQL exploration and reproducible KPI
logic.

## Verification commands

```powershell
python scripts/run_pipeline.py
ruff check .
pytest -q
```

Generated raw/interim/processed files and the `.duckdb` database are excluded by `.gitignore`; the
small quality report and preview are intentionally versioned so collaborators can review results.
