from pydantic import BaseModel
from typing import Optional

class DriverCreate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    license_number: Optional[str] = None
    license_category: Optional[str] = None
    is_active: bool = True

class DriverResponse(DriverCreate):
    id: int
    class Config:
        from_attributes = True