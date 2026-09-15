from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func
from app.db.database import Base
from app.schemas.enums import StatusType

class Snapshot(Base):
    __tablename__ = "snapshots"
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    minio_object_path = Column(String(255), nullable=True)
    uploaded_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(Enum(StatusType), nullable=False, default=StatusType.UPLOADING)  # uploading, validating, completed, failed
    error_message = Column(String(255), nullable=True)  # If status is failed, this field will contain the error message
    route_count = Column(Integer, nullable=True)
    trip_count = Column(Integer, nullable=True) 
    stop_count = Column(Integer, nullable=True) 