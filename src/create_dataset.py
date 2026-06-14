import pandas as pd

df = pd.read_csv("data/raw/reviews.csv")

def rating_to_label(rating):
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    return "negative"

df["label"] = df["rating"].apply(rating_to_label)

df.to_csv(
    "data/interim/labeled_reviews.csv",
    index=False
)