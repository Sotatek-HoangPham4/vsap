VIETNAMESE_DICT = {
    "ko": "không",
    "hok": "không",
    "k": "không",
    "dc": "được",
    "sp": "sản phẩm",
    "ship": "giao hàng"
}

import re

class TextNormalizer:

    def __init__(self):
        self.mapping = VIETNAMESE_DICT

    def normalize(self, text):

        words = text.split()

        words = [
            self.mapping.get(word, word)
            for word in words
        ]

        text = " ".join(words)

        return text