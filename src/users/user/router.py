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
    prefix="/users",
    tags=["Users"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.get("/me", status_code=200)
async def get_my_profile(session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await get_my_profile(session, user)


@router.patch("/complete_my_profile", status_code=201)
async def complete_my_profile(profile: UserUpdate, session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_active_user)):
    return await complete_users_profile(profile, session, user)


@router.patch("/me", status_code=201)
async def update_my_profile(profile: UserUpdate, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await update_my_profile(profile, session, user)


@router.get("/{user_id}", status_code=200)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await get_user_profile(user_id, session, user)


@router.delete("/me", status_code=201)
async def delete_my_profile(session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_active_user)):
    return await delete_my_profile(user, session)
