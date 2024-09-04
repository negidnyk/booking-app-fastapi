from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta


class CreateAppointment(BaseModel):
    master_id: int
    description: str
    service_id: int
    price: float
    booked_at: datetime
    booked_to: datetime
    created_at: datetime
    is_approved_by_master: bool = False
    is_visited_by_user: bool = False

    class Config:
        from_attributes = True


class GetCreatedAppointment(BaseModel):
    id: int
    master_id: int
    user_id: int
    description: str
    service_id: int
    price: float
    booked_at: datetime
    booked_to: datetime
    created_at: datetime
    is_approved_by_master: bool
    is_visited_by_user: bool

    class Config:
        from_attributes = True


