-- Run individual statements against data/processed/electronics_market.duckdb.
-- Currency is always grouped or filtered because the source contains USD and CAD.

-- Overall data coverage and price profile.
SELECT
    currency,
    COUNT(*) AS price_observations,
    COUNT(DISTINCT product_id) AS products_observed,
    COUNT(DISTINCT merchant_key) AS merchants_observed,
    ROUND(AVG(price_midpoint), 2) AS average_observed_price,
    ROUND(MEDIAN(price_midpoint), 2) AS median_observed_price,
    ROUND(100 * AVG(CASE WHEN is_sale THEN 1.0 ELSE 0.0 END), 2) AS sale_rate_pct
FROM price_observations
GROUP BY currency
ORDER BY currency;

-- Merchant coverage. Observation count is not sales volume.
SELECT
    currency,
    merchant,
    COUNT(*) AS price_observations,
    COUNT(DISTINCT product_id) AS products_observed,
    ROUND(MEDIAN(price_midpoint), 2) AS median_observed_price,
    ROUND(100 * AVG(CASE WHEN is_sale THEN 1.0 ELSE 0.0 END), 2) AS sale_rate_pct
FROM price_observations
GROUP BY currency, merchant
ORDER BY price_observations DESC;

-- Monthly trend from the generated view.
SELECT *
FROM monthly_price_summary
WHERE currency = 'USD'
ORDER BY year_month, merchant;

-- Products with a latest cross-merchant price spread.
SELECT
    p.product_id,
    p.product_name,
    p.brand,
    l.currency,
    COUNT(DISTINCT l.merchant_key) AS merchants,
    ROUND(MIN(l.price_midpoint), 2) AS lowest_latest_price,
    ROUND(MAX(l.price_midpoint), 2) AS highest_latest_price,
    ROUND(MAX(l.price_midpoint) - MIN(l.price_midpoint), 2) AS merchant_price_spread
FROM latest_product_prices AS l
JOIN products AS p USING (product_id)
GROUP BY p.product_id, p.product_name, p.brand, l.currency
HAVING COUNT(DISTINCT l.merchant_key) >= 2
ORDER BY merchant_price_spread DESC;

-- Availability profile. Unknown/special order is not forced into true or false.
SELECT
    availability_status,
    COUNT(*) AS observations,
    ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS share_pct
FROM price_observations
GROUP BY availability_status
ORDER BY observations DESC;
