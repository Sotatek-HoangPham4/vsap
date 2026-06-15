# src/explainability/lime_explainer.py

from lime.lime_text import LimeTextExplainer

class LIMEExplainer:

    def __init__(self, model_wrapper, class_names):
        self.model = model_wrapper
        self.explainer = LimeTextExplainer(class_names=class_names)

    def explain(self, text):
        exp = self.explainer.explain_instance(
            text,
            self.model.predict_proba,
            num_features=10
        )
        return exp