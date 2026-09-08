"""Reusable CSV ingestion helpers."""

from pathlib import Path

import kagglehub
import pandas as pd

<<<<<<< HEAD
def get_data() -> pd.DataFrame:
    # Download or get cached path to dataset
    path = kagglehub.dataset_download("arashnic/e-product-pricing")
    
    # Find the CSV file inside the downloaded directory
    csv_files = list(Path(path).glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV file found in {path}")
    
    # Read and return the dataset
    df = pd.read_csv(csv_files[0])
    return df
=======

def load_csv(path: str | Path, **read_csv_kwargs) -> pd.DataFrame:
    """Load any CSV file without modifying the source file."""
    return pd.read_csv(path, low_memory=False, **read_csv_kwargs)


def load_sample(path: str | Path) -> pd.DataFrame:
    """Backward-compatible wrapper used by older starter code."""
    return load_csv(path)
>>>>>>> c3c6abf435a1a418b85f34fc2bb32722dc355165
