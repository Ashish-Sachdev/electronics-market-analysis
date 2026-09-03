"""Dataset-specific transformations for electronics price observations."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

import pandas as pd

from electronics_market.transform.generic import clean_generic, snake_case

ELECTRONICS_SIGNATURE = {
    "id",
    "prices.amountMax",
    "prices.amountMin",
    "prices.dateSeen",
    "prices.merchant",
    "name",
}

PRODUCT_COLUMNS = [
    "product_id",
    "product_name",
    "brand",
    "manufacturer",
    "manufacturer_number",
    "primary_category",
    "categories",
    "asins",
    "ean",
    "upc",
    "weight_text",
    "weight_kg",
    "date_added",
    "date_updated",
]

OBSERVATION_COLUMNS = [
    "observation_id",
    "offer_id",
    "product_id",
    "merchant",
    "merchant_key",
    "currency",
    "condition",
    "availability_status",
    "is_available",
    "is_sale",
    "price_min",
    "price_max",
    "price_midpoint",
    "price_spread",
    "shipping_text",
    "shipping_cost",
    "shipping_is_free",
    "date_seen",
    "date_seen_date",
    "year",
    "month",
    "year_month",
    "source_url",
    "source_row_number",
]


@dataclass(frozen=True)
class ElectronicsTransformStats:
    raw_rows: int
    valid_offer_rows: int
    rejected_rows: int
    observation_rows_before_deduplication: int
    duplicate_observations_removed: int
    processed_observations: int
    products: int
    product_categories: int


def is_electronics_pricing_dataset(columns) -> bool:
    """Return True when the Datafiniti electronics pricing signature is present."""
    return ELECTRONICS_SIGNATURE.issubset(set(columns))


def _canonical_by_case(series: pd.Series) -> pd.Series:
    """Collapse case-only variants while keeping the most frequent spelling."""
    values = series.astype("string")
    keys = values.str.casefold()
    counts = (
        pd.DataFrame({"key": keys, "value": values})
        .dropna()
        .value_counts()
        .rename("count")
        .reset_index()
        .sort_values(["key", "count", "value"], ascending=[True, False, True])
    )
    mapping = counts.drop_duplicates("key").set_index("key")["value"]
    return keys.map(mapping).astype("string")


def _standardize_condition(value: object) -> str:
    text = str(value).strip().casefold()
    if "refurbished" in text:
        return "refurbished"
    if text == "used" or "pre-owned" in text:
        return "used"
    if text.startswith("new"):
        return "new"
    return "other"


def _standardize_availability(value: object) -> str:
    text = str(value).strip().casefold()
    if text in {"in stock", "yes", "true"} or re.fullmatch(r"\d+ available", text):
        return "in_stock"
    if text in {"out of stock", "no", "false", "sold", "retired"}:
        return "out_of_stock"
    if text in {"special order", "more on the way"}:
        return "limited_or_special_order"
    return "unknown"


def _standardize_merchant(series: pd.Series) -> pd.Series:
    aliases = {
        "bestbuy.com": "Best Buy",
        "best buy": "Best Buy",
        "bhphotovideo.com": "B&H Photo Video",
        "b&h photo video": "B&H Photo Video",
        "walmart.com": "Walmart",
        "walmart": "Walmart",
        "buydig": "BuyDig",
    }
    canonical = _canonical_by_case(series)
    keys = series.astype("string").str.casefold()
    return keys.map(aliases).fillna(canonical).astype("string")


def _weight_to_kg(series: pd.Series) -> pd.Series:
    extracted = series.astype("string").str.extract(
        r"(?i)^\s*([-+]?\d*\.?\d+)\s*(pounds?|lbs?\.?|ounces?|oz\.?|kilograms?|kgs?\.?|grams?|g)\b"
    )
    amount = pd.to_numeric(extracted[0], errors="coerce")
    unit = extracted[1].str.casefold().str.rstrip(".")
    factor = unit.map(
        {
            "pound": 0.45359237,
            "pounds": 0.45359237,
            "lb": 0.45359237,
            "lbs": 0.45359237,
            "ounce": 0.028349523125,
            "ounces": 0.028349523125,
            "oz": 0.028349523125,
            "kilogram": 1.0,
            "kilograms": 1.0,
            "kg": 1.0,
            "kgs": 1.0,
            "gram": 0.001,
            "grams": 0.001,
            "g": 0.001,
        }
    )
    return (amount * factor).round(6)


def _shipping_cost(series: pd.Series) -> pd.Series:
    extracted = series.astype("string").str.extract(r"(?i)\bUSD\s*([0-9]+(?:\.[0-9]+)?)")[0]
    return pd.to_numeric(extracted, errors="coerce")


def _shipping_is_free(series: pd.Series) -> pd.Series:
    text = series.astype("string").str.casefold()
    result = pd.Series(pd.NA, index=series.index, dtype="boolean")
    result.loc[text.str.contains("free", na=False)] = True
    charged = text.str.contains(r"\busd\s*\d|charges apply|freight", regex=True, na=False)
    result.loc[charged] = False
    return result


def clean_electronics_offers(
    raw: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Clean offer rows and quarantine structurally shifted CSV records."""
    cleaned, _ = clean_generic(
        raw,
        drop_empty_columns=False,
        deduplicate=False,
        infer_types=False,
    )
    cleaned.insert(0, "source_row_number", cleaned.index + 2)

    extra_columns = [column for column in cleaned if column.startswith("unnamed_")]
    shifted = cleaned[extra_columns].notna().any(axis=1)
    unexpected_category = ~cleaned["primary_categories"].str.contains(
        "electronics", case=False, na=False
    )

    reasons = pd.Series("", index=cleaned.index, dtype="string")
    reasons.loc[shifted] = "malformed_csv_alignment"
    reasons.loc[unexpected_category] = (
        reasons.loc[unexpected_category]
        .mask(reasons.loc[unexpected_category].eq(""), "unexpected_primary_category")
        .where(
            reasons.loc[unexpected_category].eq(""),
            reasons.loc[unexpected_category] + ";unexpected_primary_category",
        )
    )
    rejected_mask = shifted | unexpected_category
    rejected = cleaned.loc[rejected_mask].copy()
    rejected.insert(1, "rejection_reason", reasons.loc[rejected_mask])

    offers = cleaned.loc[~rejected_mask].drop(columns=extra_columns).copy()
    offers = offers.rename(
        columns={
            "id": "product_id",
            "name": "product_name",
            "prices_amount_min": "price_min",
            "prices_amount_max": "price_max",
            "prices_availability": "availability_raw",
            "prices_condition": "condition_raw",
            "prices_currency": "currency",
            "prices_date_seen": "date_seen_raw",
            "prices_is_sale": "is_sale",
            "prices_merchant": "merchant_raw",
            "prices_shipping": "shipping_text",
            "prices_source_urls": "source_url",
            "primary_categories": "primary_category",
            "manufacturer_number": "manufacturer_number",
            "date_added": "date_added",
            "date_updated": "date_updated",
            "weight": "weight_text",
        }
    )

    offers["brand"] = _canonical_by_case(offers["brand"])
    offers["merchant"] = _standardize_merchant(offers["merchant_raw"])
    offers["merchant_key"] = offers["merchant"].map(snake_case)
    offers["condition"] = offers["condition_raw"].map(_standardize_condition)
    offers["availability_status"] = offers["availability_raw"].map(_standardize_availability)
    availability_lookup = {"in_stock": True, "out_of_stock": False}
    offers["is_available"] = (
        offers["availability_status"].map(availability_lookup).astype("boolean")
    )
    offers["currency"] = offers["currency"].str.upper()
    offers["is_sale"] = offers["is_sale"].astype("boolean")
    offers["date_added"] = pd.to_datetime(offers["date_added"], errors="coerce", utc=True)
    offers["date_updated"] = pd.to_datetime(offers["date_updated"], errors="coerce", utc=True)
    offers["weight_kg"] = _weight_to_kg(offers["weight_text"])
    offers["shipping_cost"] = _shipping_cost(offers["shipping_text"])
    offers["shipping_is_free"] = _shipping_is_free(offers["shipping_text"])
    offers["offer_id"] = offers["source_row_number"].map(lambda value: f"offer_{value:07d}")
    return offers.reset_index(drop=True), rejected.reset_index(drop=True)


