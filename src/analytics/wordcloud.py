from wordcloud import WordCloud


def generate_wordcloud(
    texts,
    output_file,
):

    content = " ".join(texts)

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white",
    )

    wc.generate(content)

    wc.to_file(output_file)