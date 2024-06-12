from typing import Optional

from fastapi import FastAPI

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.users.user.router import router as users_router
from src.users.masters.router import router as masters_router
from src.services.router import router as services_router

app = FastAPI(
    title="Booking App"
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


current_user = fastapi_users.current_user()

app.include_router(users_router)
app.include_router(masters_router)
app.include_router(services_router)
