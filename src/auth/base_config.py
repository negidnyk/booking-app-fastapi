from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication import JWTStrategy
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy
from fastapi import Depends
from .models import AccessToken, User

from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.utils import get_access_token_db
from config import AUTH_SECRET

# cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_database_strategy(access_token_db: AccessTokenDatabase[get_access_token_db] = Depends(get_access_token_db),)\
        -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)



# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret=AUTH_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
