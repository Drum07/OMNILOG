
from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    warehouse_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    warehouse_code: Mapped[str] = mapped_column(
        String(30), nullable=False, unique=True
    )
    warehouse_name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state_code: Mapped[str] = mapped_column(String(10), nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
