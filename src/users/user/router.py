from fastapi import APIRouter, Depends, Query
from typing import Annotated, Union
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
# from src.users.user.services import (get_my_profile,
#                                      complete_registration,
#                                      change_profile,
#                                      get_single_user,
#                                      remove_profile)
from src.users.user.services import UserCrud
from src.auth.schemas import UserUpdate
from src.auth.models import User
import uuid


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.get("/me/", status_code=200)
async def get_me(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_active_user)):
    return await UserCrud.get_my_profile(session, user)


@router.patch("/complete_my_profile/", status_code=201)
async def complete_profile(profile: UserUpdate, session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_active_user)):
    return await UserCrud.complete_registration(profile, session, user)


@router.patch("/update_me/", status_code=201)
async def update_my_profile(profile: UserUpdate, session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_active_user)):
    return await UserCrud.change_profile(profile, session, user)


@router.get("/{user_id}/", status_code=200)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await UserCrud.get_single_user(session, user_id, user)


@router.delete("/delete_me/", status_code=201)
async def delete_profile(session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    return await UserCrud.remove_profile(session, user)
