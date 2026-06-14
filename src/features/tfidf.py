from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDFVectorizerWrapper:
    def __init__(self, max_features=5000):
        self.vectorizer = TfidfVectorizer(
            min_df=1,
            max_df=0.95,
            max_features=50000,
            ngram_range=(1,2),
            stop_words=None  # đặc biệt cho tiếng Việt
        )

    def fit(self, texts):
        self.vectorizer.fit(texts)
        return self

    def transform(self, texts):
        return self.vectorizer.transform(texts)

    def fit_transform(self, texts):
        return self.vectorizer.fit_transform(texts)