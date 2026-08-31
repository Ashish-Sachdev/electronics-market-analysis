# Electronics Market Analysis — 10-Day Project Plan

## Team and objective
Team size: 8. Duration: 10 days. Build an end-to-end analytics project for electronics-related Olist marketplace orders, combining data engineering, SQL, exploratory analysis, Power BI and machine learning.

## Business questions
1. Which electronics categories generate the most GMV and units sold?
2. How do sales and customer ratings change over time and across categories?
3. Which categories have the highest low-review and late-delivery rates?
4. What operational and order characteristics are associated with poor reviews?
5. Can historical order information estimate low-review risk?

## MVP KPIs
- GMV = sum(item price)
- Units Sold = count of valid order items
- Average Item Price = mean(item price)
- Average Review Score = mean(review score)
- Late Delivery Rate = late delivered orders / delivered orders
- Low Review Rate = reviews <= 3 / reviewed orders

## Machine learning
Target: `low_review = 1` when review score <= 3, otherwise 0. Start with a simple baseline, then Logistic Regression, then Random Forest. Use a time-aware train/test split where practical. Report precision, recall, F1, ROC-AUC and confusion matrix. Avoid leakage: features unavailable at prediction time must not be used.

## Dashboard
Page 1 — Sales & Market Overview: KPI cards, monthly GMV, category GMV, units by category, category/state/date filters.

Page 2 — Customer Experience & Prediction: low-review rate, late-delivery rate, review distribution, low reviews by category, delivery performance vs rating, and summarized ML performance/risk output.

## Team division
| Person | Primary responsibility | Main days |
|---|---|---|
| P1 | Project lead, definitions, integration | 1–2, 8–10 |
| P2 | Ingestion | 2–4 |
| P3 | Transformation | 2–5 |
| P4 | DuckDB and SQL | 4–6 |
| P5 | EDA and business insights | 4–6 |
| P6 | Power BI Page 1 | 5–8 |
| P7 | Power BI Page 2 | 5–9 |
| P8 | Machine learning and testing | 4–9 |

## Roadmap
| Day | Deliverable |
|---|---|
| 1 | Scope, definitions, categories, issues and ownership |
| 2 | Dataset inspection and join design |
| 3 | Ingestion and transformation V1 |
| 4 | Processed table, quality checks and DuckDB |
| 5 | EDA, KPI validation and ML feature design |
| 6 | Power BI V1 and Logistic Regression |
| 7 | Random Forest and dashboard completion |
| 8 | Integration and documentation |
| 9 | Testing, source validation and corrections only |
| 10 | README, final insights and presentation rehearsal |

## Definition of done
The pipeline reruns from documented inputs; processed data follows the data dictionary; quality checks and tests pass; important values are manually compared with source data; dashboard filters/calculations work; missing values are not displayed as zero; ML is compared with a baseline; limitations are visible; setup instructions work; every teammate can explain their contribution; and no credentials/private or unnecessary generated files are committed.