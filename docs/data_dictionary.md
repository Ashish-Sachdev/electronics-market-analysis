# Data Dictionary — Core Analysis Fields

| Field | Meaning |
|---|---|
| `id` | Source product/listing identifier; do not use as a normal price-model feature |
| `name` | Product name; useful for inspection, but too specific for the beginner model |
| `brand_clean` | Team-standardized brand name |
| `merchant_clean` | Team-standardized merchant/channel |
| `category_clean` | Team-standardized analytical category |
| `condition_clean` | Team-standardized condition such as new/used/refurbished where available |
| `availability_clean` | Team-standardized listing availability |
| `shipping_clean` | Cleaned source shipping description |
| `shipping_type` | Grouped shipping category used for analysis |
| `date_seen_clean` | Cleaned source observation date/time |
| `date_seen` | Datetime parsed by the notebook from `date_seen_clean` |
| `prices.isSale` | Original source sale indicator |
| `sale_flag` | Boolean sale indicator created by the notebook |
| `price` | Cleaned observed listing price used as the main analytical value and optional ML target |
| `prices.amountMin` | Original price-related source field; do not use to predict `price` if `price` was derived from it |
| `prices.amountMax` | Original price-related source field; do not use to predict `price` if `price` was derived from it |

## Observation grain
Treat each row as an **observed listing/price record**. The same product may appear more than once across merchants or observation dates. Row count is therefore not automatically product count or units sold.

The notebook includes additional raw/source columns such as categories, UPC/ASIN, URLs, weight and manufacturer number; consult the notebook/data for their exact source meanings before using them in business claims.