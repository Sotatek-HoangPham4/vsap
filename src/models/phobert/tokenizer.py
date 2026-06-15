from transformers import AutoTokenizer


def get_tokenizer(model_name: str):
    return AutoTokenizer.from_pretrained(model_name, use_fast=False)