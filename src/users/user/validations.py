from fastapi import HTTPException
from sqlalchemy import select
from src.auth.models import User
from src.auth.schemas import UserGetsUser
# from src.posts.models import Post


# from posts.helpers import get_creator


def is_user(role_id):
    if role_id == 1 or role_id == 2:
        raise HTTPException(status_code=403, detail="This option is for users only")


def is_deleted(user):
    if user.is_deleted is True:
        raise HTTPException(status_code=400, detail=f"User: {user.username} is deleted!")
