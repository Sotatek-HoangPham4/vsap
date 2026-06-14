from app.clients.tiki_client import (
    TikiClient,
)


class ProductWorker:

    URL = (
        "https://tiki.vn/api/"
        "personalish/v1/blocks/listings"
    )

    def __init__(
        self,
        client: TikiClient,
    ):
        self.client = client

    async def fetch(
        self,
        category_id: int,
        page: int,
    ):

        return await self.client.get(
            self.URL,
            params={
                "category": category_id,
                "page": page,
                "limit": 40,
            },
        )