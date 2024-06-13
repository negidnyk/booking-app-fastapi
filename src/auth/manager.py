from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
import uuid
from src.auth.models import User
from src.auth.utils import get_user_db

from config import RESET_PASS_SECRET
import re
from typing import Any, Dict, Generic, Optional, Union

from fastapi import Request, Response, HTTPException

from fastapi_users import exceptions, models, schemas

RESET_PASSWORD_TOKEN_AUDIENCE = "fastapi-users:reset"
VERIFY_USER_TOKEN_AUDIENCE = "fastapi-users:verify"


async def validate_password(password: str, user: Union[schemas.UC, models.UP]) -> None:
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password should contain at least 8 characters")

    if len(password) > 30:
        raise HTTPException(status_code=400, detail="Password should not contain more than 30 characters")

    if re.search(r'\d', password) and not re.search(r'[a-zA-Z]', password) or re.search(r'[a-zA-Z]', password) and not \
            re.search(r'\d', password):
        raise HTTPException(status_code=400, detail="Password should contain at least 1 letter and 1 digit")

    if re.search(r'[а-яА-я]', password):
        raise HTTPException(status_code=400, detail="Password should contain latinic characters only")

    else:
        return  # pragma: no cover


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = RESET_PASS_SECRET
    verification_token_secret = RESET_PASS_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = user_create.role_id

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
