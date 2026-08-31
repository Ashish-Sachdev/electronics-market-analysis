# KPI Definitions

| KPI | Formula | Direction | Caveat |
|---|---|---|---|
| GMV | SUM(price) | Context dependent | Sales value, not profit |
| Units Sold | COUNT(valid order items) | Higher | Define cancelled-order treatment |
| Average Item Price | AVG(price) | Context dependent | Product mix affects it |
| Average Review Score | AVG(review_score) | Higher | Only reviewed orders |
| Late Delivery Rate | late delivered orders / eligible delivered orders | Lower | Missing delivery dates excluded |
| Low Review Rate | reviews <= 3 / reviewed orders | Lower | Missing reviews are not zero |

Each dashboard calculation must be reconciled against SQL or Python before presentation.