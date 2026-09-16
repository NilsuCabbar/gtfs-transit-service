from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.db.database import Base
from app.schemas.enums import RouteType


class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id"), nullable=False)
    route_id = Column(String(100), nullable=False)
    route_short_name = Column(String(100), nullable=False)
    route_long_name = Column(String(100), nullable=False)
    agency_id = Column(String(100), nullable=False)
    route_type = Column(Enum(RouteType), nullable=False)