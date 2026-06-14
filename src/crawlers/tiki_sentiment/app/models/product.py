from datetime import datetime
from sqlalchemy import DateTime

from sqlalchemy import (
    BigInteger,
    Integer,
    Float,
    Text,
    DateTime,
    JSON,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    category_id: Mapped[int] = mapped_column(
        BigInteger,
        index=True,
    )

    seller_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        Text,
    )

    price: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    original_price: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    rating_average: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    review_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    thumbnail_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    raw_json: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    last_review_crawl_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    review_crawled_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )