# Modelling Plan

## Business question
Can information available at prediction time identify orders at greater risk of receiving a customer review of 3 stars or lower?

## Target
`low_review = 1` when `review_score <= 3`; otherwise 0 for reviewed orders.

## Models
1. Majority-class or simple probability baseline.
2. Logistic Regression for an interpretable benchmark.
3. Random Forest as the main nonlinear comparison model.

## Candidate features
Price, freight value, product category, customer state, order timing and promised delivery window. Only use variables that would actually be known at the stated prediction time.

## Validation
Split chronologically: older observations for training and newer observations for testing. Never randomly mix future records into the training period for a time-dependent prediction claim.

## Metrics
ROC-AUC, precision, recall, F1 and confusion matrix. Pay special attention to recall for low-review orders.

## Interpretation
Predictions are risk probabilities, not guarantees. Avoid leakage from the review itself or future delivery outcomes when claiming purchase-time prediction.