from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

PaymentMethod = Literal["PIX", "CREDIT_CARD", "DEBIT_CARD", "BOLETO", "CASH", "OTHER"]
PaymentStatus = Literal["PENDING", "AUTHORIZED", "PAID", "REFUNDED", "FAILED"]

class PaymentCreate(BaseModel):
    order_id: int
    payment_reference: str | None = None
    payment_method: PaymentMethod
    payment_status: PaymentStatus = "PENDING"
    amount: Decimal = Field(gt=0)
    paid_at: datetime | None = None

class PaymentResponse(PaymentCreate):
    model_config = ConfigDict(from_attributes=True)
    payment_id: int
    created_at: datetime | None = None
