"""Create simple analytical fields used by the MVP."""

import pandas as pd


def prepare_orders(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    if {"actual_delivery_days", "estimated_delivery_days"}.issubset(result.columns):
        result["late_delivery"] = (
            result["actual_delivery_days"] > result["estimated_delivery_days"]
        ).astype("int8")
    if "review_score" in result.columns:
        result["low_review"] = result["review_score"].le(3).astype("int8")
    return result
