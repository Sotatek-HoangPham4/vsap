from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def train_lda(texts, n_topics=5):
    vectorizer = CountVectorizer(
        max_features=8000,
        min_df=5,
        max_df=0.8
    )

    X = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42
    )

    lda.fit(X)

    return lda, vectorizer, X

def get_topics(lda, vectorizer, n_words=10):

    words = vectorizer.get_feature_names_out()
    topics = []

    for idx, topic in enumerate(lda.components_):

        top_words = [
            words[i]
            for i in topic.argsort()[-n_words:]
        ]

        topics.append((idx, top_words))

    return topics

import numpy as np

def assign_topics(lda, X):
    topic_probs = lda.transform(X)
    return np.argmax(topic_probs, axis=1)