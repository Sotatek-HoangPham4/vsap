# repositories/sentiment_label_repository.py

from sqlalchemy.dialects.postgresql import insert

from app.models.sentiment_label import (
    SentimentLabel,
)


class SentimentLabelRepository:

    @staticmethod
    async def upsert(
        session,
        review_id: int,
        sentiment: str,
    ):
        stmt = (
            insert(SentimentLabel)
            .values(
                review_id=review_id,
                sentiment=sentiment,
            )
            .on_conflict_do_update(
                index_elements=["review_id"],
                set_={
                    "sentiment": sentiment,
                },
            )
        )

        await session.execute(stmt)