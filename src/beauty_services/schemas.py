from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta


class CreateBeautyService(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class GetBeautyService(CreateBeautyService):
    id: int
    added_by: int
    created_at: datetime

    class Config:
        from_attributes = True


