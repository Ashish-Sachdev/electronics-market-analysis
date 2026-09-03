import duckdb
import pandas as pd

from electronics_market.pipeline import run_pipeline


def test_generic_pipeline_writes_csv_report_and_duckdb(tmp_path):
    raw_directory = tmp_path / "data" / "raw"
    raw_directory.mkdir(parents=True)
    source = raw_directory / "customers.csv"
    pd.DataFrame({"Customer ID": ["001", "002"], "Amount": ["$10", "$20"]}).to_csv(
        source, index=False
    )

    database = tmp_path / "data" / "processed" / "analytics.duckdb"
    report = run_pipeline(
        source,
        project_root=tmp_path,
        interim_directory=tmp_path / "data" / "interim",
        processed_directory=tmp_path / "data" / "processed",
        database_path=database,
        report_path=tmp_path / "reports" / "quality.json",
        mode="generic",
    )

    assert report["quality"]["passed"]
    assert (tmp_path / "data" / "interim" / "customers_cleaned.csv").exists()
    assert (tmp_path / "data" / "processed" / "customers_processed.csv").exists()
    with duckdb.connect(str(database), read_only=True) as connection:
        assert connection.execute("SELECT COUNT(*) FROM processed_data").fetchone()[0] == 2
