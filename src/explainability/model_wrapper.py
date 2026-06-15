# src/explainability/model_wrapper.py

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class SentimentModelWrapper:

    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.eval()

    def predict_proba(self, texts):
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=256
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)

        return probs.numpy()