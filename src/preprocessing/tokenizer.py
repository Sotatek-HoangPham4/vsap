from underthesea import word_tokenize

def tokenize(text: str):
    return word_tokenize(
        text,
        format="text",
    )