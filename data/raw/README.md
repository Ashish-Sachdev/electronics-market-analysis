# Raw data

`ElectronicsProductsPricingData.csv` is the original electronics pricing dataset used by this project.

## Rule
Treat this file as the source snapshot. Do not manually overwrite it after analysis begins. If cleaning decisions change, keep a separate cleaned copy so the team can always compare the result with the original.

## Current team workflow
The team has already cleaned the dataset collaboratively. The analysis notebook currently expects a cleaned file called:

```text
electronics_pricing_clean.csv
```

The recommended repository location for that final cleaned file is:

```text
data/processed/electronics_pricing_clean.csv
```

The original raw file and the cleaned file have different purposes:

- **raw** = what the project started with
- **processed/clean** = the version the team agreed to analyze

The current project does not use Olist and does not require multiple Olist tables.