import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


class MetadataFeatureExtractor:

    def __init__(self):
        self.scaler = StandardScaler()

    def fit(self, df):
        X = self._build(df)
        self.scaler.fit(X)
        return self

    def transform(self, df):
        X = self._build(df)
        return self.scaler.transform(X)

    def fit_transform(self, df):
        return self.fit(df).transform(df)

    def _build(self, df):

        df = df.copy()

        df["review_length"] = df["text"].fillna("").apply(len)

        df["thank_count"] = np.log1p(df["thank_count"])

        df["is_photo"] = df["is_photo"].astype(int)

        df["days_after_delivery"] = (
            pd.to_datetime(df["review_created_time"], errors="coerce")
            - pd.to_datetime(df["delivery_date"], errors="coerce")
        ).dt.days

        df["days_after_delivery"] = df["days_after_delivery"].fillna(0)

        return df[[
            "review_length",
            "thank_count",
            "is_photo",
            "days_after_delivery"
        ]].values