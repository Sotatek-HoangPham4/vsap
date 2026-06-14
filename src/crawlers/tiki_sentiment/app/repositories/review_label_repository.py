from sqlalchemy.dialects.postgresql import insert

from app.models.review_label import ReviewLabel

from sqlalchemy import select

from app.models.review import Review


class ReviewLabelRepository:

    @staticmethod
    async def upsert(
        session,
        payload,
    ):
        stmt = insert(
            ReviewLabel
        ).values(
            **payload
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[
                ReviewLabel.review_id
            ],
            set_={
                "label": stmt.excluded.label,
                "label_source": stmt.excluded.label_source,
            },
        )

        await session.execute(stmt)

    @staticmethod
    async def get_batch(
        session,
        limit: int = 1000,
        # TODO: CHANGE LATER
    ):
        result = await session.execute(
            select(Review)
            .limit(limit)
        )

        return result.scalars().all()