from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, Double
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()


class BeautyServiceGroup(Base):
    __tablename__ = "beauty_service_group"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    added_by = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class BeautyService(Base):
    __tablename__ = "beauty_service"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    added_by = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)


class BeautyServiceWithGroup(Base):
    __tablename__ = "beauty_service_with_group"
    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    service_id = Column(Integer, ForeignKey("beauty_service.id", ondelete='CASCADE'))
    group_id = Column(Integer, ForeignKey("beauty_service_group.id", ondelete='CASCADE'))
    added_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
