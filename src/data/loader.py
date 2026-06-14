import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "crawlers" / "tiki_sentiment"))

import pandas as pd
from src.crawlers.tiki_sentiment.app.core.database import AsyncSessionLocal
from src.crawlers.tiki_sentiment.app.repositories.review_repository import ReviewRepository


async def load_labeled_reviews():
    async with AsyncSessionLocal() as session:
        rows = await ReviewRepository.get_labeled_reviews(session)

    data = []
    for r in rows:
        data.append({
            "text": " ".join(filter(None, [r.title, r.content])),
            "rating": r.rating,
            "thank_count": r.thank_count or 0,
            "is_photo": int(bool(r.is_photo)),
            "seller_id": r.seller_id or -1,
            "review_created_time": r.review_created_time,
            "delivery_date": r.delivery_date,
            "label": r.sentiment
        })

    return pd.DataFrame(data)