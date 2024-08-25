from fastapi import UploadFile, File
import aiofiles
from sqlalchemy import select
from src.files.models import File


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


