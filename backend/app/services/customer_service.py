
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.customer import Customer
from backend.app.schemas.customer import CustomerCreate


def create_customer(db: Session, data: CustomerCreate):
    existing = db.scalar(
        select(Customer).where(Customer.email == str(data.email))
    )

    if existing:
        raise ValueError("Já existe um cliente com esse e-mail.")

    customer = Customer(
        full_name=data.full_name,
        email=str(data.email),
        phone=data.phone,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def list_customers(db: Session):
    statement = select(Customer).order_by(Customer.customer_id)
    return list(db.scalars(statement).all())


def get_customer(db: Session, customer_id: int):
    return db.get(Customer, customer_id)
