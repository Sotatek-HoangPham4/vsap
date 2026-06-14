LOGISTICS_KEYWORDS = {
    "giao", "ship", "shipper", "đóng_gói", "vận_chuyển", "nhanh", "chậm"
}

QUALITY_KEYWORDS = {
    "lỗi", "rách", "móp", "bẩn", "hỏng", "cũ", "xước", "bung"
}

PRICE_KEYWORDS = {
    "giá", "sale", "voucher", "rẻ", "đắt", "khuyến_mãi"
}

GENERAL_POSITIVE = {
    "đẹp", "tốt", "ok", "hài_lòng", "ổn"
}


def map_topic_to_business(words: list[str]) -> str:
    words_set = set(words)

    logistics_score = len(words_set & LOGISTICS_KEYWORDS)
    quality_score = len(words_set & QUALITY_KEYWORDS)
    price_score = len(words_set & PRICE_KEYWORDS)

    scores = {
        "LOGISTICS": logistics_score,
        "PRODUCT_QUALITY": quality_score,
        "PRICING": price_score,
    }

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "GENERAL"

    return best