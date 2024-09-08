from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta


class CreateMasterProposal(BaseModel):
    service_id: int
    price: float
    description: Optional[str] = None

    class Config:
        from_attributes = True


class GetMasterProposal(CreateMasterProposal):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


