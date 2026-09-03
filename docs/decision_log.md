# Decision Log

| Decision | Reason |
|---|---|
| Use the uploaded electronics pricing file for the current pipeline | It is the only provided source and differs from Olist |
| Replace order/review KPIs with price-observation KPIs | The source has no orders, quantities, reviews or delivery fields |
| Quarantine 45 shifted rows | Their CSV fields are misaligned; silently using them would corrupt product attributes |
| Explode `prices.dateSeen` | A list of dates violates first normal form and hides the observation grain |
| Split products, categories and price observations | Removes repeated product data and creates clearer DuckDB relationships |
| Deduplicate on the documented observation key | Removes repeated sightings without treating distinct merchants/prices as duplicates |
| Keep missing values missing | Zero would falsely mean a known price, cost, weight or status |
| Keep currencies separate | One observation is CAD while the remainder are USD |
| Use DuckDB | It provides local SQL analytics with no database server |
| Defer review-risk modelling | The current source has no valid prediction target |
