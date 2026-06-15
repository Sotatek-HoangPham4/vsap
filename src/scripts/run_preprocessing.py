import logging
import time

import pandas as pd

from preprocessing.cleaner import clean_text


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    force=True,
)


def load_stopwords():

    logging.info("Loading stopwords...")

    with open(
        "src/stopwords.txt",
        encoding="utf-8",
    ) as f:

        stopwords = {
            line.strip()
            for line in f
            if line.strip()
        }

    logging.info(
        "Loaded %s stopwords",
        len(stopwords),
    )

    return stopwords


def remove_stopwords(
    text: str,
    stopwords: set[str],
) -> str:

    return " ".join(
        word
        for word in text.split()
        if word not in stopwords
    )


def main():

    start_time = time.time()

    stopwords = load_stopwords()

    logging.info("Loading dataset...")

    df = pd.read_csv(
        "data/interim/labeled_reviews.csv"
    )

    logging.info(
        "Dataset loaded: %s rows",
        len(df),
    )

    logging.info("Cleaning text...")

    df["clean_text"] = (
        df["text"]
        .fillna("")
        .apply(clean_text)
    )

    logging.info("Removing stopwords...")

    df["clean_text"] = (
        df["clean_text"]
        .apply(
            lambda text: remove_stopwords(
                text,
                stopwords,
            )
        )
    )

    output_path = (
        "data/processed/reviews_processed.csv"
    )

    logging.info(
        "Saving processed dataset..."
    )

    df.to_csv(
        output_path,
        index=False,
    )

    elapsed = round(
        time.time() - start_time,
        2,
    )

    logging.info(
        "Done. Saved to %s",
        output_path,
    )

    logging.info(
        "Total rows: %s",
        len(df),
    )

    logging.info(
        "Execution time: %s seconds",
        elapsed,
    )


if __name__ == "__main__":
    main()