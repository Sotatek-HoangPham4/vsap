from app.core.logger import logger

from app.core.database import (
    AsyncSessionLocal,
)

from app.clients.tiki_client import (
    TikiClient,
)

from app.services.product_service import (
    ProductService,
)

from app.repositories.category_repository import (
    CategoryRepository,
)

from app.workers.product_worker import (
    ProductWorker,
)


class ProductCrawler:

    async def run(self):

        client = TikiClient()

        await client.start()

        try:

            async with AsyncSessionLocal() as session:

                category_ids = (
                    await CategoryRepository
                    .get_leaf_categories(
                        session
                    )
                )

                # category_ids = [320]

                worker = ProductWorker(
                    client
                )

                for category_id in category_ids:

                    logger.info(
                        f"Crawling category {category_id}"
                    )

                    page = 1

                    while True:

                        data = await worker.fetch(
                            category_id,
                            page,
                        )

                        products = data.get(
                            "data",
                            [],
                        )

                        if not products:
                            break

                        for item in products:

                            await ProductService.save_product(
                                session=session,
                                category_id=category_id,
                                item=item,
                            )

                        await session.commit()

                        logger.info(
                            f"Category={category_id}"
                            f" Page={page}"
                            f" Products={len(products)}"
                        )

                        page += 1

        finally:

            await client.close()