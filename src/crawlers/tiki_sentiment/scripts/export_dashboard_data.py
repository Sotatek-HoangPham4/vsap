from pathlib import Path
import sys
import asyncio
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core.database import AsyncSessionLocal
from app.repositories.review_repository import ReviewRepository


OUTPUT_PATH = Path("data/interim/dashboard_data.csv")


async def export():

    async with AsyncSessionLocal() as session:
        rows = await ReviewRepository.get_dashboard_data(session)

    print(f"Fetched {len(rows)} rows from DB")

    data = [
        {
            "review_id": r["id"],
            "product_id": r["product_id"],
            "product_name": r["product_name"],
            "category": r["category"],
            "rating": r["rating"],
            "text": " ".join(filter(None, [r["title"], r["content"]])),
            "sentiment": r["sentiment"],
            "created_time": r["review_created_time"],
        }
        for r in rows
    ]

    df = pd.DataFrame(data)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print(f"Exported -> {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(export())