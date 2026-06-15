from pathlib import Path
import sys
import asyncio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# scripts/generate_labels.py

import asyncio

from app.core.database import (
    AsyncSessionLocal,
)

from app.repositories.review_repository import (
    ReviewRepository,
)

from app.repositories.sentiment_label_repository import (
    SentimentLabelRepository,
)


def rating_to_sentiment(
    rating: int,
) -> str:

    if rating <= 2:
        return "negative"

    if rating == 3:
        return "neutral"

    return "positive"


async def main():

    async with AsyncSessionLocal() as session:

        reviews = await ReviewRepository.get_batch(
            session=session
        )

        count = 0

        for review in reviews:

            sentiment = rating_to_sentiment(
                review.rating
            )

            await SentimentLabelRepository.upsert(
                session=session,
                review_id=review.id,
                sentiment=sentiment,
            )

            count += 1

        await session.commit()

        print(
            f"Generated {count} labels"
        )


if __name__ == "__main__":
    asyncio.run(main())