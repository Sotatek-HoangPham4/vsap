import pandas as pd

class AnalyticsAggregator:

    def __init__(self, df):
        self.df = df.copy()

    def total_reviews(self):
        return len(self.df)

    def positive_ratio(self):
        return (self.df["label"] == "positive").mean()

    def negative_ratio(self):
        return (self.df["label"] == "negative").mean()

    def sentiment_trend(self):
        return (
            self.df
            .groupby("review_created_time")["label"]
            .value_counts()
            .unstack()
            .fillna(0)
        )