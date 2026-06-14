import logging
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("train_pipeline")

from sklearn.model_selection import train_test_split

from src.data.loader import load_labeled_reviews
from src.data.preprocess import DataPreprocessor

from src.features.tfidf import TFIDFVectorizerWrapper
from src.features.metadata import MetadataFeatureExtractor
from src.features.builder import FeatureBuilder

from src.models.train import train_model
from src.models.evaluate import evaluate

def print_classification_report(report: dict, logger=None):
    lines = []
    lines.append("\n=== CLASSIFICATION REPORT ===\n")
    lines.append(f"{'class':<10} {'precision':<10} {'recall':<10} {'f1':<10} {'support':<10}")

    for label in ["negative", "neutral", "positive"]:
        r = report[label]
        lines.append(
            f"{label:<10} "
            f"{r['precision']:<10.2f} "
            f"{r['recall']:<10.2f} "
            f"{r['f1-score']:<10.2f} "
            f"{int(r['support']):<10}"
        )

    lines.append("\n--- summary ---")
    lines.append(f"macro avg F1: {report['macro avg']['f1-score']:.4f}")
    lines.append(f"weighted avg F1: {report['weighted avg']['f1-score']:.4f}")

    output = "\n".join(lines)

    if logger:
        logger.info(output)
    else:
        print(output)


async def main():

    logger.info("🚀 Starting training pipeline")

    # 1. Load data
    logger.info("📥 Loading labeled reviews from database...")
    df = await load_labeled_reviews()
    logger.info(f"✅ Loaded data shape: {df.shape}")

    # 2. Preprocess
    logger.info("🧹 Preprocessing data...")
    df = DataPreprocessor().transform(df)
    logger.info(f"✅ After preprocessing: {df.shape}")

    logger.info(f"Label distribution:\n{df['label'].value_counts()}")

    X_df = df
    y = df["label"]

    # 3. Feature engineering
    logger.info("⚙️ Building features (TF-IDF + metadata)...")
    builder = FeatureBuilder(
        TFIDFVectorizerWrapper(),
        MetadataFeatureExtractor()
    )

    X = builder.fit_transform(X_df)
    logger.info(f"✅ Feature matrix shape: {X.shape}")

    # 4. Train/test split
    logger.info("✂️ Splitting train/test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    logger.info(f"Train size: {X_train.shape}, Test size: {X_test.shape}")

    # 5. Train model
    logger.info("🤖 Training model (Logistic Regression)...")
    model = train_model(X_train, y_train, model_name="lr")
    logger.info("✅ Model training completed")

    # 6. Evaluate
    logger.info("📊 Evaluating model...")
    
    metrics = evaluate(model, X_test, y_test)

    logger.info(
        f"🎯 Accuracy: {metrics['accuracy']:.4f} | Macro F1: {metrics['macro_f1']:.4f}"
    )

    logger.info("📊 Classification Report:")
    
    print_classification_report(metrics["report"], logger)

    logger.info(
        f"🎯 Accuracy: {metrics['accuracy']:.4f} | "
        f"Macro F1: {metrics['macro_f1']:.4f}"
    )

    logger.info("🎉 Pipeline finished successfully")


if __name__ == "__main__":
    asyncio.run(main())