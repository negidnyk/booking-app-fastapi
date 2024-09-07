from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta


class CreateBeautyServiceGroup(BaseModel):
    name: str


class GetBeautyServiceGroup(CreateBeautyServiceGroup):
    id: int
    added_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class CreateBeautyService(BaseModel):
    name: str
    group_id: int

    class Config:
        from_attributes = True


class GetBeautyService(BaseModel):
    id: int
    name: str
    group: Optional[GetBeautyServiceGroup] = None
    added_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class GetBeautyServiceByGroup(BaseModel):
    name: str
    added_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class GetBeautyServiceByGroupList(BaseModel):
    id: int
    service: GetBeautyServiceByGroup
