from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
    BigInteger,
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class CrawlLog(Base):
    __tablename__ = "crawl_logs"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(50)
    )

    entity_id: Mapped[int]

    current_page: Mapped[int]

    status: Mapped[str]

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )