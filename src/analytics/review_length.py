import matplotlib.pyplot as plt


def plot_review_length(df):

    lengths = (
        df["clean_text"]
        .fillna("")
        .str.split()
        .apply(len)
    )

    plt.figure(figsize=(10, 5))

    plt.hist(
        lengths,
        bins=50,
    )

    plt.title("Review Length Distribution")
    plt.xlabel("Number of Words")
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        "reports/figures/review_length.png"
    )

    plt.close()