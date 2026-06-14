from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

def get_models():
    return {
        "nb": MultinomialNB(),
        "lr": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "svm": LinearSVC(),
        "rf": RandomForestClassifier(n_estimators=200, random_state=42),
    }