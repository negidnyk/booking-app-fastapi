from fastapi import HTTPException
from sqlalchemy import select
# from src.posts.models import Post


# from posts.helpers import get_creator


def is_user(role_id):
    if role_id != 3:
        raise HTTPException(status_code=403, detail="This option is for masters only")

