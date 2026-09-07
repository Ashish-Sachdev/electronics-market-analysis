# Price Prediction — Model Results

Fill this page only after `scripts/train_price_model.py` has been run against the team's final cleaned dataset.

## Experiment
- Target: `price`
- Split: chronological 80% train / 20% test using `date_seen`
- Leakage exclusions: `price`, `prices.amountMin`, `prices.amountMax`, product `id`, full product `name`
- Features used: document the exact final list here

## Results

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Median baseline | TODO | TODO | TODO |
| Linear Regression | TODO | TODO | TODO |
| Random Forest Regressor | TODO | TODO | TODO |

## Interpretation
- Best model: TODO
- Improvement over baseline: TODO
- Typical absolute prediction error: TODO
- Largest failure cases: TODO
- Important features: TODO

## Limitations
- Historical listing data does not guarantee future market prices.
- Repeated observations of the same product may affect performance.
- The source captures observed merchants/listings, not the entire electronics market.
- A model should not be treated as evidence of causation.