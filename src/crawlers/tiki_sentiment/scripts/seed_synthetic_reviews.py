from pathlib import Path
import sys
import asyncio
import random
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import random
import uuid
import hashlib
import logging
from datetime import datetime

from app.core.database import AsyncSessionLocal
from sqlalchemy.dialects.postgresql import insert
from app.models.product import Product
from app.models.review import Review

from sqlalchemy import select, text


negative_templates = [
    "Sản phẩm {product} dùng rất tệ, không như mong đợi.",
    "Chất lượng {product} quá kém, chỉ dùng vài ngày đã hỏng.",
    "{product} không hoạt động đúng như mô tả.",
    "Rất không hài lòng với {product}, trải nghiệm tệ.",
    "{product} giao bị lỗi, không sử dụng được.",
    "Đóng gói cẩu thả, {product} bị hư khi nhận.",
    "{product} chất lượng thấp, không đáng tiền.",
    "Thất vọng với {product}, dùng rất nhanh hỏng.",
    "{product} hoạt động không ổn định, lúc được lúc không.",
    "Sản phẩm {product} bị lỗi ngay khi mở hộp.",

    "Không nên mua {product}, chất lượng quá tệ.",
    "{product} không giống mô tả, bị lừa rồi.",
    "Trải nghiệm rất kém với {product}.",
    "{product} dùng được 1–2 ngày là hỏng.",
    "Rất thất vọng, {product} không sử dụng được lâu.",
    "{product} hay bị lỗi vặt.",
    "Không hài lòng, {product} quá kém chất lượng.",
    "{product} hoạt động rất yếu.",
    "{product} bị lỗi pin rất nhanh.",
    "{product} sạc không vào, rất tệ.",

    "Âm thanh {product} rất kém, rè và nhỏ.",
    "{product} kết nối kém, hay bị ngắt.",
    "{product} nóng nhanh, dễ hỏng.",
    "{product} bị trầy xước khi nhận hàng.",
    "Chất liệu {product} rất rẻ tiền.",
    "{product} không giống ảnh quảng cáo.",
    "Giao hàng chậm, {product} bị lỗi.",
    "{product} dùng rất khó chịu.",
    "{product} không bền như quảng cáo.",
    "Hiệu năng {product} rất yếu.",

    "Không xứng đáng với giá tiền của {product}.",
    "{product} bị hỏng sau vài lần sử dụng.",
    "{product} dễ bị treo, lag liên tục.",
    "{product} không nhận kết nối.",
    "{product} pin tụt rất nhanh.",
    "{product} không sạc được.",
    "Chất lượng gia công {product} rất kém.",
    "{product} bị lỗi phần cứng.",
    "{product} chạy rất chậm.",
    "{product} không ổn định khi sử dụng lâu.",

    "{product} rất ồn khi hoạt động.",
    "{product} rung mạnh, khó chịu.",
    "{product} thiết kế kém, dễ vỡ.",
    "{product} bị lỗi ngay lần đầu sử dụng.",
    "{product} không bật được.",
    "{product} không có hiệu quả như quảng cáo.",
    "Quá tệ, {product} không dùng được.",
    "{product} nhanh nóng và tự tắt.",
    "{product} bị lỗi cảm ứng.",
    "{product} không phản hồi khi sử dụng.",

    "Không hài lòng vì {product} quá yếu.",
    "{product} không đáng mua.",
    "{product} hoạt động rất chập chờn.",
    "{product} bị lỗi liên tục.",
    "{product} không bền.",
    "{product} dễ hỏng khi va chạm nhẹ.",
    "{product} bị lỗi khi cập nhật.",
    "{product} không tương thích.",
    "{product} không dùng được sau 1 tuần.",
    "{product} chất lượng hoàn thiện rất tệ.",

    "{product} không đúng mô tả sản phẩm.",
    "{product} không giống hình ảnh.",
    "{product} bị lỗi ngay từ đầu.",
    "{product} hoạt động kém hơn mong đợi.",
    "{product} dễ bị nóng máy.",
    "{product} không ổn định khi chạy.",
    "{product} hay bị treo máy.",
    "{product} bị lỗi kết nối.",
    "{product} không thể sử dụng lâu dài.",
    "{product} dễ bị hỏng linh kiện.",

    "Rất tệ, {product} không dùng được.",
    "{product} gây thất vọng lớn.",
    "{product} chất lượng rất thấp so với giá.",
    "{product} không thể sử dụng bình thường.",
    "{product} bị lỗi liên tục khi dùng.",
    "{product} không đạt yêu cầu cơ bản.",
    "{product} bị hỏng nhanh chóng.",
    "{product} không đáng để mua.",
    "{product} trải nghiệm cực kỳ tệ.",
    "{product} không hoạt động ổn định."
] 

