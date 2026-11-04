
from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    parent_category_id: Mapped[int | None] = mapped_column(
        BigInteger, nullable=True
    )
    category_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
