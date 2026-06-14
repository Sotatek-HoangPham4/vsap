from sklearn.metrics import classification_report, accuracy_score

def evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)

    report = classification_report(
        y_test,
        y_pred,
        output_dict=True
    )

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "macro_f1": report["macro avg"]["f1-score"],
        "report": report,
        "y_pred": y_pred
    }