# Data Dictionary

## `products`

Grain: one row per `product_id`.

| Field | Meaning |
|---|---|
| product_id | Source product identifier; primary key |
| product_name | Product name from the most recently updated valid offer |
| brand | Case-normalized brand spelling |
| manufacturer | Manufacturer when supplied |
| manufacturer_number | Source manufacturer/model number |
| primary_category | Source primary category |
| categories | Original comma-separated category hierarchy |
| asins / ean / upc | Product identifiers when supplied |
| weight_text | Original weight text |
| weight_kg | First stated weight converted to kilograms |
| date_added / date_updated | UTC source metadata timestamps |

## `product_categories`

Grain: one row per unique `product_id` + `category_key`.

| Field | Meaning |
|---|---|
| product_id | Product foreign key |
| category | Trimmed source category label |
| category_key | Lowercase snake_case grouping key |

## `price_observations`

Grain: one unique product + merchant + currency + price range + sale flag + observed timestamp.

| Field | Meaning |
|---|---|
| observation_id | Stable hash of the observation business key |
| offer_id | Traceable source-row identifier |
| product_id | Product foreign key |
| merchant / merchant_key | Display name and normalized grouping key |
| currency | Uppercase three-letter currency code |
| condition | `new`, `used`, `refurbished` or `other` |
| availability_status | `in_stock`, `out_of_stock`, `limited_or_special_order` or `unknown` |
| is_available | True/false only when stock status is explicit; otherwise missing |
| is_sale | Source sale flag |
| price_min / price_max | Source observed price range |
| price_midpoint | `(price_min + price_max) / 2` |
| price_spread | `price_max - price_min` |
| shipping_text | Original shipping description |
| shipping_cost | Explicit `USD n.nn` amount when present; otherwise missing |
| shipping_is_free | True/false only when the text states it; otherwise missing |
| date_seen | Individual UTC observation timestamp split from the source list |
| date_seen_date / year / month / year_month | Derived calendar fields |
| source_url | Offer source URL |
| source_row_number | Original CSV row number, including the header offset |

Missing means unknown or unavailable; it is never automatically converted to zero.
