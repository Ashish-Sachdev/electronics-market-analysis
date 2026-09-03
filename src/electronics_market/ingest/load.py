"""Reusable CSV ingestion helpers."""

from pathlib import Path

import pandas as pd


def load_csv(path: str | Path, **read_csv_kwargs) -> pd.DataFrame:
    """Load any CSV file without modifying the source file."""
    return pd.read_csv(path, low_memory=False, **read_csv_kwargs)


def load_sample(path: str | Path) -> pd.DataFrame:
    """Backward-compatible wrapper used by older starter code."""
    return load_csv(path)
