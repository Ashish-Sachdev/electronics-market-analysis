"""Inspect the generated DuckDB database or run a read-only SQL query."""

import argparse
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a read-only query against DuckDB.")
    parser.add_argument(
        "--database",
        type=Path,
        default=ROOT / "data" / "processed" / "electronics_market.duckdb",
    )
    parser.add_argument(
        "--query",
        default="SHOW ALL TABLES",
        help='SQL to run, for example: "SELECT * FROM latest_product_prices LIMIT 10"',
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.database.exists():
        raise FileNotFoundError(
            f"Database not found: {args.database}. Run scripts/run_pipeline.py first."
        )
    with duckdb.connect(str(args.database), read_only=True) as connection:
        print(connection.sql(args.query).df().to_string(index=False))


if __name__ == "__main__":
    main()
