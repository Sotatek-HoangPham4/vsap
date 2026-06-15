import logging
import time

import pandas as pd

from analytics.class_distribution import (
    plot_class_distribution,
)

from analytics.review_length import (
    plot_review_length,
)

from analytics.word_frequency import (
    top_words,
)

from analytics.wordcloud import (
    generate_wordcloud,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def main():

    start_time = time.time()

    logging.info(
        "Loading dataset..."
    )

    df = pd.read_csv(
        "data/processed/reviews_processed.csv"
    )

    logging.info(
        "Loaded %s reviews",
        len(df),
    )

    logging.info(
        "Generating class distribution chart..."
    )

    plot_class_distribution(df)

    logging.info(
        "Class distribution chart saved"
    )

    logging.info(
        "Generating review length chart..."
    )

    plot_review_length(df)

    logging.info(
        "Review length chart saved"
    )

    for sentiment in [
        "positive",
        "negative",
        "neutral",
    ]:

        logging.info(
            "Processing sentiment: %s",
            sentiment,
        )

        subset = df[
            df["sentiment"] == sentiment
        ]

        logging.info(
            "%s reviews found",
            len(subset),
        )

        texts = subset[
            "clean_text"
        ].fillna("")

        print(
            f"\n=== {sentiment.upper()} ==="
        )

        for word, count in top_words(texts):

            print(
                word,
                count,
            )

        output_file = (
            f"reports/figures/"
            f"{sentiment}_wordcloud.png"
        )

        logging.info(
            "Generating wordcloud: %s",
            output_file,
        )

        generate_wordcloud(
            texts.tolist(),
            output_file,
        )

        logging.info(
            "Saved wordcloud: %s",
            output_file,
        )

    elapsed = round(
        time.time() - start_time,
        2,
    )

    logging.info(
        "EDA completed successfully"
    )

    logging.info(
        "Execution time: %s seconds",
        elapsed,
    )


if __name__ == "__main__":
    main()