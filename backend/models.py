from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from .database import Base

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, index=True)
    label = Column(String)
    conf = Column(Float)
    x1 = Column(Integer); y1 = Column(Integer); x2 = Column(Integer); y2 = Column(Integer)
    cx = Column(Integer); cy = Column(Integer)
    evento = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EventOut(BaseModel):
    id: int
    timestamp: str
    label: str
    conf: float
    x1: int; y1: int; x2: int; y2: int
    cx: int; cy: int
    evento: str

    class Config:
        orm_mode = True
