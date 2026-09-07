# Predictive Modelling Plan — Price Regression

## Question
Can product and listing attributes estimate the observed `price` of electronics listings in this historical dataset?

## Target
`price`

Because the target is a number, this is a **regression** task.

## Starter models
1. `DummyRegressor(strategy="median")` — simple baseline
2. Linear Regression — simple benchmark
3. Random Forest Regressor — nonlinear comparison

## Candidate features
Use cleaned attributes that would be known without looking at the target price:
- `brand_clean`
- `merchant_clean`
- `category_clean`
- `condition_clean`
- `availability_clean`
- `shipping_type`
- `sale_flag`
- year/month derived from `date_seen`

## Leakage exclusions
Do not use:
- `price`
- `prices.amountMin`
- `prices.amountMax`
- product `id`
- full product `name`

The amountMin/amountMax fields must be excluded if the cleaned `price` was derived from them; otherwise the model would effectively be given the answer.

## Split
Prefer a chronological 80/20 split based on `date_seen`: older observations for training and newer observations for testing. For a stronger follow-up experiment, test a product-grouped split to reduce repeated-product leakage.

## Metrics
- MAE — easiest business interpretation; lower is better
- RMSE — penalizes large mistakes; lower is better
- R² — amount of price variation explained; higher is generally better, but interpret with MAE/RMSE

## Success rule
The Random Forest or Linear Regression should materially beat the median baseline on the unseen test set before it is presented as useful.

## Limitations
This model estimates patterns in historical observed listing prices. It is not an authoritative product valuation system and is not a guaranteed future-price forecast.

A runnable beginner implementation is in `scripts/train_price_model.py`.