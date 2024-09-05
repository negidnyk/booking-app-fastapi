from fastapi import APIRouter, Depends, Query
from typing import Annotated, Union
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.beauty_services.services import BeautyServiceCrud
from src.beauty_services.schemas import CreateBeautyService, GetBeautyService


router = APIRouter(
    prefix="/beauty_service",
    tags=["Beauty_service"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.post("/", status_code=201)
async def create_beauty_service(service: CreateBeautyService, session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_active_user)):
    return await BeautyServiceCrud.create_service(service, session, user)
