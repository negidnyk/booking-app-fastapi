from fastapi import APIRouter, Depends, Query
from typing import Annotated, Union
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.appointments.services import AppointmentsCrud
from src.appointments.schemas import CreateAppointment


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.post("/", status_code=201)
async def create_appointment(appointment: CreateAppointment, session: AsyncSession = Depends(get_async_session)):
    return await AppointmentsCrud.create_appointment(appointment, session)
