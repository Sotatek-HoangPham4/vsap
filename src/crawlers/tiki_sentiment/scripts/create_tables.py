from pathlib import Path
import sys
import asyncio

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core.database import engine
from app.core.database import Base

from app.models.category import Category
from app.models.product import Product
from app.models.review import Review
from app.models.crawl_log import CrawlLog
from app.models.review_label import ReviewLabel
from app.models.sentiment_label import (
    SentimentLabel,
)

async def create_tables():

    print(Base.metadata.tables.keys())

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    print("done")


if __name__ == "__main__":
    asyncio.run(create_tables())