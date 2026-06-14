from sqlalchemy import (
    BigInteger,
    String,
    Integer,
    Boolean,
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    parent_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    root_category_id: Mapped[int]

    name: Mapped[str] = mapped_column(
        String(500)
    )

    url_key: Mapped[str | None]

    full_url_key: Mapped[str | None]

    level: Mapped[int | None] = mapped_column(
        Integer
    )

    product_count: Mapped[int | None]

    is_leaf: Mapped[bool | None] = mapped_column(
        Boolean
    )