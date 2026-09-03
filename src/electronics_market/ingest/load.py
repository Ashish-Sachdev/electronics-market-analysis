"""Read tabular source files without changing the raw data."""

from pathlib import Path

import pandas as pd

SUPPORTED_SUFFIXES = {".csv", ".tsv", ".json", ".jsonl", ".xlsx", ".xls"}


def load_tabular(path: str | Path, **read_kwargs) -> pd.DataFrame:
    """Load a supported tabular file into a DataFrame.

    Ingestion deliberately does not clean values. Keeping reading separate from
    transformation makes the raw -> interim boundary explicit and reproducible.
    """
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Input file does not exist: {source}")

    suffix = source.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_SUFFIXES))
        raise ValueError(f"Unsupported file type {suffix!r}. Supported: {supported}")

    if suffix == ".csv":
        options = {"low_memory": False, **read_kwargs}
        return pd.read_csv(source, **options)
    if suffix == ".tsv":
        return pd.read_csv(source, sep="\t", low_memory=False, **read_kwargs)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(source, **read_kwargs)
    if suffix == ".jsonl":
        return pd.read_json(source, lines=True, **read_kwargs)
    return pd.read_json(source, **read_kwargs)


def discover_input(raw_directory: str | Path) -> Path:
    """Return the only supported data file in a raw-data directory."""
    raw_directory = Path(raw_directory)
    candidates = sorted(
        path
        for path in raw_directory.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )
    if not candidates:
        raise FileNotFoundError(f"No supported data file found in {raw_directory}")
    if len(candidates) > 1:
        names = ", ".join(path.name for path in candidates)
        raise ValueError(f"Multiple raw data files found ({names}); pass --input explicitly")
    return candidates[0]


def load_csv(path: str | Path, **read_csv_kwargs) -> pd.DataFrame:
    """Load any CSV file without modifying the source file."""
    return load_tabular(path, **read_csv_kwargs)


def load_sample(path: str | Path) -> pd.DataFrame:
    """Backward-compatible wrapper used by older starter code."""
    return load_csv(path)
