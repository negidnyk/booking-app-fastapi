from fastapi import HTTPException
from sqlalchemy import select
from src.auth.models import User
from src.auth.schemas import UserGetsUser
# from src.posts.models import Post


# from posts.helpers import get_creator


async def is_user(role_id):
    if role_id != 3:
        raise HTTPException(status_code=403, detail="This option is for users only")


async def is_admin(role_id):
    if role_id != 1 or role_id != 2:
        raise HTTPException(status_code=403, detail="This option is for admins only")


async def is_master(role_id):
    if role_id != 4:
        raise HTTPException(status_code=403, detail="This option is for masters only")


async def is_user_or_master(role_id):
    if role_id != 3 or role_id != 4:
        raise HTTPException(status_code=403, detail="This option is for masters and users only")


async def is_deleted(user):
    if user.is_deleted is True:
        raise HTTPException(status_code=400, detail=f"User: {user.username} is deleted!")
