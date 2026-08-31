"""Train starter low-review classification models."""

from pathlib import Path

import pandas as pd

from electronics_market.models.train import train_models
from electronics_market.transform.orders import prepare_orders

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    path = ROOT / "data" / "sample" / "electronics_orders_sample.csv"
    df = prepare_orders(pd.read_csv(path))
    results = train_models(df)
    for model, metrics in results.items():
        print(model, metrics)


if __name__ == "__main__":
    main()
