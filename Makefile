.PHONY: install notebook lint model

install:
	python -m pip install -e ".[dev,notebook]"

notebook:
	jupyter lab

lint:
	ruff check scripts

model:
	python scripts/train_price_model.py
