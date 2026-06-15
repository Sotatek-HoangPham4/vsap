from src.explainability.model_wrapper import SentimentModelWrapper
from src.explainability.shap_explainer import SHAPExplainer

MODEL_PATH = "outputs/vinai_phobert-base"

def main():

    # 1. load model
    model = SentimentModelWrapper(MODEL_PATH)

    # 2. init SHAP
    explainer = SHAPExplainer(model)

    # 3. test sentence
    text = "Sách đẹp nhưng giao chậm"

    # 4. predict
    probs = model.predict_proba([text])[0]

    print("\n=== PREDICTION ===")
    print("Negative:", probs[0])
    print("Neutral :", probs[1])
    print("Positive:", probs[2])

    # 5. explain
    print("\n=== SHAP EXPLANATION ===")
    shap_values = explainer.explain(text)

    print(shap_values)

if __name__ == "__main__":
    main()