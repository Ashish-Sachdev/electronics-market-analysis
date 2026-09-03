import pandas as pd

from electronics_market.quality import validate_price_observations
from electronics_market.transform.products import transform_electronics_dataset


def _raw_row(**overrides):
    row = {
        "id": "p1",
        "prices.amountMax": 100.0,
        "prices.amountMin": 90.0,
        "prices.availability": "Yes",
        "prices.condition": "new",
        "prices.currency": "usd",
        "prices.dateSeen": "2018-01-02T00:00:00Z,2018-01-03T00:00:00Z",
        "prices.isSale": True,
        "prices.merchant": "Bestbuy.com",
        "prices.shipping": "FREE",
        "prices.sourceURLs": "https://example.com/offer",
        "asins": "A1",
        "brand": "ACME",
        "categories": "Electronics,Headphones",
        "dateAdded": "2017-01-01T00:00:00Z",
        "dateUpdated": "2018-01-04T00:00:00Z",
        "ean": "123",
        "manufacturer": "Acme Inc",
        "manufacturerNumber": "M1",
        "name": "Test Headphones",
        "primaryCategories": "Electronics",
        "upc": "456",
        "weight": "2 pounds",
        "Unnamed: 26": None,
    }
    row.update(overrides)
    return row


def test_electronics_transform_normalizes_and_quarantines():
    raw = pd.DataFrame(
        [
            _raw_row(),
            _raw_row(**{"prices.dateSeen": "2018-01-03T00:00:00Z"}),
            _raw_row(
                id="bad",
                primaryCategories="Apple CarPlay",
                **{"Unnamed: 26": "shifted"},
            ),
        ]
    )
    offers, rejected, products, categories, observations, stats = transform_electronics_dataset(raw)

    assert len(offers) == 2
    assert len(rejected) == 1
    assert rejected.loc[0, "rejection_reason"] == (
        "malformed_csv_alignment;unexpected_primary_category"
    )
    assert products["product_id"].tolist() == ["p1"]
    assert set(categories["category_key"]) == {"electronics", "headphones"}
    assert len(observations) == 2
    assert observations["merchant"].unique().tolist() == ["Best Buy"]
    assert observations["currency"].unique().tolist() == ["USD"]
    assert observations["availability_status"].unique().tolist() == ["in_stock"]
    assert observations["shipping_is_free"].all()
    assert stats.duplicate_observations_removed == 1
    assert validate_price_observations(observations) == []


def test_price_quality_rejects_invalid_range():
    raw = pd.DataFrame([_raw_row(**{"prices.amountMin": 110.0})])
    *_, observations, _ = transform_electronics_dataset(raw)
    assert "price_min is greater than price_max" in validate_price_observations(observations)
