"""Run raw -> interim -> processed -> quality -> DuckDB."""

import argparse
import json
from pathlib import Path

from electronics_market.ingest.load import discover_input
from electronics_market.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean a tabular dataset and load the processed result into DuckDB."
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="CSV, TSV, JSON, JSONL, XLSX or XLS input (default: only data file in data/raw)",
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "electronics", "generic"],
        default="auto",
        help="Auto-detect the electronics schema or force a pipeline mode",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=ROOT / "data" / "processed" / "electronics_market.duckdb",
        help="DuckDB output path",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "reports" / "data_quality_report.json",
        help="JSON quality report path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.input or discover_input(ROOT / "data" / "raw")
    if not source.is_absolute():
        source = ROOT / source
    report = run_pipeline(
        source,
        project_root=ROOT,
        interim_directory=ROOT / "data" / "interim",
        processed_directory=ROOT / "data" / "processed",
        database_path=args.database,
        report_path=args.report,
        mode=args.mode,
    )
    summary = {
        "pipeline_mode": report["pipeline_mode"],
        "quality_passed": report["quality"]["passed"],
        "outputs": report["outputs"],
        "duckdb": report["duckdb"],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
