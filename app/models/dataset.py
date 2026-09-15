from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.database import Base

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)