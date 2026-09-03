"""Orchestrate ingestion, transformation, validation, export and DuckDB loading."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

import pandas as pd

from electronics_market.db import (
    build_electronics_database,
    database_table_counts,
    write_generic_table,
)
from electronics_market.ingest.load import load_tabular
from electronics_market.quality import (
    missing_value_summary,
    require_quality,
    validate_generic_data,
    validate_price_observations,
)
from electronics_market.transform.generic import clean_generic, snake_case
from electronics_market.transform.products import (
    is_electronics_pricing_dataset,
    transform_electronics_dataset,
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(path: Path, project_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(project_root.resolve()))
    except ValueError:
        return str(path.resolve())


def _write_json(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _value_counts(series: pd.Series) -> dict[str, int]:
    return {str(key): int(value) for key, value in series.value_counts(dropna=False).items()}


def run_electronics_pipeline(
    source: Path,
    raw: pd.DataFrame,
    project_root: Path,
    interim_directory: Path,
    processed_directory: Path,
    database_path: Path,
    report_path: Path,
) -> dict:
    """Run the specialized electronics pricing pipeline and return its report."""
    offers, rejected, products, categories, observations, stats = transform_electronics_dataset(raw)
    failures = validate_price_observations(observations)
    require_quality(failures)

    interim_directory.mkdir(parents=True, exist_ok=True)
    processed_directory.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    interim_path = interim_directory / "electronics_price_offers_cleaned.csv"
    rejected_path = interim_directory / "electronics_price_offers_rejected.csv"
    products_path = processed_directory / "products.csv"
    categories_path = processed_directory / "product_categories.csv"
    observations_path = processed_directory / "price_observations.csv"
    preview_path = report_path.parent / "processed_preview.csv"

    offers.to_csv(interim_path, index=False)
    rejected.to_csv(rejected_path, index=False)
    products.to_csv(products_path, index=False)
    categories.to_csv(categories_path, index=False)
    observations.to_csv(observations_path, index=False)
    (
        observations.merge(
            products[["product_id", "product_name", "brand"]],
            on="product_id",
            how="left",
            validate="many_to_one",
        )
        .head(25)
        .to_csv(preview_path, index=False)
    )

    build_electronics_database(products, categories, observations, database_path)
    table_counts = database_table_counts(database_path)
    expected_counts = {
        "products": len(products),
        "product_categories": len(categories),
        "price_observations": len(observations),
    }
    require_quality(
        ["DuckDB row counts do not match processed CSVs"] if table_counts != expected_counts else []
    )

    usd_prices = observations.loc[observations["currency"].eq("USD"), "price_midpoint"]
    report = {
        "pipeline_mode": "electronics_pricing",
        "source": {
            "path": _relative(source, project_root),
            "sha256": _sha256(source),
            "rows": len(raw),
            "columns": len(raw.columns),
        },
        "transform": asdict(stats),
        "quality": {
            "passed": not failures,
            "failures": failures,
            "raw_missing_values": missing_value_summary(raw),
            "processed_missing_values": missing_value_summary(observations),
        },
        "profile": {
            "date_seen_min": observations["date_seen"].min().isoformat(),
            "date_seen_max": observations["date_seen"].max().isoformat(),
            "unique_merchants": int(observations["merchant_key"].nunique()),
            "currencies": _value_counts(observations["currency"]),
            "conditions": _value_counts(observations["condition"]),
            "availability": _value_counts(observations["availability_status"]),
            "sale_observations": int(observations["is_sale"].sum()),
            "sale_rate_percent": round(float(observations["is_sale"].mean() * 100), 2),
            "usd_price_midpoint": {
                "minimum": round(float(usd_prices.min()), 2),
                "median": round(float(usd_prices.median()), 2),
                "mean": round(float(usd_prices.mean()), 2),
                "maximum": round(float(usd_prices.max()), 2),
            },
        },
        "duckdb": {
            "path": _relative(database_path, project_root),
            "table_counts": table_counts,
            "views": ["latest_product_prices", "monthly_price_summary"],
        },
        "outputs": {
            "interim_cleaned": _relative(interim_path, project_root),
            "interim_rejected": _relative(rejected_path, project_root),
            "products": _relative(products_path, project_root),
            "product_categories": _relative(categories_path, project_root),
            "price_observations": _relative(observations_path, project_root),
            "preview": _relative(preview_path, project_root),
        },
    }
    _write_json(report, report_path)
    return report


def run_generic_pipeline(
    source: Path,
    raw: pd.DataFrame,
    project_root: Path,
    interim_directory: Path,
    processed_directory: Path,
    database_path: Path,
    report_path: Path,
) -> dict:
    """Run conservative structural cleaning for an arbitrary tabular dataset."""
    processed, stats = clean_generic(raw)
    failures = validate_generic_data(processed)
    require_quality(failures)

    interim_directory.mkdir(parents=True, exist_ok=True)
    processed_directory.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    stem = snake_case(source.stem)
    interim_path = interim_directory / f"{stem}_cleaned.csv"
    processed_path = processed_directory / f"{stem}_processed.csv"
    preview_path = report_path.parent / "processed_preview.csv"
    processed.to_csv(interim_path, index=False)
    processed.to_csv(processed_path, index=False)
    processed.head(25).to_csv(preview_path, index=False)
    write_generic_table(processed, database_path)

    report = {
        "pipeline_mode": "generic",
        "source": {
            "path": _relative(source, project_root),
            "sha256": _sha256(source),
            "rows": len(raw),
            "columns": len(raw.columns),
        },
        "transform": asdict(stats),
        "quality": {
            "passed": not failures,
            "failures": failures,
            "missing_values": missing_value_summary(processed),
        },
        "duckdb": {
            "path": _relative(database_path, project_root),
            "table": "processed_data",
            "rows": len(processed),
        },
        "outputs": {
            "interim_cleaned": _relative(interim_path, project_root),
            "processed": _relative(processed_path, project_root),
            "preview": _relative(preview_path, project_root),
        },
    }
    _write_json(report, report_path)
    return report


def run_pipeline(
    source: str | Path,
    *,
    project_root: str | Path,
    interim_directory: str | Path,
    processed_directory: str | Path,
    database_path: str | Path,
    report_path: str | Path,
    mode: str = "auto",
) -> dict:
    """Run an auto-detected specialized pipeline or the generic fallback."""
    source = Path(source)
    project_root = Path(project_root)
    interim_directory = Path(interim_directory)
    processed_directory = Path(processed_directory)
    database_path = Path(database_path)
    report_path = Path(report_path)
    raw = load_tabular(source)

    if mode not in {"auto", "electronics", "generic"}:
        raise ValueError("mode must be one of: auto, electronics, generic")
    detected_electronics = is_electronics_pricing_dataset(raw.columns)
    if mode == "electronics" and not detected_electronics:
        signature = {
            "id",
            "prices.amountMax",
            "prices.amountMin",
            "prices.dateSeen",
            "prices.merchant",
            "name",
        }
        missing = sorted(signature - set(raw.columns))
        raise ValueError(f"Electronics mode selected but signature columns are missing: {missing}")

    if detected_electronics and mode != "generic":
        return run_electronics_pipeline(
            source,
            raw,
            project_root,
            interim_directory,
            processed_directory,
            database_path,
            report_path,
        )
    return run_generic_pipeline(
        source,
        raw,
        project_root,
        interim_directory,
        processed_directory,
        database_path,
        report_path,
    )
