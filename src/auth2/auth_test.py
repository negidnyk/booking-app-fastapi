from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
import jwt
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from src.auth.models import User
from src.auth.schemas import UserCreate, UserRead, UserGetsUser
from typing import Optional
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session



#saske = "spasiiiiii"

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


router = APIRouter(
    prefix="/auth-test",
    tags=["Auth-test"]
)


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None


async def get_user_by_email(session, email: str):
    query = select(User).where(User.email == email)
    user_profile = await session.execute(query)
    profile = user_profile.scalar_one_or_none()
    return profile


async def create_user(session, user):
    hashed_password = await get_password_hash(user.password)
    stmt = insert(User).values(email=user.email,
                               hashed_password=hashed_password,
                               is_active=user.is_active,
                               is_superuser=user.is_superuser,
                               is_verified=user.is_verified,
                               username=user.username,
                               bio=user.bio,
                               role_id=user.role_id,
                               is_deleted=user.is_deleted)
    print(stmt)
    await session.execute(stmt)
    await session.commit()

    query = select(User).limit(1).order_by(User.registered_at.desc())
    created_service = await session.execute(query)
    result = created_service.scalar_one_or_none()
    return UserRead(id=result.id,
                    email=result.email,
                    is_active=result.is_active,
                    is_superuser=result.is_superuser,
                    is_verified=result.is_verified,
                    username=result.username,
                    bio=result.bio,
                    role_id=result.role_id,
                    is_deleted=result.is_deleted)


async def get_current_user(session, token: str = Depends(oauth2_scheme)):
    payload = await decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user_by_email(session, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/users/")
async def create_new_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    db_user = await get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(session, user)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_email(session, form_data.username)
    if not user or not await verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


