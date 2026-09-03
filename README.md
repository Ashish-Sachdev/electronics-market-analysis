# Electronics Product Pricing Analytics

A reproducible Python, Pandas, DuckDB and SQL pipeline for the uploaded
`ElectronicsProductsPricingData.csv` file.

## What the project analyzes

The source contains historical product-price observations from multiple merchants. It is not
an order or customer-review dataset, so the project measures product coverage, merchant coverage,
observed prices, availability and sale flags—not GMV, units sold, delivery performance or reviews.

## Data flow

`raw (untouched) -> ingest -> interim (clean + quarantine) -> processed (normalized tables) -> quality checks -> DuckDB -> SQL/Power BI`

Generated tables:

- `data/interim/electronics_price_offers_cleaned.csv` — one structurally valid source offer per row.
- `data/interim/electronics_price_offers_rejected.csv` — malformed rows plus rejection reasons.
- `data/processed/products.csv` — one row per product.
- `data/processed/product_categories.csv` — one row per product/category pair.
- `data/processed/price_observations.csv` — one product/merchant/price/date observation per row.
- `data/processed/electronics_market.duckdb` — the three tables plus analysis views.

## Quick start

Python 3.11 or newer is required.

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python scripts/run_pipeline.py
python scripts/query_duckdb.py
```

Example query:

```powershell
python scripts/query_duckdb.py --query "SELECT * FROM latest_product_prices LIMIT 10"
```

On macOS/Linux, activate with `source .venv/bin/activate` instead.

## Process another dataset

The command auto-detects this electronics schema. For another CSV, TSV, JSON, JSONL, XLSX or XLS
file, use the conservative generic cleaner:

```powershell
python scripts/run_pipeline.py --input data/raw/my_dataset.csv --mode generic
```

The generic mode normalizes column names, whitespace, missing tokens, obvious data types, empty
columns and exact duplicate rows. Dataset-specific business rules still require a new transformer;
the pipeline deliberately does not guess what an unfamiliar column means.

See [docs/pipeline_guide.md](docs/pipeline_guide.md) for the exact cleaning rules, script-by-script
explanation, output meanings and DuckDB workflow. The latest verified run is summarized in
`reports/data_quality_report.json`, with a small sample in `reports/processed_preview.csv`.
