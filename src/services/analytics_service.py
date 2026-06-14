import pandas as pd

class AnalyticsService:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # =====================
    # OVERVIEW METRICS
    # =====================
    def total_reviews(self):
        return len(self.df)

    def sentiment_ratio(self):
        return self.df["label"].value_counts(normalize=True)

    # =====================
    # CATEGORY ANALYTICS
    # =====================
    def by_category(self):
        return self.df.groupby(["category", "label"]).size().unstack().fillna(0)

    # =====================
    # SELLER ANALYTICS
    # =====================
    def by_seller(self):
        return self.df.groupby(["seller_id", "label"]).size().unstack().fillna(0)

    # =====================
    # TIME SERIES
    # =====================
    def sentiment_trend(self):
        df = self.df.copy()
        df["date"] = pd.to_datetime(df["review_created_time"], errors="coerce").dt.date

        return df.groupby(["date", "label"]).size().unstack().fillna(0)

    # =====================
    # TOP ISSUES
    # =====================
    def top_issues(self):
        keywords = ["delivery", "packaging", "quality", "price"]

        results = {}
        for k in keywords:
            results[k] = self.df["text"].str.contains(k, case=False, na=False).sum()

        return pd.Series(results)