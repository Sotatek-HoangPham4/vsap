from sqlalchemy import (
    BigInteger,
    String,
    ForeignKey,
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class SentimentLabel(Base):

    __tablename__ = "sentiment_labels"

    review_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("reviews.id"),
        primary_key=True,
    )

    sentiment: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )