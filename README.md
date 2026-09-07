# Electronics Pricing Analysis

A team portfolio project that studies how electronics prices vary by **brand, merchant, category, product condition, discount status, shipping type and time**. The main analysis lives in `notebooks/electronics_pricing_analysis.ipynb`.

## What the project actually does

The current notebook uses the team's cleaned dataset, `electronics_pricing_clean.csv`, and loads **7,235 rows and 35 columns**. It explores five business questions:

1. Does actual brand pricing match the intended market position?
2. Which brands and merchants depend most on discounts?
3. Where are the strongest channel-coverage opportunities and risks?
4. Which categories offer less noisy competitive space?
5. What value do used and refurbished products offer relative to new products?

## Current workflow

```text
Original electronics dataset
        ↓
Team cleaning (completed manually / collaboratively)
        ↓
electronics_pricing_clean.csv
        ↓
notebooks/electronics_pricing_analysis.ipynb
        ↓
EDA + charts + business findings
        ↓
reports/ + Power BI
        ↓
optional price-prediction model
```

**We are not using DuckDB or an automated Python cleaning pipeline in the current version of the project.** That earlier architecture was removed because it did not match the workflow the team actually chose.

## Important data note

The notebook currently reads the cleaned file from:

```python
/content/drive/MyDrive/project/electronics_pricing_clean.csv
```

The GitHub repository currently contains `data/raw/ElectronicsProductsPricingData.csv`, but it does **not yet contain `electronics_pricing_clean.csv`**. For the notebook to work for every teammate immediately after cloning, add the cleaned CSV to:

```text
data/processed/electronics_pricing_clean.csv
```

and change the notebook data path to:

```python
DATA_PATH = Path("../data/processed/electronics_pricing_clean.csv")
```

when Jupyter is launched from the `notebooks/` folder. If Jupyter is launched from the project root, use `data/processed/electronics_pricing_clean.csv` instead.

## Repository guide

- `data/raw/` — original source dataset.
- `data/processed/` — recommended home for the team's final cleaned CSV.
- `notebooks/` — main exploratory pricing analysis.
- `reports/` — written findings, model guide and exported figures.
- `dashboards/powerbi/` — Power BI plan aligned with the pricing analysis.
- `scripts/train_price_model.py` — optional beginner-friendly predictive model.
- `docs/` — methodology, KPI definitions, decisions and project documentation.

## Setup

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install the project tools:

```bash
python -m pip install -e ".[dev,notebook]"
```

Start Jupyter:

```bash
jupyter lab
```

Then open:

```text
notebooks/electronics_pricing_analysis.ipynb
```

## Predictive modelling

The natural first predictive problem for this dataset is **price prediction**. Because `price` is a number, this is a **regression** problem, not classification. Start with a simple baseline and compare it with a Random Forest model. See `reports/predictive_model_guide.md` and `scripts/train_price_model.py`.

Do not call this a current-market price forecast: the dataset is historical. The model estimates price patterns present in this dataset.