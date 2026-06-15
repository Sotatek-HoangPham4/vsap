from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from sklearn.model_selection import train_test_split

from src.models.phobert.dataset import load_data
from src.models.phobert.train import train_phobert

DATA_PATH = "data/interim/labeled_reviews.csv"


def run():
    dataset = load_data(DATA_PATH)

    train_test = dataset.train_test_split(test_size=0.2, seed=42)

    train_ds = train_test["train"]
    test_ds = train_test["test"]

    print("🔥 Training PhoBERT-base...")
    base_result = train_phobert(
        "vinai/phobert-base",
        train_ds,
        test_ds,
    )

    print("🔥 Training PhoBERT-large...")
    large_result = train_phobert(
        "vinai/phobert-large",
        train_ds,
        test_ds,
    )

    print("\n📊 FINAL RESULTS:")
    print("BASE:", base_result)
    print("LARGE:", large_result)


if __name__ == "__main__":
    run()