from sqlalchemy.dialects.postgresql import insert

from app.models.category import Category

from sqlalchemy import select

from app.models.category import Category


class CategoryRepository:

    @staticmethod
    async def upsert(
        session,
        payload: dict,
    ):

        stmt = insert(Category).values(
            **payload
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "parent_id": stmt.excluded.parent_id,
                "root_category_id": stmt.excluded.root_category_id,
                "name": stmt.excluded.name,
                "url_key": stmt.excluded.url_key,
                "full_url_key": stmt.excluded.full_url_key,
                "level": stmt.excluded.level,
                "product_count": stmt.excluded.product_count,
                "is_leaf": stmt.excluded.is_leaf,
            },
        )

        await session.execute(stmt)

    @staticmethod
    async def get_leaf_categories(
        session,
    ):

        result = await session.execute(
            select(Category.id)
            .where(
                Category.is_leaf.is_(True)
            )
        )

        return result.scalars().all()



