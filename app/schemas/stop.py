from pydantic import BaseModel, Field
from app.schemas.enums import WheelchairBoardingType, LocationType

class Stop(BaseModel):
    stop_id: str = Field(..., min_length=1, max_length=50)
    stop_name: str = Field(..., min_length=1, max_length=50)
    stop_lat: float = Field(..., ge=-90, le=90)
    stop_lon: float = Field(..., ge=-180, le=180)
    wheelchair_boarding: WheelchairBoardingType
    location_type: LocationType