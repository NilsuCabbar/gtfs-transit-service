from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Float
from app.db.database import Base
from app.schemas.enums import WheelchairBoardingType, LocationType

class Stop(Base):
    __tablename__ = "stops"
    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=False)
    stop_id = Column(String(255), nullable=False)
    stop_name = Column(String(255), nullable=False)
    stop_lat = Column(Float, nullable=False)
    stop_lon = Column(Float, nullable=False)
    wheelchair_boarding = Column(Enum(WheelchairBoardingType), nullable=True)
    location_type = Column(Enum(LocationType), nullable=True)