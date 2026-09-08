"""Read source or sample CSV files without changing them."""

from pathlib import Path

import kagglehub
import pandas as pd

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
