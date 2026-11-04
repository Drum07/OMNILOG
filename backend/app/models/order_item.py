
from decimal import Decimal

from sqlalchemy import BigInteger, DECIMAL, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("orders.order_id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("products.product_id"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    line_total: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
