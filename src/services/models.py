from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    description = Column(String(200), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)