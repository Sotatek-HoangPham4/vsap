# src/explainability/inference.py

def explain_review(text, model, shap_explainer):

    probs = model.predict_proba([text])[0]

    pred_class = probs.argmax()
    confidence = probs.max()

    explanation = shap_explainer.explain(text)

    return {
        "text": text,
        "prediction": int(pred_class),
        "confidence": float(confidence),
        "shap": explanation
    }