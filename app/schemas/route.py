from pydantic import BaseModel, Field
from app.schemas.enums import RouteType

class Route(BaseModel):
    route_id: str = Field(..., min_length=1, max_length=100)
    route_short_name: str = Field(..., min_length=1, max_length=100)
    route_long_name: str = Field(..., min_length=1, max_length=100)
    agency_id: str = Field(..., min_length=1, max_length=100)
    route_type: RouteType

class RouteOut(BaseModel):
    id: int = Field(...)
    route_id: str = Field(..., min_length=1, max_length=100)
    route_short_name: str = Field(..., min_length=1, max_length=100)
    route_long_name: str = Field(..., min_length=1, max_length=100)
    agency_id: str = Field(..., min_length=1, max_length=100)
    route_type: RouteType
    class Config:
        from_attributes = True