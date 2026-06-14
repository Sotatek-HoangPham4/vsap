from app.repositories.category_repository import (
    CategoryRepository,
)


class CategoryService:

    @staticmethod
    async def save_tree(
        session,
        node: dict,
        root_id: int,
        parent_id: int | None,
    ):

        payload = {
            "id": node["id"],
            "parent_id": parent_id,
            "root_category_id": root_id,
            "name": node.get("name"),
            "url_key": node.get("url_key"),
            "full_url_key": node.get("full_url_key"),
            "level": node.get("level"),
            "product_count": node.get("product_count"),
            "is_leaf": node.get("is_leaf"),
        }

        await CategoryRepository.upsert(
            session,
            payload,
        )

        children = node.get("children", [])

        for child in children:

            await CategoryService.save_tree(
                session=session,
                node=child,
                root_id=root_id,
                parent_id=node["id"],
            )