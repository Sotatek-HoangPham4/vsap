from app.repositories.review_label_repository import (
    ReviewLabelRepository,
)


class ReviewLabelService:

    @staticmethod
    async def create_label(
        session,
        review,
    ):

        if review.rating <= 2:
            label = "negative"

        elif review.rating == 3:
            label = "neutral"

        else:
            label = "positive"

        payload = {
            "review_id": review.id,
            "label": label,
            "label_source": "rating_rule",
        }

        await ReviewLabelRepository.upsert(
            session,
            payload,
        )