neutral_templates = [
    "Sản phẩm {product} dùng tạm ổn, không quá nổi bật.",
    "{product} ở mức bình thường, không có gì đặc biệt.",
    "Trải nghiệm với {product} khá ổn.",
    "{product} dùng được, nhưng không xuất sắc.",
    "Chất lượng {product} ở mức trung bình.",
    "{product} không tốt lắm nhưng cũng không tệ.",
    "Sản phẩm {product} dùng ổn trong tầm giá.",
    "{product} tạm dùng được.",
    "Mức độ hài lòng với {product} là trung bình.",
    "{product} không có gì để phàn nàn nhiều.",

    "{product} hoạt động bình thường.",
    "{product} dùng được nhưng chưa ấn tượng.",
    "{product} ổn so với giá tiền.",
    "Chất lượng {product} chấp nhận được.",
    "{product} không quá tốt cũng không quá tệ.",
    "{product} dùng ổn định.",
    "{product} không nổi bật.",
    "Sản phẩm {product} ở mức khá.",
    "{product} dùng tạm được.",
    "{product} không gây thất vọng nhưng cũng không wow.",

    "{product} đáp ứng nhu cầu cơ bản.",
    "{product} hoạt động ổn trong thời gian ngắn.",
    "{product} dùng được trong điều kiện bình thường.",
    "{product} không có lỗi lớn.",
    "{product} chấp nhận được với mức giá.",
    "{product} không quá ấn tượng.",
    "{product} dùng ổn định trong thời gian đầu.",
    "{product} không có vấn đề nghiêm trọng.",
    "{product} tạm ổn, chưa thực sự tốt.",
    "{product} ở mức chấp nhận được.",

    "{product} không quá nổi bật nhưng dùng được.",
    "{product} phù hợp nhu cầu cơ bản.",
    "{product} hoạt động bình thường như mong đợi.",
    "{product} không có gì đặc biệt.",
    "{product} dùng ổn nhưng chưa bền lắm.",
    "{product} trải nghiệm trung bình.",
    "{product} không gây khó chịu khi dùng.",
    "{product} ổn trong tầm giá.",
    "{product} không có lỗi rõ ràng.",
    "{product} dùng được nhưng chưa tốt.",

    "{product} hoạt động tương đối ổn.",
    "{product} không quá xuất sắc.",
    "{product} dùng ổn với nhu cầu nhẹ.",
    "{product} ở mức vừa phải.",
    "{product} không gây ấn tượng mạnh.",
    "{product} dùng được cho nhu cầu cơ bản.",
    "{product} chất lượng trung bình khá.",
    "{product} không có điểm nổi bật.",
    "{product} hoạt động bình thường, ổn định.",
    "{product} không quá tốt nhưng chấp nhận được.",

    "{product} dùng ổn trong thời gian ngắn.",
    "{product} không quá tệ cũng không quá tốt.",
    "{product} đáp ứng nhu cầu tối thiểu.",
    "{product} dùng được cho công việc nhẹ.",
    "{product} không có vấn đề lớn.",
    "{product} ở mức ổn định.",
    "{product} không gây thất vọng lớn.",
    "{product} dùng ổn định tạm thời.",
    "{product} không có lỗi nghiêm trọng.",
    "{product} chấp nhận được trong tầm giá.",

    "{product} không quá nổi bật nhưng ổn.",
    "{product} dùng được bình thường.",
    "{product} không có gì để chê nhiều.",
    "{product} ở mức trung bình khá.",
    "{product} hoạt động ổn định cơ bản.",
    "{product} không gây vấn đề khi dùng.",
    "{product} dùng tạm ổn định.",
    "{product} không có điểm nhấn.",
    "{product} dùng ổn nhưng không lâu dài.",
    "{product} chấp nhận được với nhu cầu cơ bản.",

    "{product} không quá tốt nhưng dùng được.",
    "{product} hoạt động vừa đủ.",
    "{product} ở mức trung bình thị trường.",
    "{product} không có gì đặc sắc.",
    "{product} dùng ổn cho nhu cầu nhẹ.",
    "{product} không có lỗi đáng kể.",
    "{product} hoạt động ổn định tạm thời.",
    "{product} dùng được trong ngắn hạn.",
    "{product} không quá nổi bật.",
    "{product} chấp nhận được."
]


# =========================
# LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("synthetic-seeder")


# =========================
# CONFIG
# =========================
NEGATIVE_TARGET = 10482
NEUTRAL_TARGET = 30684
BATCH_SIZE = 2000


# =========================
# UTILS
# =========================

import re

def clean_product_name(name: str) -> str:
    name = name.lower().strip()

    # chỉ remove ký tự rác cực đoan
    name = re.sub(r"[^\w\s\-\(\)']", " ", name)

    # collapse spaces
    name = re.sub(r"\s+", " ", name)

    return name.strip()

