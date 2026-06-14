from app.core.logger import logger

from app.core.database import (
    AsyncSessionLocal,
)

from app.clients.tiki_client import (
    TikiClient,
)

from app.services.category_service import (
    CategoryService,
)

from app.workers.category_worker import (
    CategoryWorker,
)


class CategoryCrawler:

    ROOT_CATEGORIES = [8322, 1883, 1789, 2549, 1815, 1882, 1520, 8594, 931, 4384, 1975, 915, 17166, 1846, 1686, 4221, 1703, 1801, 27498, 44792, 8371, 6000, 11312, 976, 27616, 15078]

    async def run(self):

        client = TikiClient()
        await client.start()

        try:
            worker = CategoryWorker(client)

            async with AsyncSessionLocal() as session:

                total_count = 0

                for root_category in self.ROOT_CATEGORIES:

                    logger.info(
                        f"Crawling category {root_category}"
                    )

                    result = await worker.fetch(
                        root_category
                    )

                    data = result.get("data")

                    if not data:
                        logger.warning(
                            f"No data for category {root_category}"
                        )
                        continue

                    count = 0

                    for node in data:
                        await CategoryService.save_tree(
                            session=session,
                            node=node,
                            root_id=root_category,
                            parent_id=root_category,
                        )

                        count += 1

                    total_count += count

                    logger.info(
                        f"Saved {count} categories for root {root_category}"
                    )

                await session.commit()

                logger.info(
                    f"Total saved: {total_count}"
                )

        except Exception as ex:
            logger.exception(ex)

        finally:
            await client.close()