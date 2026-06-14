import logging
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from preprocess import load_data
from lda_model import train_lda, get_topics, assign_topics
from topic_mapper import map_topic_to_business

# =========================
# OUTPUT DIR
# =========================
REPORT_DIR = Path("reports/topics")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# SAVE TOPICS TEXT
# =========================
def save_topics(topics, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        for tid, words in topics:
            f.write(f"Topic {tid}:\n")
            f.write(", ".join(words) + "\n\n")


# =========================
# SAVE TOPIC DISTRIBUTION
# =========================
def plot_topic_distribution(df, file_path):
    counts = df["topic"].value_counts().sort_index()

    plt.figure(figsize=(8, 4))
    plt.bar(counts.index.astype(str), counts.values)
    plt.title("Topic Distribution")
    plt.xlabel("Topic")
    plt.ylabel("Number of reviews")

    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()


# =========================
# SAVE TOP WORDS PER TOPIC
# =========================
def plot_topic_words(topics, file_path_prefix):
    for tid, words in topics:
        plt.figure(figsize=(8, 4))
        plt.bar(words, range(len(words)))
        plt.xticks(rotation=45)
        plt.title(f"Topic {tid} Top Words")

        plt.tight_layout()
        plt.savefig(f"{file_path_prefix}_topic_{tid}.png")
        plt.close()


# =========================
# MAIN
# =========================
def main():

    logging.basicConfig(level=logging.INFO)

    df = load_data()
    logging.info(f"Loaded {len(df)} reviews")

    texts = df["clean_text"].fillna("")

    # =====================
    # TRAIN LDA
    # =====================
    lda, vectorizer, X = train_lda(texts, n_topics=5)

    topics = get_topics(lda, vectorizer)

    business_mapping = []

    for tid, words in topics:
        label = map_topic_to_business(words)

        business_mapping.append({
            "topic_id": tid,
            "label": label,
            "keywords": words
        })

        print(f"\nTopic {tid} → {label}")
        print(", ".join(words))

    logging.info("Topics found:")

    # SAVE JSON BUSINESS INSIGHT
    import json 
    with open(REPORT_DIR / "business_topics.json", "w", encoding="utf-8") as f:
        json.dump(business_mapping, f, ensure_ascii=False, indent=2)

    # =====================
    # ASSIGN TOPIC
    # =====================
    df["topic"] = assign_topics(lda, X)

    # convert mapping dict
    topic_label_map = {
        x["topic_id"]: x["label"]
        for x in business_mapping
    }

    df["topic_label"] = df["topic"].map(topic_label_map)

    # =====================
    # SAVE DATASET
    # =====================
    output_csv = Path("data/interim/topics_labeled.csv")
    df.to_csv(
        "data/interim/topics_business_labeled.csv",
        index=False,
        encoding="utf-8-sig"
    )

    logging.info(f"Saved topic-labeled dataset -> {output_csv}")

    # =====================
    # SAVE REPORTS
    # =====================
    save_topics(topics, REPORT_DIR / "topics_lda.txt")

    plot_topic_distribution(df, REPORT_DIR / "topic_distribution.png")

    plot_topic_words(topics, REPORT_DIR / "topic_words")

    logging.info(f"Saved reports to {REPORT_DIR}")


if __name__ == "__main__":
    main()