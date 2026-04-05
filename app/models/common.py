# app/models/common.py
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, func
from app.db.base import Base

class TimestampMixin:
    """时间戳混入类"""
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class BaseModel(Base, TimestampMixin):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)