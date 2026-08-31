-- Starter KPI view/query. Adapt the table name after the processed model is finalized.
SELECT
    SUM(price) AS gmv,
    COUNT(*) AS units_sold,
    AVG(price) AS average_item_price,
    AVG(review_score) AS average_review_score,
    AVG(CASE WHEN review_score <= 3 THEN 1.0 ELSE 0.0 END) AS low_review_rate
FROM electronics_orders;
