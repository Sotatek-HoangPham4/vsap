import aiohttp
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
)


class TikiClient:

    def __init__(self):
        self.session = None

    async def start(self):

        timeout = aiohttp.ClientTimeout(
            total=60
        )

        self.session = aiohttp.ClientSession(
            timeout=timeout,
            headers={
                "User-Agent":
                    "Mozilla/5.0"
            },
        )

    async def close(self):

        if self.session:
            await self.session.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
    )
    async def get(
        self,
        url,
        params=None,
    ):

        async with self.session.get(
            url,
            params=params,
        ) as response:

            response.raise_for_status()

            return await response.json()