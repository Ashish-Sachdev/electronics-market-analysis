"""Data-quality checks and compact profiling summaries."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

ELECTRONICS_REQUIRED_COLUMNS = {
    "observation_id",
    "product_id",
    "merchant",
    "currency",
    "price_min",
    "price_max",
    "date_seen",
}


class DataQualityError(ValueError):
    """Raised when processed data is unsafe to publish."""


def validate_generic_data(df: pd.DataFrame) -> list[str]:
    """Return structural failures applicable to any processed table."""
    failures: list[str] = []
    if df.empty:
        failures.append("processed data contains no rows")
    if not df.columns.is_unique:
        failures.append("processed data contains duplicate column names")
    if any(not str(column).strip() for column in df.columns):
        failures.append("processed data contains a blank column name")
    if df.isna().all(axis=0).any():
        empty = sorted(df.columns[df.isna().all(axis=0)].tolist())
        failures.append(f"processed data contains completely empty columns: {empty}")
    return failures


def validate_price_observations(df: pd.DataFrame) -> list[str]:
    """Return failures for the normalized electronics price-observation fact."""
    # Optional derived columns such as shipping_cost may be entirely missing in a
    # small input, so only the core structural checks are shared here.
    failures: list[str] = []
    if df.empty:
        failures.append("processed data contains no rows")
    if not df.columns.is_unique:
        failures.append("processed data contains duplicate column names")
    if any(not str(column).strip() for column in df.columns):
        failures.append("processed data contains a blank column name")
    missing = ELECTRONICS_REQUIRED_COLUMNS - set(df.columns)
    if missing:
        failures.append(f"missing required columns: {sorted(missing)}")
        return failures

    for column in ["observation_id", "product_id", "merchant", "currency", "date_seen"]:
        if df[column].isna().any():
            failures.append(f"{column} contains missing values")
    if df["observation_id"].duplicated().any():
        failures.append("observation_id contains duplicate values")
    if df[["price_min", "price_max"]].isna().any(axis=1).any():
        failures.append("price_min or price_max contains missing values")
    if (df[["price_min", "price_max"]] < 0).any(axis=None):
        failures.append("price_min or price_max contains negative values")
    if (df["price_min"] > df["price_max"]).any():
        failures.append("price_min is greater than price_max")
    valid_currency = df["currency"].astype("string").str.fullmatch(r"[A-Z]{3}", na=False)
    if not valid_currency.all():
        failures.append("currency contains a value that is not a three-letter code")
    return failures


def require_quality(failures: Iterable[str]) -> None:
    """Stop the pipeline when any validation failed."""
    failures = list(failures)
    if failures:
        details = "\n- ".join(failures)
        raise DataQualityError(f"Data-quality checks failed:\n- {details}")


def missing_value_summary(df: pd.DataFrame) -> dict[str, dict[str, float | int]]:
    """Return missing counts and percentages for columns containing missing data."""
    summary: dict[str, dict[str, float | int]] = {}
    for column, count in df.isna().sum().items():
        if count:
            summary[str(column)] = {
                "count": int(count),
                "percent": round(float(count / len(df) * 100), 2) if len(df) else 0.0,
            }
    return summary


# Compatibility helper retained for the original starter tests and notebooks.
REQUIRED_COLUMNS = {"order_id", "product_id", "price", "review_score"}


def validate_processed_data(df: pd.DataFrame) -> list[str]:
    """Validate the earlier Olist-shaped starter table."""
    failures: list[str] = []
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        failures.append(f"Missing required columns: {sorted(missing)}")
        return failures
    if df["order_id"].isna().any():
        failures.append("order_id contains missing values")
    if (df["price"].dropna() < 0).any():
        failures.append("price contains negative values")
    if not df["review_score"].dropna().between(1, 5).all():
        failures.append("review_score contains values outside 1-5")
    return failures
