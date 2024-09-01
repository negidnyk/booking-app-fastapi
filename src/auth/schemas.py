from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, Field
from src.files.schemas import MediaOut


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    bio: str = None
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    is_deleted: bool

    class Config:
        from_attributes = True


class UserGetsUser(BaseModel):
    id: int
    email: str
    username: str
    bio: str = None
    avatar: MediaOut = None

    class Config:
        from_attributes = True


class AdminGetsUser(UserRead):
    avatar: MediaOut = None


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    role_id: int = Field(description="1 - Admin, 2 - User, 3 - Superadmin")
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    is_deleted: bool = Field(default=False)

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str = None
    bio: str = None
    avatar_id: int = None


class OauthUserCreate(schemas.BaseOAuthAccount):
    pass