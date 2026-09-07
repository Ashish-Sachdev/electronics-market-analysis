# Notebooks

## Main notebook

`electronics_pricing_analysis.ipynb` is the main analysis for this project.

It currently:
- loads the team's cleaned electronics-pricing dataset
- checks the data structure and quality
- creates parsed `date_seen` and Boolean `sale_flag` fields
- analyses price patterns across brand, merchant, category, condition, discount/sale status and shipping
- checks outliers and correlations
- creates stakeholder-facing charts

The notebook currently loaded **7,235 rows and 35 columns** in its saved run.

## Making it work for every teammate

The saved notebook currently points to a personal Google Drive path:

```python
DATA_PATH = Path("/content/drive/MyDrive/project/electronics_pricing_clean.csv")
```

For a GitHub-first team workflow, put the agreed cleaned file at:

```text
data/processed/electronics_pricing_clean.csv
```

Then use a project-relative path instead of a personal Drive path. If Jupyter is launched from the project root:

```python
DATA_PATH = Path("data/processed/electronics_pricing_clean.csv")
```

If the notebook's working directory is `notebooks/`:

```python
DATA_PATH = Path("../data/processed/electronics_pricing_clean.csv")
```

## Team rule
Avoid having several people edit the same `.ipynb` file at the same time. Notebook merge conflicts are difficult to review. Use a branch, finish a coherent section, push it, and merge before another teammate changes the same cells.

The notebook is for analysis and communication. Reusable machine-learning code can live in `scripts/` so the same experiment can be rerun without copying cells.