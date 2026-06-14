from app.repositories.product_repository import (
    ProductRepository,
)


class ProductService:

    @staticmethod
    async def save_product(
        session,
        category_id: int,
        item: dict,
    ):

        payload = {
            "id": item["id"],
            "category_id": category_id,
            "seller_id": item.get("seller_id"),
            "name": item.get("name"),
            "price": item.get("price"),
            "original_price": item.get("original_price"),
            "rating_average": item.get(
                "rating_average"
            ),
            "review_count": item.get(
                "review_count"
            ),
            "thumbnail_url": item.get(
                "thumbnail_url"
            ),
            "raw_json": item,
        }

        await ProductRepository.upsert(
            session,
            payload,
        )