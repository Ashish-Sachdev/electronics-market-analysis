# Electronics E-Commerce Sales & Customer Experience Analytics

A 10-day, 8-person portfolio project using Python, Pandas, SQL/DuckDB, Power BI and machine learning.

## Objective
Build a reproducible analytics pipeline that measures electronics-category sales and customer experience and predicts the risk of a low customer review using historical e-commerce transaction data.

## MVP
- Primary data: Brazilian E-Commerce Public Dataset by Olist
- Scope: electronics-related product categories
- KPIs: GMV, units sold, average item price, average review score, late-delivery rate, low-review rate
- Dashboard: two Power BI pages
- ML: baseline classifier, Logistic Regression and Random Forest
- Database: DuckDB

## Data flow
`raw data -> ingestion -> interim -> transformation -> processed -> quality checks -> DuckDB -> SQL/EDA/ML -> Power BI`

## Repository
- `config/` mappings and configuration
- `data/` local raw/interim/processed/sample data (large/raw data should not be committed)
- `docs/` project documentation
- `notebooks/` exploratory work
- `scripts/` runnable pipeline/model entry points
- `sql/` analytical SQL
- `src/electronics_market/` reusable Python code
- `tests/` automated tests
- `dashboards/powerbi/` dashboard documentation

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .[dev]
pytest
python scripts/run_pipeline.py
python scripts/train_model.py
```

## Responsible interpretation
This project analyzes historical Olist marketplace data. It does not represent the entire current electronics market. GMV is sales value, not profit. Missing values must not be treated as zero. Predictive outputs are risk estimates, not certainties.

See `PROJECT_PLAN.md` and `docs/` for the full plan.