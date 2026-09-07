"""Train simple price-prediction models on the team's cleaned dataset.

This script intentionally starts small:
1. Load the cleaned CSV.
2. Recreate the notebook's date/sale fields when needed.
3. Keep a small set of understandable, non-leaking features.
4. Split older observations into training and newer observations into testing.
5. Compare a median baseline, Linear Regression and Random Forest Regressor.

It does NOT clean the raw dataset and it does NOT use DuckDB.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "electronics_pricing_clean.csv"
TARGET = "price"

CATEGORICAL_FEATURES = [
    "brand_clean",
    "merchant_clean",
    "category_clean",
    "condition_clean",
    "availability_clean",
    "shipping_type",
    "sale_flag",
    "date_seen_month",
    "date_seen_year",
]


def load_clean_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the team's final cleaned CSV and prepare model-friendly fields."""
    if not path.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found at: {path}\n"
            "Place electronics_pricing_clean.csv in data/processed/ first."
        )

    df = pd.read_csv(path)

    if TARGET not in df.columns:
        raise ValueError(f"Required target column '{TARGET}' is missing.")

    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")

    if "date_seen" in df.columns:
        date_seen = pd.to_datetime(df["date_seen"], utc=True, errors="coerce")
    elif "date_seen_clean" in df.columns:
        date_seen = pd.to_datetime(df["date_seen_clean"], utc=True, errors="coerce")
    else:
        date_seen = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns, UTC]")

    df["date_seen"] = date_seen
    df["date_seen_year"] = date_seen.dt.year.astype("Int64").astype("string")
    df["date_seen_month"] = date_seen.dt.month.astype("Int64").astype("string")

    if "sale_flag" not in df.columns and "prices.isSale" in df.columns:
        df["sale_flag"] = (
            df["prices.isSale"]
            .astype("string")
            .str.lower()
            .map({"true": True, "false": False})
        )

    # Prices must be positive and known to be useful as a regression target.
    df = df[df[TARGET].notna() & (df[TARGET] > 0)].copy()

    return df


def choose_features(df: pd.DataFrame) -> list[str]:
    """Use only understandable columns that actually exist in the cleaned file."""
    features = [column for column in CATEGORICAL_FEATURES if column in df.columns]
    if not features:
        raise ValueError(
            "None of the expected modelling features were found. "
            "Check the cleaned column names before training."
        )
    return features


def chronological_split(df: pd.DataFrame, test_fraction: float = 0.20):
    """Put older dated observations in train and newer observations in test."""
    dated = df[df["date_seen"].notna()].sort_values("date_seen").copy()

    if len(dated) < max(20, int(len(df) * 0.5)):
        # If too many dates are unavailable, keep the split deterministic rather than random.
        ordered = df.reset_index(drop=True).copy()
        split_at = max(1, int(len(ordered) * (1 - test_fraction)))
        return ordered.iloc[:split_at], ordered.iloc[split_at:], "row-order fallback"

    split_at = max(1, int(len(dated) * (1 - test_fraction)))
    return dated.iloc[:split_at], dated.iloc[split_at:], "chronological date_seen"


def build_preprocessor(features: list[str]) -> ColumnTransformer:
    """Fill missing categories and convert text categories into model-readable columns."""
    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", min_frequency=2),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[("categorical", categorical, features)],
        remainder="drop",
    )


def evaluate(name: str, model, x_train, y_train, x_test, y_test) -> dict[str, float | str]:
    """Fit a model and return easy-to-explain regression metrics."""
    model.fit(x_train, y_train)
    prediction = model.predict(x_test)

    return {
        "model": name,
        "mae": float(mean_absolute_error(y_test, prediction)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, prediction))),
        "r2": float(r2_score(y_test, prediction)),
    }


def main() -> None:
    df = load_clean_data()
    features = choose_features(df)
    train, test, split_method = chronological_split(df)

    if train.empty or test.empty:
        raise ValueError("The dataset is too small to create both training and test sets.")

    x_train = train[features].copy()
    y_train = train[TARGET]
    x_test = test[features].copy()
    y_test = test[TARGET]

    preprocessor = build_preprocessor(features)

    models = {
        "median_baseline": DummyRegressor(strategy="median"),
        "linear_regression": Pipeline(
            steps=[
                ("preprocess", preprocessor),
                ("model", LinearRegression()),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("preprocess", preprocessor),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=300,
                        random_state=42,
                        n_jobs=-1,
                        min_samples_leaf=2,
                    ),
                ),
            ]
        ),
    }

    print(f"Loaded usable rows: {len(df):,}")
    print(f"Features: {features}")
    print(f"Split: {split_method} | train={len(train):,}, test={len(test):,}\n")

    results = []
    for name, model in models.items():
        # DummyRegressor does not need categorical feature preparation.
        if name == "median_baseline":
            result = evaluate(
                name,
                model,
                np.zeros((len(x_train), 1)),
                y_train,
                np.zeros((len(x_test), 1)),
                y_test,
            )
        else:
            result = evaluate(name, model, x_train, y_train, x_test, y_test)
        results.append(result)

    result_df = pd.DataFrame(results).sort_values("mae")
    print(result_df.to_string(index=False, float_format=lambda value: f"{value:,.3f}"))

    best = result_df.iloc[0]
    print(
        f"\nLowest test MAE: {best['model']} "
        f"(MAE={best['mae']:,.2f}). Compare this with the baseline before claiming improvement."
    )


if __name__ == "__main__":
    main()
