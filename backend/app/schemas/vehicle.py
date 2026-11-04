from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class VehicleCreate(BaseModel):
    plate_hash: str = Field(min_length=1, max_length=255)
    vehicle_type: str = Field(min_length=1, max_length=60)
    capacity_kg: Decimal = Field(gt=0)
    is_active: bool = True

class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    vehicle_id: int
    plate_hash: str
    vehicle_type: str
    capacity_kg: Decimal
    is_active: bool
