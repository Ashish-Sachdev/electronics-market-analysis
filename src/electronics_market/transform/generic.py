"""Conservative cleaning rules that work for ordinary tabular datasets."""

from __future__ import annotations

import re
from dataclasses import dataclass

import pandas as pd

MISSING_TOKENS = {"", "-", "--", "n/a", "na", "nan", "none", "null", "undefined"}
TRUE_TOKENS = {"true", "yes", "y"}
FALSE_TOKENS = {"false", "no", "n"}


@dataclass(frozen=True)
class GenericCleaningStats:
    input_rows: int
    output_rows: int
    renamed_columns: int
    empty_columns_removed: tuple[str, ...]
    duplicate_rows_removed: int


def snake_case(value: object) -> str:
    """Convert a label to a stable lowercase snake_case identifier."""
    text = str(value).strip()
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()
    return text or "column"


def normalize_column_names(columns) -> list[str]:
    """Normalize names and make collisions explicit with numeric suffixes."""
    normalized: list[str] = []
    counts: dict[str, int] = {}
    for column in columns:
        base = snake_case(column)
        counts[base] = counts.get(base, 0) + 1
        normalized.append(base if counts[base] == 1 else f"{base}_{counts[base]}")
    return normalized


def _clean_text(series: pd.Series) -> pd.Series:
    cleaned = series.astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
    missing = cleaned.str.casefold().isin(MISSING_TOKENS)
    return cleaned.mask(missing, pd.NA)


def _maybe_boolean(series: pd.Series) -> pd.Series:
    values = series.dropna().astype("string").str.casefold()
    if values.empty or not values.isin(TRUE_TOKENS | FALSE_TOKENS).all():
        return series
    lookup = {**{value: True for value in TRUE_TOKENS}, **{value: False for value in FALSE_TOKENS}}
    return series.astype("string").str.casefold().map(lookup).astype("boolean")


def _maybe_numeric(name: str, series: pd.Series) -> pd.Series:
    numeric_hint = re.search(
        r"(^|_)(amount|min|max|price|cost|rate|score|quantity|count|total|value|age)($|_)",
        name,
    )
    if not numeric_hint or not isinstance(series.dtype, pd.StringDtype):
        return series
    converted = pd.to_numeric(series.str.replace(r"[$,%]", "", regex=True), errors="coerce")
    non_missing = int(series.notna().sum())
    if non_missing and converted.notna().sum() / non_missing >= 0.95:
        return converted
    return series


def _maybe_datetime(name: str, series: pd.Series) -> pd.Series:
    date_hint = re.search(r"(^|_)(date|datetime|timestamp|time|created|updated)($|_)", name)
    if not date_hint or not isinstance(series.dtype, pd.StringDtype):
        return series
    converted = pd.to_datetime(series, errors="coerce", utc=True)
    non_missing = int(series.notna().sum())
    if non_missing and converted.notna().sum() / non_missing >= 0.95:
        return converted
    return series


def clean_generic(
    df: pd.DataFrame,
    *,
    drop_empty_columns: bool = True,
    deduplicate: bool = True,
    infer_types: bool = True,
) -> tuple[pd.DataFrame, GenericCleaningStats]:
    """Apply safe structural cleaning without inventing business rules.

    This function standardizes headers, whitespace and missing tokens. It only
    converts a text column when its name suggests a type and at least 95% of its
    non-missing values convert successfully.
    """
    result = df.copy()
    original_columns = [str(column) for column in result.columns]
    result.columns = normalize_column_names(result.columns)
    renamed_columns = sum(a != b for a, b in zip(original_columns, result.columns))

    for column in result.select_dtypes(include=["object", "string"]).columns:
        result[column] = _clean_text(result[column])

    empty_columns: list[str] = []
    if drop_empty_columns:
        empty_columns = [column for column in result.columns if result[column].isna().all()]
        result = result.drop(columns=empty_columns)

    if infer_types:
        for column in list(result.columns):
            result[column] = _maybe_boolean(result[column])
            result[column] = _maybe_numeric(column, result[column])
            result[column] = _maybe_datetime(column, result[column])

    duplicates = int(result.duplicated().sum()) if deduplicate else 0
    if deduplicate:
        result = result.drop_duplicates().reset_index(drop=True)

    stats = GenericCleaningStats(
        input_rows=len(df),
        output_rows=len(result),
        renamed_columns=renamed_columns,
        empty_columns_removed=tuple(empty_columns),
        duplicate_rows_removed=duplicates,
    )
    return result, stats
