from pathlib import Path
import sys
import asyncio

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from app.crawlers.category_crawler import CategoryCrawler
from app.crawlers.product_crawler import ProductCrawler
from app.crawlers.review_crawler import ReviewCrawler


async def main():
    # print("=== Crawl Categories ===")
    # await CategoryCrawler().run()

    # print("=== Crawl Products ===")
    # await ProductCrawler().run()

    print("=== Crawl Reviews ===")
    await ReviewCrawler().run()

    print("=== Done ===")


if __name__ == "__main__":
    asyncio.run(main())