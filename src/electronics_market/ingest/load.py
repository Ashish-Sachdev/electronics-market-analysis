"""Read source or sample CSV files without changing them."""

from pathlib import Path

import pandas as pd


def load_sample(path: str | Path) -> pd.DataFrame:
    """Load a CSV into a DataFrame."""
    return pd.read_csv(path)
