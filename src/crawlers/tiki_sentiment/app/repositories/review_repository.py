from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.models.review import Review
from app.models.sentiment_label import SentimentLabel


class ReviewRepository:

    @staticmethod
    async def upsert(session, payload: dict):
        stmt = insert(Review).values(**payload)

        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                # core fields
                "product_id": stmt.excluded.product_id,
                "customer_id": stmt.excluded.customer_id,
                "seller_id": stmt.excluded.seller_id,

                "rating": stmt.excluded.rating,
                "title": stmt.excluded.title,
                "content": stmt.excluded.content,

                # metadata
                "thank_count": stmt.excluded.thank_count,
                "is_photo": stmt.excluded.is_photo,
                "image_count": stmt.excluded.image_count,

                "review_created_time": stmt.excluded.review_created_time,
                "delivery_date": stmt.excluded.delivery_date,

                "score": stmt.excluded.score,
                "new_score": stmt.excluded.new_score,

                "comment_count": stmt.excluded.comment_count,

                # raw
                "raw_json": stmt.excluded.raw_json,
            },
        )

        await session.execute(stmt)

    @staticmethod
    async def get_batch(session, limit: int = 1000, offset: int = 0):
        stmt = (
            select(Review)
            .limit(limit)
            .offset(offset)
        )

        result = await session.execute(stmt)
        return result.scalars().all()

    
    @staticmethod
    async def get_labeled_reviews(session, limit: int | None = None):
        stmt = (
            select(
                    Review.id,
                    Review.product_id,
                    Review.rating,
                    Review.title,
                    Review.content,
                    Review.review_created_time,
                    Review.delivery_date,  
                    Review.thank_count,
                    Review.is_photo,
                    Review.seller_id,
                    SentimentLabel.sentiment,
                )
            .join(
                SentimentLabel,
                SentimentLabel.review_id == Review.id,
            )
        )

        if limit:
            stmt = stmt.limit(limit)

        result = await session.execute(stmt)
        return result.all()