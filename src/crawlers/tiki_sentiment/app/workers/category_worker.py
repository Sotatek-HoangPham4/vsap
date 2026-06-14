from app.clients.tiki_client import TikiClient


class CategoryWorker:

    URL = "https://tiki.vn/api/v2/categories"

    def __init__(
        self,
        client: TikiClient,
    ):
        self.client = client

    async def fetch(
        self,
        parent_id: int,
    ):

        return await self.client.get(
            self.URL,
            params={
                "include": "children",
                "parent_id": parent_id,
            },
        )