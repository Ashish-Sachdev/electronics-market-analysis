# KPI Definitions

| KPI | Formula | Caveat |
|---|---|---|
| Price observations | `COUNT(*)` from `price_observations` | Measures data coverage, not sales |
| Products observed | `COUNT(DISTINCT product_id)` | Only products present in this file |
| Merchant product coverage | Distinct products per merchant | Observation frequency differs by merchant |
| Median observed price | `MEDIAN(price_midpoint)` grouped by currency | Product mix affects comparisons |
| Sale-observation rate | Sale observations / all eligible observations | A sale flag is not a completed sale |
| Known in-stock rate | In-stock / (`in_stock` + `out_of_stock`) | Unknown/special-order values excluded |
| Product merchant spread | Highest latest merchant price - lowest latest merchant price | Compare only within one currency |

Never sum prices as revenue or GMV. Every price aggregation must group or filter by `currency`.
