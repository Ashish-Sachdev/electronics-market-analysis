import pandas as pd

from electronics_market.transform.generic import clean_generic


def test_clean_generic_standardizes_structure_and_types():
    df = pd.DataFrame(
        {
            "Customer ID": [" C001 ", "C001"],
            "Sale Amount": ["$12.50", "$12.50"],
            "Signup.Date": ["2026-01-02", "2026-01-02"],
            "Active": ["Yes", "yes"],
            "Empty": ["N/A", ""],
        }
    )

    result, stats = clean_generic(df)

    assert result.columns.tolist() == [
        "customer_id",
        "sale_amount",
        "signup_date",
        "active",
    ]
    assert len(result) == 1
    assert result.loc[0, "customer_id"] == "C001"
    assert result.loc[0, "sale_amount"] == 12.5
    assert result.loc[0, "active"]
    assert str(result["signup_date"].dtype) == "datetime64[us, UTC]"
    assert stats.duplicate_rows_removed == 1
    assert stats.empty_columns_removed == ("empty",)


def test_clean_generic_does_not_turn_identifier_into_number():
    df = pd.DataFrame({"Account ID": ["001", "002"]})
    result, _ = clean_generic(df)
    assert result["account_id"].tolist() == ["001", "002"]
