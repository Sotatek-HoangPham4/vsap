import pandas as pd


class DataPreprocessor:

    def transform(self, df: pd.DataFrame):

        df = df.copy()

        # text clean
        df["text"] = df["text"].fillna("").str.lower()

        # numeric fill
        df["thank_count"] = df["thank_count"].fillna(0)
        df["seller_id"] = df["seller_id"].fillna(-1)
        df["is_photo"] = df["is_photo"].fillna(0)

        # drop empty text
        df = df[df["text"].str.len() > 0]

        return df