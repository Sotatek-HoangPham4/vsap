from app.repositories.review_repository import ReviewRepository
from datetime import datetime


class ReviewService:

    @staticmethod
    async def save_review(session, product_id: int, item: dict):

        timeline = item.get("timeline", {})

        review_created_date = timeline.get("review_created_date")
        delivery_date = timeline.get("delivery_date")

        def parse_dt(x):
            if not x:
                return None
            return datetime.strptime(x, "%Y-%m-%d %H:%M:%S")

        payload = {
            "id": item["id"],
            "product_id": product_id,

            # user info
            "customer_id": (item.get("created_by") or {}).get("id"),
            "seller_id": (item.get("seller") or {}).get("id"),

            # text
            "rating": item.get("rating", 0),
            "title": item.get("title"),
            "content": item.get("content"),

            # sentiment metadata
            "thank_count": item.get("thank_count", 0),

            # FIX IMPORTANT (rename field)
            "review_created_time": parse_dt(review_created_date),
            "delivery_date": parse_dt(delivery_date),

            # engagement / quality signals
            "is_photo": len(item.get("images") or []) > 0,
            "image_count": len(item.get("images") or []),
            "status": item.get("status"),

            "score": item.get("score"),
            "new_score": item.get("new_score"),

            "comment_count": item.get("comment_count") or len(item.get("comments") or []),

            # raw backup
            "raw_json": item,
        }

        await ReviewRepository.upsert(session, payload)