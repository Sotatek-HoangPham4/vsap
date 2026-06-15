from src.explainability.model_wrapper import SentimentModelWrapper
from src.explainability.lime_explainer import LIMEExplainer

MODEL_PATH = "outputs/vinai_phobert-base"

model = SentimentModelWrapper(MODEL_PATH)
lime = LIMEExplainer(model, ["neg", "neu", "pos"])

text = "Sách đẹp nhưng giao chậm"

exp = lime.explain(text)

exp.show_in_notebook()  # hoặc exp.as_list()