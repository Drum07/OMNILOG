
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DECIMAL, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("categories.category_id"), nullable=False
    )
    sku: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    product_name: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    unit_weight_kg: Mapped[Decimal] = mapped_column(DECIMAL(10, 3), nullable=False)
    is_hazardous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
