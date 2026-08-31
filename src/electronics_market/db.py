"""DuckDB helpers for loading processed analytics data."""

from pathlib import Path

import duckdb
import pandas as pd


def write_orders(df: pd.DataFrame, database_path: str | Path) -> None:
    """Replace the analytics_orders table with the supplied processed data."""
    with duckdb.connect(str(database_path)) as connection:
        connection.register("orders_df", df)
        connection.execute(
            "CREATE OR REPLACE TABLE analytics_orders AS SELECT * FROM orders_df"
        )
