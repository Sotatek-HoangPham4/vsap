import matplotlib.pyplot as plt
import pandas as pd


def plot_class_distribution(df):
    counts = df["sentiment"].value_counts()

    plt.figure(figsize=(8, 5))
    counts.plot(kind="bar")

    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig(
        "reports/figures/class_distribution.png"
    )

    plt.close()