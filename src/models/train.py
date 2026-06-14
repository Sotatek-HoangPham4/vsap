from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB


def train_model(X, y, model_name="lr"):

    if model_name == "lr":
        model = LogisticRegression(max_iter=1000, class_weight="balanced")

    elif model_name == "svm":
        model = LinearSVC()

    elif model_name == "nb":
        model = MultinomialNB()

    else:
        raise ValueError("Unknown model")

    model.fit(X, y)
    return model