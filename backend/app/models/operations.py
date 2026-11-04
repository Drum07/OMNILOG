
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    DECIMAL,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    JSON,
    LargeBinary,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.base import Base


class WarehouseLocation(Base):
    __tablename__ = "warehouse_locations"

    location_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    warehouse_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("warehouses.warehouse_id"), nullable=False
    )
    aisle: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    shelf: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    level_no: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    max_weight_kg: Mapped[Decimal] = mapped_column(DECIMAL(12, 3))
    hazardous_allowed: Mapped[bool] = mapped_column(Boolean)
    location_status: Mapped[str] = mapped_column(String(30))


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("products.product_id")
    )
    warehouse_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("warehouses.warehouse_id")
    )
    location_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("warehouse_locations.location_id")
    )
    quantity: Mapped[Decimal] = mapped_column(DECIMAL(14, 3))
    reserved_quantity: Mapped[Decimal] = mapped_column(DECIMAL(14, 3))
    updated_at: Mapped[datetime] = mapped_column(DateTime)


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)


class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    role_name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime)


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("roles.role_id"), primary_key=True
    )
    assigned_at: Mapped[datetime] = mapped_column(DateTime)


class Driver(Base):
    __tablename__ = "drivers"

    driver_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150))
    license_number_hash: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(30))
    is_active: Mapped[bool] = mapped_column(Boolean)


class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    plate_hash: Mapped[str] = mapped_column(String(255), unique=True)
    vehicle_type: Mapped[str] = mapped_column(String(50))
    capacity_kg: Mapped[Decimal] = mapped_column(DECIMAL(12, 3))
    is_active: Mapped[bool] = mapped_column(Boolean)


class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    route_code: Mapped[str] = mapped_column(String(50), unique=True)
    origin_warehouse_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("warehouses.warehouse_id")
    )
    destination_description: Mapped[str] = mapped_column(Text)
    planned_distance_km: Mapped[Decimal] = mapped_column(DECIMAL(12, 3))
    estimated_cost: Mapped[Decimal] = mapped_column(DECIMAL(12, 2))
    route_status: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime)


class Delivery(Base):
    __tablename__ = "deliveries"

    delivery_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("orders.order_id"), unique=True
    )
    route_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("routes.route_id")
    )
    vehicle_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("vehicles.vehicle_id")
    )
    driver_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("drivers.driver_id")
    )
    tracking_code: Mapped[str] = mapped_column(String(100), unique=True)
    delivery_status: Mapped[str] = mapped_column(String(30))
    shipped_at: Mapped[datetime | None] = mapped_column(DateTime)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime)


class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("orders.order_id")
    )
    payment_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)
    payment_method: Mapped[str] = mapped_column(String(30))
    payment_status: Mapped[str] = mapped_column(String(30))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2))
    paid_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime)


class CustomerAddress(Base):
    __tablename__ = "customer_addresses"

    address_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("customers.customer_id")
    )
    address_type: Mapped[str] = mapped_column(String(30))
    street: Mapped[str] = mapped_column(String(150))
    number: Mapped[str] = mapped_column(String(20))
    complement: Mapped[str | None] = mapped_column(String(100))
    district: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    state_code: Mapped[str] = mapped_column(String(10))
    postal_code: Mapped[str] = mapped_column(String(20))
    country_code: Mapped[str] = mapped_column(String(2))
    is_default: Mapped[bool] = mapped_column(Boolean)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id")
    )
    entity_name: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[int] = mapped_column(BigInteger)
    action_name: Mapped[str] = mapped_column(String(50))
    details: Mapped[dict | None] = mapped_column(JSON)
    ip_address: Mapped[bytes | None] = mapped_column(LargeBinary(16))
    created_at: Mapped[datetime] = mapped_column(DateTime)
