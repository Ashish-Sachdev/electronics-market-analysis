import pandas as pd

from electronics_market.quality import validate_processed_data


def test_valid_data_passes():
    df = pd.DataFrame({
        "order_id": ["o1"],
        "product_id": ["p1"],
        "price": [100.0],
        "review_score": [5],
    })
    assert validate_processed_data(df) == []


def test_negative_price_fails():
    df = pd.DataFrame({
        "order_id": ["o1"],
        "product_id": ["p1"],
        "price": [-1.0],
        "review_score": [4],
    })
    assert "price contains negative values" in validate_processed_data(df)
