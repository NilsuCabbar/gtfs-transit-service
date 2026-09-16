from pydantic import BaseModel, Field
from app.schemas.enums import PickupType, DropOffType
from typing import Optional

class StopTime(BaseModel):
    trip_id: str = Field(..., min_length=1, max_length=50)
    stop_id: str = Field(..., min_length=1, max_length=50)
    stop_sequence: int = Field(..., ge=1)
    departure_time: str = Field(..., min_length=1, max_length=8)
    pickup_type: Optional[PickupType] = None
    drop_off_type: Optional[DropOffType] = None
    arrival_time: str = Field(..., min_length=1, max_length=8)
    shape_dist_traveled: Optional[float] = Field(None, ge=0)