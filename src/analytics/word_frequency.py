from collections import Counter


def top_words(
    texts,
    n=20,
):
    counter = Counter()

    for text in texts:

        words = text.split()

        counter.update(words)

    return counter.most_common(n)