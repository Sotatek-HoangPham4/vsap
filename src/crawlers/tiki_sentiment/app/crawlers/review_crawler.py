from app.core.logger import logger

from app.core.database import (
    AsyncSessionLocal,
)

from app.clients.tiki_client import (
    TikiClient,
)

from app.repositories.product_repository import (
    ProductRepository,
)

from app.services.review_service import (
    ReviewService,
)

from app.workers.review_worker import (
    ReviewWorker,
)


class ReviewCrawler:

    async def run(self):

        client = TikiClient()

        await client.start()

        try:

            async with AsyncSessionLocal() as session:

                products = await ProductRepository.get_products_need_reviews(
                    session,
                    limit=1000,
                )

                worker = ReviewWorker(
                    client
                )

            for (
                product_id,
                review_count,
            ) in products:

                logger.info(
                    f"Product={product_id}"
                )

                page = 1

                while True:

                    data = await worker.fetch(
                        product_id,
                        page,
                    )

                    reviews = data.get(
                        "data",
                        [],
                    )

                    if not reviews:
                        break

                    for item in reviews:

                        await ReviewService.save_review(
                            session=session,
                            product_id=product_id,
                            item=item,
                        )

                    await session.commit()

                    page += 1

                await ProductRepository.mark_review_crawled(
                    session=session,
                    product_id=product_id,
                    review_count=review_count,
                )

                await session.commit()

        finally:


            await client.close()