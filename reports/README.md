# Verified Data-Cleaning Results

These results were produced from the source SHA-256 recorded in
`data_quality_report.json`.

## Pipeline result

| Measure | Result |
|---|---:|
| Raw source rows | 7,249 |
| Structurally valid offer rows | 7,204 |
| Quarantined shifted rows | 45 (0.62%) |
| Observation rows before deduplication | 22,167 |
| Duplicate observations removed | 28 |
| Final price observations | 22,139 |
| Unique products | 832 |
| Product/category relationships | 11,659 |
| Normalized merchants | 668 |
| Quality checks | Passed |

Observation dates range from 2014-08-30 to 2018-07-25. The processed fact contains 22,138 USD
observations and one CAD observation. USD price midpoint ranges from $1.00 to $6,498.99, with a
median of $199.95. Sale-flagged observations account for 18.17% of the final fact.

The largest observation counts are Best Buy (10,869), B&H Photo Video (6,081) and Walmart (1,273).
These counts measure how often the source recorded prices, not transactions or market share.

## Missing-data interpretation

Shipping cost is missing for 99.47% of final observations because it is populated only when the
source explicitly gives a numeric `USD` amount. `shipping_is_free` and `is_available` also remain
missing when the source text does not establish a true/false answer. Missing values were not
replaced with zero.

See `processed_preview.csv` for 25 analysis-ready rows. Full generated CSV and DuckDB files remain
in `data/processed/` locally and are excluded from Git by design.
