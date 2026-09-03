"""DuckDB writers for generic and electronics-specific processed data."""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


def _prepare_database_path(database_path: str | Path) -> Path:
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_generic_table(
    df: pd.DataFrame,
    database_path: str | Path,
    table_name: str = "processed_data",
) -> None:
    """Replace one generic DuckDB table with a processed DataFrame."""
    if not table_name.replace("_", "").isalnum():
        raise ValueError("table_name may only contain letters, numbers and underscores")
    path = _prepare_database_path(database_path)
    with duckdb.connect(str(path)) as connection:
        connection.register("incoming_df", df)
        connection.execute(f'CREATE OR REPLACE TABLE "{table_name}" AS SELECT * FROM incoming_df')


def build_electronics_database(
    products: pd.DataFrame,
    product_categories: pd.DataFrame,
    price_observations: pd.DataFrame,
    database_path: str | Path,
) -> None:
    """Build normalized DuckDB tables plus analysis-ready views."""
    path = _prepare_database_path(database_path)
    with duckdb.connect(str(path)) as connection:
        connection.register("products_df", products)
        connection.register("categories_df", product_categories)
        connection.register("observations_df", price_observations)
        connection.execute("CREATE OR REPLACE TABLE products AS SELECT * FROM products_df")
        connection.execute(
            "CREATE OR REPLACE TABLE product_categories AS SELECT * FROM categories_df"
        )
        connection.execute(
            "CREATE OR REPLACE TABLE price_observations AS SELECT * FROM observations_df"
        )
        connection.execute(
            """
            CREATE OR REPLACE VIEW latest_product_prices AS
            SELECT * EXCLUDE (price_rank)
            FROM (
                SELECT
                    o.*,
                    p.product_name,
                    p.brand,
                    p.primary_category,
                    ROW_NUMBER() OVER (
                        PARTITION BY o.product_id, o.merchant_key
                        ORDER BY o.date_seen DESC, o.observation_id DESC
                    ) AS price_rank
                FROM price_observations AS o
                JOIN products AS p USING (product_id)
            )
            WHERE price_rank = 1
            """
        )
        connection.execute(
            """
            CREATE OR REPLACE VIEW monthly_price_summary AS
            SELECT
                year_month,
                currency,
                merchant,
                COUNT(*) AS observations,
                COUNT(DISTINCT product_id) AS products,
                ROUND(AVG(price_midpoint), 2) AS average_price,
                ROUND(MEDIAN(price_midpoint), 2) AS median_price,
                ROUND(AVG(CASE WHEN is_sale THEN 1.0 ELSE 0.0 END), 4) AS sale_rate
            FROM price_observations
            GROUP BY year_month, currency, merchant
            """
        )


def database_table_counts(database_path: str | Path) -> dict[str, int]:
    """Return row counts used to verify that DuckDB matches exported CSVs."""
    with duckdb.connect(str(database_path), read_only=True) as connection:
        tables = ["products", "product_categories", "price_observations"]
        return {
            table: int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
            for table in tables
        }


def write_orders(df: pd.DataFrame, database_path: str | Path) -> None:
    """Backward-compatible writer for the original starter code."""
    write_generic_table(df, database_path, table_name="analytics_orders")
