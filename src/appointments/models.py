from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData, Double
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    master_proposal_id = Column(Integer, ForeignKey("master_proposal.id", ondelete='CASCADE'))
    booked_at = Column(TIMESTAMP, nullable=False)
    booked_to = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    is_approved_by_master = Column(Boolean, default=False, nullable=False)
    is_visited_by_user = Column(Boolean, default=False, nullable=False)



