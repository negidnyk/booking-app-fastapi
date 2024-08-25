from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.files.services import upload_an_image


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

current_active_user = fastapi_users.current_user(active=True)

@router.post("/image")
async def upload_image(file: UploadFile, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_active_user)):
    return await upload_an_image(file, session, user)
