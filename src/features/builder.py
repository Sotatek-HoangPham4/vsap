from scipy.sparse import hstack


class FeatureBuilder:

    def __init__(self, text_vectorizer, metadata_extractor):
        self.text_vectorizer = text_vectorizer
        self.metadata_extractor = metadata_extractor

    def fit(self, df):
        self.text_vectorizer.fit(df["text"])
        self.metadata_extractor.fit(df)
        return self

    def transform(self, df):

        X_text = self.text_vectorizer.transform(df["text"])
        X_meta = self.metadata_extractor.transform(df)

        return hstack([X_text, X_meta])

    def fit_transform(self, df):
        self.fit(df)
        return self.transform(df)