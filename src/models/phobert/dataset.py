from datasets import Dataset
import pandas as pd


def load_data(path: str):
    df = pd.read_csv(path)

    df = df.dropna(subset=["text", "sentiment"])

    label_map = {
        "negative": 0,
        "neutral": 1,
        "positive": 2
    }

    df["label"] = df["sentiment"].map(label_map)

    return Dataset.from_pandas(df[["text", "label"]])