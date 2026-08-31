# Decision Log

| Decision | Reason |
|---|---|
| Use Olist as the primary MVP dataset | Supports multi-table sales, product, delivery and review analysis |
| Limit MVP to electronics-related categories | Keeps a 10-day project achievable |
| Use GMV rather than profit/revenue claims | Product costs and full business expenses are unavailable |
| Use DuckDB | Lightweight SQL database suitable for local analytics |
| Build two Power BI pages | Prevents dashboard overcrowding |
| Predict low-review risk | Classification matches available review outcomes |
| Compare Logistic Regression and Random Forest | Provides interpretable baseline and nonlinear model |
| Use chronological ML validation | Avoids mixing future observations into past training data |