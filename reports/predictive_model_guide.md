# Beginner Guide — Predicting Electronics Prices

## 1. What is a model?
A machine-learning model is a mathematical rule that learns patterns from examples.

For this project, imagine giving the computer thousands of rows like:

```text
Brand = Samsung
Merchant = bestbuy.com
Category = TV & Home Theater
Condition = new
Sale = yes
Observed price = 499.99
```

During training, the model sees the real `price`. It learns relationships between the other columns and price. Later, you give it a row without the answer and it estimates the price.

## 2. What are Python scripts for?
A Python script is simply a saved recipe. Instead of manually repeating 20 notebook cells every time, one command can load the data, prepare features, train models, calculate metrics and save the results.

A **script is not the same thing as a predictive model**:
- Python script = instructions/automation
- predictive model = the mathematical pattern learned from data
- notebook = interactive place to explore, explain and visualize

Your team does not need an automated cleaning pipeline to use machine learning. A manually cleaned, documented CSV is perfectly usable as the model input.

## 3. What should we predict?
Recommended target:

```text
price
```

Because price is a continuous number such as `$79.99`, `$499.00` or `$1,299.00`, this is called a **regression** problem.

## 4. Which columns should we use?
Good starter features from the cleaned notebook data:
- `brand_clean`
- `merchant_clean`
- `category_clean`
- `condition_clean`
- `availability_clean`
- `shipping_type`
- `sale_flag`
- month/year derived from `date_seen`

Do **not** use these as normal predictors of `price`:
- `price` itself
- `prices.amountMin`
- `prices.amountMax`
- raw IDs such as `id`
- full product `name`

If `price` was calculated from `prices.amountMin` or `prices.amountMax`, using those columns would reveal the answer to the model. That is called **data leakage**.

## 5. Why use three models?
### Median baseline
This barely learns anything. It predicts the training-set median price for every row.

Why keep it? Because a complicated model is only useful if it beats a very simple guess.

### Linear Regression
This is the easiest real regression model to explain. It estimates how encoded features are associated with higher or lower prices.

It is useful as a simple benchmark, but electronics prices often have nonlinear relationships.

### Random Forest Regressor
A Random Forest builds many decision trees and averages them. It can learn relationships such as:

```text
IF category = laptop AND brand = premium brand AND condition = new
THEN expected price tends to be high
```

It handles nonlinear interactions better than basic Linear Regression.

## 6. Training and testing
Never evaluate a model on the same rows it learned from.

Preferred approach for this dataset:

```text
older date_seen observations  -> training set (~80%)
newer date_seen observations  -> test set (~20%)
```

This asks a more realistic question: *Can patterns from earlier observations estimate later listing prices?*

Because the same product may appear multiple times, do not include product `id` or full `name` as predictors. For a stronger future version, consider a grouped split by product as an additional robustness check.

## 7. Metrics
### MAE — Mean Absolute Error
If MAE = `$45`, predictions are off by about `$45` on average.

Lower is better and this is the easiest metric to explain.

### RMSE — Root Mean Squared Error
Like MAE, but large mistakes are punished more heavily.

Lower is better.

### R²
Measures how much variation in price the model explains.

- closer to `1` = stronger fit
- around `0` = roughly no better than a simple mean-type prediction
- negative = poor test performance

Do not judge the model using R² alone.

## 8. What does a good project result look like?
Create a table like:

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Median baseline | ... | ... | ... |
| Linear Regression | ... | ... | ... |
| Random Forest | ... | ... | ... |

Then answer:
1. Which model performed best on unseen data?
2. By how much did it beat the baseline?
3. Which features appear most useful?
4. Where does the model make its biggest errors?
5. Are expensive products much harder to predict?

## 9. Responsible claim
Say:

> "The model estimates historical observed listing prices from product and channel attributes in this dataset."

Do not say:

> "The model knows the correct market price of any electronic product."

The data is historical, sampled and may contain repeated observations.

## 10. Running the starter model
After placing the agreed cleaned CSV here:

```text
data/processed/electronics_pricing_clean.csv
```

run:

```bash
python scripts/train_price_model.py
```

The script prints the baseline, Linear Regression and Random Forest metrics. Copy verified results into `reports/model_results_template.md`.