from pathlib import Path
import sys
import asyncio
import random
from datetime import datetime, timedelta

# 👉 FIX IMPORT PATH (giữ nguyên app)
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core.database import AsyncSessionLocal
from app.models.review import Review
from sqlalchemy import insert


def random_date(start_year=2020, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def generate_review(i: int):
    created_time = random_date()
    delivery_time = created_time - timedelta(days=random.randint(1, 10))

    return {
        "id": i,
        "product_id": random.randint(1000, 999999),
        "customer_id": random.randint(10000, 999999) if random.random() > 0.1 else None,
        "seller_id": random.randint(1, 1000) if random.random() > 0.05 else None,

        "rating": random.randint(1, 5),
        "title": random.choice(["Tốt", "Bình thường", "Không ổn", "Rất tốt", None]),
        "content": "This is a sample review content " + str(i),

        "review_created_time": created_time,
        "delivery_date": delivery_time,

        "thank_count": random.randint(0, 50),
        "is_photo": random.choice([True, False]),
        "image_count": random.randint(0, 5),

        "status": random.choice(["approved", "pending", "rejected"]),

        "score": round(random.random() * 100, 6),
        "new_score": round(random.random(), 6),

        "comment_count": random.randint(0, 10),

        "raw_json": {
            "id": i,
            "rating": random.randint(1, 5),
            "content": "sample"
        },

        "created_at": datetime.utcnow()
    }


async def seed():
    async with AsyncSessionLocal() as session:

        batch_size = 1000
        total = 10_000

        for start in range(0, total, batch_size):

            batch = [
                generate_review(i)
                for i in range(start + 1, start + batch_size + 1)
            ]

            # 👉 async insert chuẩn
            await session.execute(insert(Review), batch)
            await session.commit()

            print(f"Inserted {start + batch_size}/{total}")


if __name__ == "__main__":
    asyncio.run(seed())