from pathlib import Path
import sys
import asyncio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import asyncio
from pathlib import Path

import pandas as pd

from app.core.database import (
    AsyncSessionLocal,
)

from app.repositories.review_repository import (
    ReviewRepository,
)


OUTPUT_FILE = (
    Path("data/interim")
    / "labeled_reviews.csv"
)


async def main():

    async with AsyncSessionLocal() as session:

        rows = await ReviewRepository.get_labeled_reviews(
            session=session,
        )

        print(f"Fetched {len(rows)} rows from DB")

    data = []

    for row in rows:

        text = " ".join(
            filter(
                None,
                [
                    row.title,
                    row.content,
                ],
            )
        ).strip()

        data.append(
            {
                "review_id": row.id,
                "rating": row.rating,
                "text": text,
                "sentiment": row.sentiment,
                "created_time": row.review_created_time,
            }
        )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.DataFrame(data)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    print(
        f"Exported {len(df)} reviews -> {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    asyncio.run(main())