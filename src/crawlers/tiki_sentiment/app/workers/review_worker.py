from app.clients.tiki_client import (
    TikiClient,
)


class ReviewWorker:

    URL = (
        "https://tiki.vn/api/v2/reviews"
    )

    def __init__(
        self,
        client: TikiClient,
    ):
        self.client = client

    async def fetch(
        self,
        product_id: int,
        page: int,
    ):

        return await self.client.get(
            self.URL,
            params={
                "product_id": product_id,
                "page": page,
                "limit": 20,
            },
        )