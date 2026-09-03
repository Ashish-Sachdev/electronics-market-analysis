# Raw data

`ElectronicsProductsPricingData.csv` is the current source file. The pipeline reads it but never
edits it in place.

Raw and generated data paths are ignored for future additions because large datasets and build
outputs normally should not be versioned. A file already committed to Git remains tracked even
after a matching `.gitignore` rule is added.

To process a different tabular file, place it here and pass its path explicitly:

```bash
python scripts/run_pipeline.py --input data/raw/another_file.csv --mode generic
```