def hash_key(product_id, text):
    return hashlib.md5(f"{product_id}-{text}".encode()).hexdigest()


def random_bigint():
    return random.randint(1_000_000, 9_999_999_999)

def log_review(i, total, sentiment, review_obj):
    logger.info(
        f"[{sentiment.upper()} {i}/{total}] "
        f"product_id={review_obj['product_id']} | "
        f"rating={review_obj['rating']} | "
        f"text={review_obj['content'][:200]}"
    )


# =========================
# TEXT ENGINE
# =========================
def gen_text(template_list, product_name):
    product_name = clean_product_name(product_name)
    return random.choice(template_list).format(product=product_name)


# =========================
# PRODUCT MAP
# =========================
async def get_product_map(session):
   

    stmt = select(Product.id, Product.name)
    result = await session.execute(stmt)

    data = {r.id: r.name for r in result.fetchall()}

    logger.info(f"Loaded {len(data)} products")
    return data


# =========================
# PRODUCTS WITHOUT REVIEWS
# =========================
async def get_products_without_reviews(session):
    logger.info("Fetching products without reviews...")

    stmt = (
        select(Product.id)
        .outerjoin(Review, Review.product_id == Product.id)
        .where(Review.id.is_(None))
    )

    result = await session.execute(stmt)
    data = [r[0] for r in result.fetchall()]

    logger.info(f"Found {len(data)} products without reviews")
    return data


# =========================
# BUILD REVIEW
# =========================
def build_review(product_id, product_name, sentiment, templates):

    if sentiment == "negative":
        rating = random.choice([1, 2])
        status = "negative"

    elif sentiment == "neutral":
        rating = 3
        status = "neutral"

    else:
        rating = 5
        status = "positive"

    text = gen_text(templates, product_name)

    created_time = datetime.utcnow()

    return {
        "id": random_bigint(),

        # core
        "product_id": product_id,
        "customer_id": random_bigint(),
        "seller_id": random_bigint(),

        # sentiment core
        "rating": rating,
        "status": status,

        # text
        "title": "",
        "content": text,

        # time fields
        "review_created_time": created_time,
        "delivery_date": created_time - timedelta(days=random.randint(1, 10)),
        "created_at": created_time,

        # engagement simulation
        "thank_count": random.randint(0, 50),
        "comment_count": random.randint(0, 10),
        "image_count": random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1])[0],
        "is_photo": False,

        # scoring (important for ML feature)
        "score": float(rating + random.uniform(-0.3, 0.3)),
        "new_score": float(rating + random.uniform(-0.5, 0.5)),

        # raw trace
        "raw_json": {
            "source": "synthetic",
            "sentiment": status,
            "product_name": product_name
        }
    }


# =========================
# MAIN PIPELINE
# =========================
async def seed():
    async with AsyncSessionLocal() as session:

        logger.info("🚀 START SYNTHETIC SEEDING PIPELINE")

        product_ids = await get_products_without_reviews(session)
        product_map = await get_product_map(session)

        if not product_ids:
            logger.warning("No products found → exit")
            return

        data = []
        seen = set()

        def safe_add(item):
            key = hash_key(item["product_id"], item["content"])
            if key in seen:
                return False
            seen.add(key)
            data.append(item)
            return True

        # =========================
        # NEGATIVE
        # =========================
        

        neg_count = 0
        i = 0

        while neg_count < NEGATIVE_TARGET:
            pid = random.choice(product_ids)
            name = product_map.get(pid, "sản phẩm")

            review = build_review(pid, name, "negative", negative_templates)

            if safe_add(review):
                neg_count += 1
                i += 1

                # 🔥 LOG EACH RECORD
                log_review(neg_count, NEGATIVE_TARGET, "negative", review)

          

        

        # =========================
        # NEUTRAL
        # =========================
        

        neu_count = 0
        i = 0

        while neu_count < NEUTRAL_TARGET:
            pid = random.choice(product_ids)
            name = product_map.get(pid, "sản phẩm")

            review = build_review(pid, name, "neutral", neutral_templates)

            if safe_add(review):
                neu_count += 1
                i += 1

                # 🔥 LOG EACH RECORD
                log_review(neu_count, NEUTRAL_TARGET, "neutral", review)

    

        

        # =========================
        # INSERT BATCH (OPTIMIZED)
        # =========================
        logger.info(f"Total records generated: {len(data)}")
      

        stmt = insert(Review)

        for i in range(0, len(data), BATCH_SIZE):
            batch = data[i:i + BATCH_SIZE]

            await session.execute(stmt, batch)
            await session.commit()

            logger.info(f"Inserted batch {i}-{i+len(batch)}")

        logger.info("🎉 PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    asyncio.run(seed())