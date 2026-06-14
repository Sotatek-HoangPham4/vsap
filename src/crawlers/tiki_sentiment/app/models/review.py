from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Integer,
    Text,
    DateTime,
    JSON,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    product_id: Mapped[int] = mapped_column(BigInteger, index=True)
    customer_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    seller_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    rating: Mapped[int]

    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)

    review_created_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    delivery_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    thank_count: Mapped[int | None]

    is_photo: Mapped[bool | None] = mapped_column(nullable=True)

    image_count: Mapped[int | None] = mapped_column(nullable=True)

    status: Mapped[str | None] = mapped_column(nullable=True)

    score: Mapped[float | None] = mapped_column(nullable=True)
    new_score: Mapped[float | None] = mapped_column(nullable=True)

    comment_count: Mapped[int | None] = mapped_column(nullable=True)

    raw_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)