import pandas as pd

from electronics_market.transform.orders import prepare_orders


def test_prepare_orders_creates_flags():
    df = pd.DataFrame(
        {
            "review_score": [5, 2],
            "estimated_delivery_days": [10, 7],
            "actual_delivery_days": [8, 11],
        }
    )
    result = prepare_orders(df)
    assert result["low_review"].tolist() == [0, 1]
    assert result["late_delivery"].tolist() == [0, 1]
