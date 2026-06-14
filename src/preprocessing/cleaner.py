import re

from underthesea import word_tokenize


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(r"http\S+", " ", text)

    text = re.sub(r"<.*?>", " ", text)

    text = re.sub(
        r"[^\w\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễ"
        r"ìíịỉĩòóọỏõôồốộổỗơờớợởỡ"
        r"ùúụủũưừứựửữỳýỵỷỹđ]",
        " ",
        text,
    )

    text = re.sub(r"\s+", " ", text)

    text = word_tokenize(
        text.strip(),
        format="text",
    )

    return text