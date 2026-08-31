# Repository Guide

- `.github/workflows/` — automated quality checks.
- `config/` — mappings and settings used by code.
- `data/raw/` — untouched source files; local only except instructions.
- `data/interim/` — temporary cleaned/joined outputs.
- `data/processed/` — final analysis-ready outputs.
- `data/external/` — supplementary external sources.
- `data/sample/` — tiny synthetic examples for learning/tests.
- `dashboards/` — dashboard documentation and, if appropriate, lightweight assets.
- `docs/` — definitions, methodology, roadmap and team decisions.
- `notebooks/` — exploratory analysis; not the main production pipeline.
- `reports/figures/` — generated figures used in reports/README.
- `scripts/` — simple commands that run pipeline/model workflows.
- `sql/` — reusable SQL queries and views.
- `src/electronics_market/` — reusable Python package for ingestion, transformation, quality, database and ML.
- `tests/` — automated checks of code behaviour.

Git does not store empty folders, so `.gitkeep` files are used where a directory needs to exist before it contains generated data.