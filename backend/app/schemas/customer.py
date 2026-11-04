
from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None


class CustomerResponse(BaseModel):
    customer_id: int
    full_name: str
    email: str
    phone: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
