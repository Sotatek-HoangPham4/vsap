from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class TopicExtractor:

    def __init__(self, n_topics=5):
        self.vectorizer = CountVectorizer(max_df=0.95, min_df=5)
        self.model = LatentDirichletAllocation(n_components=n_topics)

    def fit_transform(self, texts):
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X)
        return self.model.transform(X)

    def get_topics(self, n_words=10):
        words = self.vectorizer.get_feature_names_out()

        topics = []
        for topic in self.model.components_:
            top_words = [words[i] for i in topic.argsort()[-n_words:]]
            topics.append(top_words)

        return topics