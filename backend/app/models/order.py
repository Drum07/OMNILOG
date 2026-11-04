
from decimal import Decimal
from datetime import datetime

from sqlalchemy import BigInteger, DECIMAL, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    customer_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("customers.customer_id"), nullable=False
    )
    order_number: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    order_status: Mapped[str] = mapped_column(
        String(30), nullable=False
    )
    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    shipping_amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    placed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
