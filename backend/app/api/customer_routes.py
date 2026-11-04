
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import SessionLocal
from backend.app.schemas.customer import CustomerCreate, CustomerResponse
from backend.app.services.customer_service import (
    create_customer,
    list_customers,
    get_customer,
)

router = APIRouter(prefix="/customers", tags=["Customers"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(data: CustomerCreate, db: Session = Depends(get_db)):
    try:
        return create_customer(db, data)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.get("/", response_model=list[CustomerResponse])
def list_all(db: Session = Depends(get_db)):
    return list_customers(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_one(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )

    return customer
