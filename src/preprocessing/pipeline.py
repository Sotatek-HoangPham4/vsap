import unicodedata

from .cleaner import clean_text
from .tokenizer import tokenize


def preprocess_text(text: str):

    text = text.lower()

    text = unicodedata.normalize(
        "NFC",
        text,
    )

    text = clean_text(text)

    text = tokenize(text)

    return text