from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Cart(Base):
    __tablename__ = "carts"
    __table_args__ = (CheckConstraint("count >= 1", name="carts_count_positive"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )
    item_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
