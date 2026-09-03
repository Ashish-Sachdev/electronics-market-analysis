# Modelling Plan

Supervised machine learning is deferred for the current MVP.

`ElectronicsProductsPricingData.csv` contains observed inputs—products, merchants, prices, dates,
availability and sale flags—but no reliable future outcome or target. Training a model to "predict"
one of these fields without a defined business decision would produce a technically runnable but
misleading result.

A future model requires:

1. A clear prediction time and business decision.
2. A labeled outcome such as future demand, completed sales, churn or review score.
3. Features that were available at prediction time.
4. Time-aware validation and a simple baseline.
5. Metrics chosen for the cost of false positives and false negatives.

The retained components in `src/electronics_market/models/` are scaffolding only; they are not part
of the current pricing pipeline.
