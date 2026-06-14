import asyncio
import logging
import sys
from pathlib import Path

from scipy.sparse import hstack
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import pandas as pd

from src.data.loader import load_labeled_reviews
from src.data.preprocess import DataPreprocessor

from src.features.tfidf import TFIDFVectorizerWrapper
from src.features.metadata import MetadataFeatureExtractor

from src.models.registry import get_models
from src.models.evaluate import evaluate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("train_all_models")


async def main():

    logger.info("📥 Loading data...")
    df = await load_labeled_reviews()

    df = DataPreprocessor().transform(df)

    X = df
    y = df["label"]

    # =========================
    # SPLIT FIRST (IMPORTANT FIX)
    # =========================
    X_train_df, X_test_df, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # =========================
    # FEATURE ENGINEERING (FIT ONLY TRAIN)
    # =========================
    logger.info("⚙️ Building features...")

    tfidf = TFIDFVectorizerWrapper()
    meta = MetadataFeatureExtractor()

    # TEXT
    X_text_train = tfidf.fit_transform(X_train_df["text"])
    X_text_test = tfidf.transform(X_test_df["text"])

    # META
    X_meta_train = meta.fit_transform(X_train_df)
    X_meta_test = meta.transform(X_test_df)

    # COMBINE
    X_full_train = hstack([X_text_train, X_meta_train])
    X_full_test = hstack([X_text_test, X_meta_test])

    # TEXT ONLY (for NB)
    X_text_only_train = X_text_train
    X_text_only_test = X_text_test

    # =========================
    # MODELS
    # =========================
    models = get_models()

    results = []

    for name, model in models.items():

        logger.info(f"🤖 Training {name}...")

        # NB ONLY TEXT
        if name == "nb":
            model.fit(X_text_only_train, y_train)
            metrics = evaluate(model, X_text_only_test, y_test)

        # OTHERS FULL FEATURES
        else:
            model.fit(X_full_train, y_train)
            metrics = evaluate(model, X_full_test, y_test)

        results.append({
            "model": name,
            "accuracy": metrics["accuracy"],
            "macro_f1": metrics["macro_f1"]
        })

        logger.info(
            f"✅ {name} -> acc={metrics['accuracy']:.4f}, f1={metrics['macro_f1']:.4f}"
        )

    # =========================
    # SUMMARY
    # =========================
    df_result = pd.DataFrame(results)
    df_result = df_result.sort_values("macro_f1", ascending=False)

    logger.info("\n📊 MODEL COMPARISON RESULT:\n")
    logger.info(f"\n{df_result}")

    print(df_result)


if __name__ == "__main__":
    asyncio.run(main())