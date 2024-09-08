from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, Double
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()


class MasterProposal(Base):
    __tablename__ = "master_proposal"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    master_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    service_id = Column(Integer, ForeignKey("beauty_service.id", ondelete='CASCADE'))
    price = Column(Double, nullable=False)
    description = Column(String(200), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)



