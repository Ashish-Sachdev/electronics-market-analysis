# Data Source

## Current source

`data/raw/ElectronicsProductsPricingData.csv` is a historical electronics product-pricing export.
It contains product metadata and repeated merchant price observations dated from 2014 through 2018.

The quality report records the exact SHA-256 hash used for a run so results can be tied to the
source version.

## Limitations

- The file is not the Brazilian Olist order dataset assumed by the original starter plan.
- It has no orders, quantities, customers, review scores, costs, profit or delivery information.
- A price observation is evidence that a price was seen, not evidence that a product sold.
- Merchant and category coverage is not guaranteed to represent the entire electronics market.
- USD and CAD observations must not be aggregated together without currency conversion.

Do not describe price totals as revenue or GMV, and do not infer sales volume from observation
counts.
