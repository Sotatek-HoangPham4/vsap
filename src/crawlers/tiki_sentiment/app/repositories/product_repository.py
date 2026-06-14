from sqlalchemy.dialects.postgresql import insert

from app.models.product import Product
from sqlalchemy import select, or_

from sqlalchemy import update
from datetime import datetime


class ProductRepository:

    @staticmethod
    async def upsert(
        session,
        payload: dict,
    ):

        stmt = insert(Product).values(
            **payload
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "category_id": stmt.excluded.category_id,
                "seller_id": stmt.excluded.seller_id,
                "name": stmt.excluded.name,
                "price": stmt.excluded.price,
                "original_price": stmt.excluded.original_price,
                "rating_average": stmt.excluded.rating_average,
                "review_count": stmt.excluded.review_count,
                "thumbnail_url": stmt.excluded.thumbnail_url,
                "raw_json": stmt.excluded.raw_json,
            },
        )

        await session.execute(stmt)



    @staticmethod
    async def get_products_need_reviews(
        session,
        limit: int = 1000,
    ):
        result = await session.execute(
            select(
                Product.id,
                Product.review_count,
            )
            .where(
                Product.review_count > 0,
                or_(
                    Product.review_crawled_count.is_(None),
                    Product.review_count >
                    Product.review_crawled_count,
                ),
            )
            .limit(limit)
        )

        return result.all()



    @staticmethod
    async def mark_review_crawled(
        session,
        product_id: int,
        review_count: int,
    ):
        await session.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(
                review_crawled_count=review_count,
                last_review_crawl_at=datetime.utcnow(),
            )
        )