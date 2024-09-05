from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, Double
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()


class BeautyService(Base):
    __tablename__ = "beauty_service"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    description = Column(String(200), nullable=True)
    added_by = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

