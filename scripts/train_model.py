"""Explain why modelling is deferred for the current source dataset."""


def main() -> None:
    print(
        "No model was trained. ElectronicsProductsPricingData.csv has no valid supervised "
        "target such as sales, reviews, demand, or outcomes. Add a labeled dataset and a "
        "documented prediction question before enabling modelling."
    )


if __name__ == "__main__":
    main()
