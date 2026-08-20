from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    pwd: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
