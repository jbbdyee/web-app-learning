from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (CheckConstraint("price >= 0", name="products_price_nonnegative"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
