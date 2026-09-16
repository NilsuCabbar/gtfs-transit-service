from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.enums import DirectionType

class Trip(BaseModel):
    route_id: str = Field(..., min_length=1, max_length=50)
    service_id: str = Field(..., min_length=1, max_length=50)
    trip_id: str = Field(..., min_length=1, max_length=50)
    trip_headsign: Optional[str] = Field(None, max_length=100)
    direction_id: Optional[DirectionType] = Field(None)
    shape_id: Optional[str] = Field(None, max_length=50)

class TripOut(BaseModel):
    id: int = Field(...)
    route_id: int # artık DB'nin integer id'si, GTFS string'i değil
    service_id: str = Field(..., min_length=1, max_length=50)
    trip_id: str = Field(..., min_length=1, max_length=50)
    trip_headsign: Optional[str] = Field(None, max_length=100)
    direction_id: Optional[DirectionType] = Field(None)
    shape_id: Optional[str] = Field(None, max_length=50)
    class Config:
        from_attributes = True