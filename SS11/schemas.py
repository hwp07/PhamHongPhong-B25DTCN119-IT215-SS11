from pydantic import BaseModel, Field

class ParkingSlotCreate(BaseModel):
    slot_code: str
    zone_name: str = Field(min_length=3)
    max_weight: int = Field(gt=0)
    is_available: bool = True