def _observation_id(row: pd.Series) -> str:
    fields = [
        row["product_id"],
        row["merchant_key"],
        row["currency"],
        f"{row['price_min']:.6f}",
        f"{row['price_max']:.6f}",
        str(bool(row["is_sale"])),
        row["date_seen"].isoformat(),
    ]
    return hashlib.sha256("|".join(fields).encode("utf-8")).hexdigest()[:20]


def normalize_electronics_tables(
    offers: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, int, int]:
    """Create product, category and price-observation tables in first normal form."""
    products = (
        offers.sort_values(["date_updated", "source_row_number"])
        .drop_duplicates("product_id", keep="last")
        .rename(columns={"categories": "categories"})
    )
    products = products[PRODUCT_COLUMNS].sort_values("product_id").reset_index(drop=True)

    product_categories = products[["product_id", "categories"]].copy()
    product_categories["category"] = product_categories["categories"].str.split(",")
    product_categories = product_categories.explode("category").drop(columns="categories")
    product_categories["category"] = product_categories["category"].str.strip()
    product_categories["category_key"] = product_categories["category"].map(snake_case)
    product_categories = (
        product_categories.dropna(subset=["category"])
        .drop_duplicates(["product_id", "category_key"])
        .sort_values(["product_id", "category_key"])
        .reset_index(drop=True)
    )

    observations = offers.copy()
    observations["date_seen"] = observations["date_seen_raw"].str.split(",")
    observations = observations.explode("date_seen")
    observations["date_seen"] = pd.to_datetime(
        observations["date_seen"].str.strip(), errors="coerce", utc=True
    )
    observations = observations.dropna(subset=["date_seen"])
    before_deduplication = len(observations)
    observation_key = [
        "product_id",
        "merchant_key",
        "price_min",
        "price_max",
        "currency",
        "is_sale",
        "date_seen",
    ]
    observations = observations.sort_values("source_row_number").drop_duplicates(observation_key)
    duplicates_removed = before_deduplication - len(observations)

    observations["price_midpoint"] = (
        (observations["price_min"] + observations["price_max"]) / 2
    ).round(2)
    observations["price_spread"] = (observations["price_max"] - observations["price_min"]).round(2)
    observations["date_seen_date"] = observations["date_seen"].dt.date
    observations["year"] = observations["date_seen"].dt.year.astype("int16")
    observations["month"] = observations["date_seen"].dt.month.astype("int8")
    observations["year_month"] = observations["date_seen"].dt.strftime("%Y-%m")
    observations["observation_id"] = observations.apply(_observation_id, axis=1)
    observations = (
        observations[OBSERVATION_COLUMNS]
        .sort_values(["date_seen", "product_id", "merchant_key"])
        .reset_index(drop=True)
    )

    return (
        products,
        product_categories,
        observations,
        before_deduplication,
        duplicates_removed,
    )


def transform_electronics_dataset(
    raw: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    ElectronicsTransformStats,
]:
    """Run the complete electronics-specific transformation in memory."""
    offers, rejected = clean_electronics_offers(raw)
    products, categories, observations, before, duplicates = normalize_electronics_tables(offers)
    stats = ElectronicsTransformStats(
        raw_rows=len(raw),
        valid_offer_rows=len(offers),
        rejected_rows=len(rejected),
        observation_rows_before_deduplication=before,
        duplicate_observations_removed=duplicates,
        processed_observations=len(observations),
        products=len(products),
        product_categories=len(categories),
    )
    return offers, rejected, products, categories, observations, stats
