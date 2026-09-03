.PHONY: install test lint pipeline database model

install:
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

pipeline:
	python scripts/run_pipeline.py

database:
	python scripts/query_duckdb.py

model:
	python scripts/train_model.py
