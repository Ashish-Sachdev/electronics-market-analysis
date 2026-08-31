"""Run the MVP analytics pipeline."""

from pathlib import Path

from electronics_market.ingest.load import load_sample
from electronics_market.transform.orders import prepare_orders
from electronics_market.quality import validate_orders

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source = ROOT / "data" / "sample" / "electronics_orders_sample.csv"
    output = ROOT / "data" / "processed" / "electronics_orders.csv"
    df = load_sample(source)
    processed = prepare_orders(df)
    validate_orders(processed)
    output.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(output, index=False)
    print(f"Pipeline complete: {len(processed)} rows -> {output}")


if __name__ == "__main__":
    main()
