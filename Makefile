.PHONY: install test lint pipeline model

install:
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

pipeline:
	python scripts/run_pipeline.py

model:
	python scripts/train_model.py
