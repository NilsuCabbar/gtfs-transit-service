from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float
from app.db.database import Base
from app.schemas.enums import PickupType, DropOffType

class StopTime(Base):
    __tablename__ = "stop_times"
    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    stop_id = Column(Integer, ForeignKey("stops.id"), nullable=False)
    stop_sequence = Column(Integer, nullable=False)
    departure_time = Column(String(8), nullable=False)
    pickup_type = Column(Enum(PickupType), nullable=True)
    drop_off_type = Column(Enum(DropOffType), nullable=True)
    arrival_time = Column(String(8), nullable=False)
    shape_dist_traveled = Column(Float, nullable=True)