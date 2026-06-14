import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
sys.path.append(str(ROOT))

# 👇 ADD THIS SHIM
CRAWLER_APP_PATH = ROOT / "crawlers" / "tiki_sentiment"
sys.path.append(str(CRAWLER_APP_PATH))

import asyncio
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight

from features.tfidf import TFIDFVectorizerWrapper
from features.metadata import MetadataFeatureExtractor
from features.builder import FeatureBuilder

from crawlers.tiki_sentiment.app.core.database import AsyncSessionLocal
from crawlers.tiki_sentiment.app.repositories.review_repository import ReviewRepository

async def load_data():
    async with AsyncSessionLocal() as session:
        rows = await ReviewRepository.get_labeled_reviews(session)

    data = []

    for r in rows:
        text = " ".join(filter(None, [r.title, r.content]))

        data.append({
            "text": text,
            "content": r.content or "",
            "title": r.title or "",

            "sentiment": r.sentiment,

            "thank_count": r.thank_count or 0,
            "is_photo": 1 if r.is_photo else 0,
            "seller_id": r.seller_id if r.seller_id is not None else -1,

            "review_created_time": r.review_created_time,
            "delivery_date": None,
        })

    return pd.DataFrame(data)

async def main():
    df = await load_data()

    print("NaN report:\n", df.isna().sum())

    # ===== CLEAN =====
    df = df.dropna(subset=["sentiment"])
    df["text"] = df["text"].fillna("")

    df = df[df["text"].str.len() > 0]

    # ===== SPLIT DATA =====
    X_df = df.copy()
    y = df["sentiment"]

    tfidf = TFIDFVectorizerWrapper()
    meta = MetadataFeatureExtractor()

    builder = FeatureBuilder(tfidf, meta)

    X = builder.fit_transform(X_df)

    # ===== TRAIN TEST SPLIT =====
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # ===== CLASS WEIGHTS (IMPORTANT FIX) =====
    classes = np.unique(y_train)

    weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=y_train
    )

    class_weight = dict(zip(classes, weights))

    # ===== MODEL =====
    model = LogisticRegression(
        max_iter=1000,
        class_weight=class_weight,
        solver="lbfgs"
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n=== CLASSIFICATION REPORT ===")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    asyncio.run(main())