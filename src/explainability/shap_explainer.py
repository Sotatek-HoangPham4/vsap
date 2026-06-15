# src/explainability/shap_explainer.py

import shap
import numpy as np

class SHAPExplainer:

    def __init__(self, model_wrapper):
        self.model = model_wrapper

        self.explainer = shap.Explainer(
            self.model.predict_proba,
            masker=shap.maskers.Text()
        )

    def explain(self, text):
        shap_values = self.explainer([text])

        return shap_values