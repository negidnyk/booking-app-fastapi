from fastapi import UploadFile, File
import aiofiles
from fastapi import HTTPException
from sqlalchemy import select
from src.files.models import File


async def checked_media(file_id, session):
    if file_id == 0 or file_id < 0:
        raise HTTPException(status_code=400, detail="Invalid file_id")

    query = select(File).where(File.id == file_id)
    file = await session.execute(query)
    response = file.scalars().first()
    if not response:
        raise HTTPException(status_code=404, detail="There is no file with such id")
    if response.is_used:
        raise HTTPException(status_code=400, detail="File is already used")
    else:
        return True


async def validate_media(file_id, session):
    query = select(File).where(File.id == file_id)
    file = await session.execute(query)
    response = file.scalars().first()
    if response.is_used:
        return True
    else:
        return False


async def file_exist(file_id, session):
    query = select(File).where(File.id == file_id)
    file = await session.execute(query)
    response = file.scalar_one_or_none()
    if response is None:
        return True
    else:
        return False


