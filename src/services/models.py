from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()


class Service(Base):
    __tablename__ = "services"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    services_group_id = Column(Integer, ForeignKey("service_groups.id"), nullable=False)


class ServiceGroup(Base):
    __tablename__ = "service_groups"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    name = Column(String(200), nullable=False)
