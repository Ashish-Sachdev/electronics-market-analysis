# Methodology

## What the team actually did
1. Started with `data/raw/ElectronicsProductsPricingData.csv`.
2. A teammate cleaned and standardized the data collaboratively outside an automated pipeline.
3. The final analysis uses `electronics_pricing_clean.csv`.
4. `notebooks/electronics_pricing_analysis.ipynb` performs data inspection, type conversions needed for analysis, EDA, outlier/correlation checks and visualizations.
5. Findings are summarized in `reports/` and can be recreated in Power BI.
6. Price prediction is an optional extension, not part of the cleaning process.

## Why manual cleaning is acceptable
An automated pipeline is useful when data must be reprocessed repeatedly. It is not a requirement for a good student analytics project. A manually cleaned file is acceptable when the team documents what changed, keeps the original file, verifies the result and makes the final cleaned file available consistently.

## Notebook-created fields
The notebook parses `date_seen_clean` into `date_seen`, converts `price` to numeric and creates `sale_flag` from `prices.isSale`.

## Quality rules
- Keep the raw file unchanged.
- Missing values are not automatically zero.
- Check whether duplicate rows represent true duplicates or repeated product/merchant/date observations before deleting them.
- Use median as well as mean for price because price distributions can be skewed by expensive products.
- Clearly distinguish listing observations from completed sales.
- Do not use source-price fields as predictors when they were used to construct the target `price`.