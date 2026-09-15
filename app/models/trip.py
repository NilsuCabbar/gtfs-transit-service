from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Float
from app.db.database import Base
from app.schemas.enums import DirectionType

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    service_id = Column(String(50), nullable=False)
    trip_id = Column(String(50), nullable=False)
    trip_headsign = Column(String(100), nullable=True)
    direction_id = Column(Enum(DirectionType), nullable=True)
    shape_id = Column(String(50), nullable=True)