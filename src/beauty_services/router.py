from fastapi import APIRouter, Depends, Query
from typing import Annotated, Union
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.beauty_services.services import BeautyServiceCrud
from src.beauty_services.schemas import CreateBeautyService, GetBeautyService, CreateBeautyServiceGroup, \
    GetBeautyServiceGroup


router = APIRouter(
    prefix="/beauty_service",
    tags=["Beauty_service"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.post("/service", status_code=201)
async def create_beauty_service(service: CreateBeautyService, session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_active_user)):
    return await BeautyServiceCrud.create_service(service, session, user)


@router.get("/service", status_code=200)
async def get_beauty_services(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_active_user)):
    return await BeautyServiceCrud.get_all_beauty_services(skip, limit, session, user)


@router.get("/service_group/{group_id}", status_code=200)
async def get_services_by_group(group_id: int, skip: int = 0, limit: int = 10,
                                session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_active_user)):
    return await BeautyServiceCrud.get_beauty_services_by_group(group_id, skip, limit, session, user)



@router.post("/group", status_code=201)
async def create_beauty_service_group(group: CreateBeautyServiceGroup,
                                      session: AsyncSession = Depends(get_async_session),
                                      user: User = Depends(current_active_user)):
    return await BeautyServiceCrud.create_service_group(group, session, user)
