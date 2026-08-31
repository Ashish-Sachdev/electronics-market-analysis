"""Minimum useful data-quality checks for the processed analytics table."""

REQUIRED_COLUMNS = {
    "order_id",
    "product_id",
    "price",
    "review_score",
}


def validate_processed_data(df):
    """Return a list of human-readable quality failures."""
    failures = []
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        failures.append(f"Missing required columns: {sorted(missing)}")
        return failures

    if df["order_id"].isna().any():
        failures.append("order_id contains missing values")
    if (df["price"].dropna() < 0).any():
        failures.append("price contains negative values")
    valid_reviews = df["review_score"].dropna().between(1, 5)
    if not valid_reviews.all():
        failures.append("review_score contains values outside 1-5")

    return failures
