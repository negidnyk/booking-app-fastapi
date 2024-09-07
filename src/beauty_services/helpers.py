from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from src.beauty_services.models import BeautyService, BeautyServiceGroup, BeautyServiceWithGroup
from src.beauty_services.schemas import CreateBeautyService, GetBeautyService, CreateBeautyServiceGroup, \
    GetBeautyServiceGroup, GetBeautyServiceByGroup


async def get_service_group_by_service(service_id, session):
    query = select(BeautyServiceWithGroup).where(BeautyServiceWithGroup.service_id == service_id)
    group = await session.execute(query)
    result = group.scalar_one_or_none()

    query2 = select(BeautyServiceGroup).where(BeautyServiceGroup.id == result.group_id)
    group2 = await session.execute(query2)
    result2 = group2.scalar_one_or_none()
    return GetBeautyServiceGroup(id=result2.id,
                                 name=result2.name,
                                 added_by=result2.added_by,
                                 created_at=result2.created_at)


async def get_service_by_id(service_id, session):
    query = select(BeautyService).where(BeautyService.id == service_id)
    service = await session.execute(query)
    result = service.scalar_one_or_none()
    return GetBeautyServiceByGroup(id=result.id,
                                   name=result.name,
                                   added_by=result.added_by,
                                   created_at=result.created_at)
