from fastapi import APIRouter, Depends, Query
from typing import Annotated, Union
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.users.user.services import get_my_profile, get_user_profile, update_my_profile, delete_my_profile, \
    complete_users_profile, complete_masters_profile
from src.auth.schemas import UserUpdate
from src.services.schemas import ServiceTypes


router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.get("/", status_code=200)
async def get_all_services(session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_active_user)):
    return await get_my_profile(session, user)

# @router.post("/", status_code=201)
# async def create_service(session: AsyncSession = Depends(get_async_session),
#                            user: User = Depends(current_active_user)):
#     return await create_a_service(session, user)

# @router.post("/groups", status_code=201)
# async def create_service_group(session: AsyncSession = Depends(get_async_session),
#                            user: User = Depends(current_active_user)):
#     return await create_a_service_group(session, user)


@router.get("/groups", status_code=200)
async def get_all_services_groups(session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_active_user)):
    return await get_my_profile(session, user)


@router.get("/services_by_groups", status_code=200)
async def get_services_by_groups(session: AsyncSession = Depends(get_async_session),
                                 user: User = Depends(current_active_user)):
    return await get_my_profile(session, user)


@router.delete("/groups", status_code=201)
async def delete_service_group(session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await delete_my_profile(user, session)


@router.delete("/", status_code=201)
async def delete_service(session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await delete_my_profile(user, session)
