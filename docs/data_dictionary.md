# Data Dictionary

The processed analytical table should document at least these fields:

| Field | Meaning |
|---|---|
| order_id | Unique order identifier |
| product_id | Product identifier |
| category | Standardized electronics category |
| price | Item selling price |
| freight_value | Freight charged for the item |
| purchase_timestamp | Order purchase time |
| estimated_delivery_date | Promised delivery date |
| delivered_customer_date | Actual delivery date |
| customer_state | Customer state |
| review_score | Customer rating when available |
| late_delivery | 1 when actual delivery is after estimated delivery |
| low_review | 1 when review score is 3 or lower |

Missing review or delivery values remain missing unless a documented business rule applies.