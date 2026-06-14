import pandas as pd

def load_data(path="data/processed/reviews_processed.csv"):
    df = pd.read_csv(path)

    df = df.dropna(subset=["clean_text"])
    return df