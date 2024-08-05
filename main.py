from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.users.user.router import router as users_router
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import FastAPI
from fastapi import Request
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from config import GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID, SECRET_KEY
from src.users.user.services import UserCrud
from database import get_async_session
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas import UserCreate
from src.auth.models import OauthUser
from src.auth.manager import UserManager
from src.auth.utils import get_user_db
from src.users.user.services import UserCrud


app = FastAPI(
    title="Booking App"
)

# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["Auth"],
)


current_user = fastapi_users.current_user()

app.include_router(users_router)


@app.get('/')
async def public(request: Request, session: AsyncSession = Depends(get_async_session)):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        given_name = user.get('given_name')
        family_name = user.get('family_name')
        email = user.get('email')
        profile_picture = user.get('picture')
        print(user)

        payload = {}
        payload['email'] = email
        payload['hashed_password'] = ""
        payload['is_active'] = True
        payload['is_superuser'] = False
        payload['is_verified'] = True
        payload['username'] = name
        payload['role_id'] = 3
        payload['is_deleted'] = False

        # google_user = UserManager(get_user_db)
        # await google_user.create(UserCreate(email=email,
        #                                     password="Qwerty12#",
        #                                     is_active=True,
        #                                     is_superuser=False,
        #                                     is_verified=True,
        #                                     username="ArtemGoogle",
        #                                     role_id=3,
        #                                     is_deleted=False))
        await UserCrud.create_google_user_profile(email=email, name=name, session=session)
        # google_user = UserManager(get_user_db)
        # await google_user.create(user_create=UserCreate(username="GOOGLEUSERARTEMYAVTUSHENKO",
        #                                     email=email,
        #                                     password="google_user1235",
        #                                     role_id=3,
        #                                     is_active=True,
        #                                     is_superuser=False,
        #                                     is_verified=True,
        #                                     is_deleted=False))
        return HTMLResponse(f'<p>Hello, {name}!</p>'
                            f'<p>Твое имя: {given_name}</p>'
                            f'<p>Твоя фамилия: {family_name}</p>'
                            f'<p>Твоя почта: {email}</p>'
                            f'<p>Ссылка но аватарку: {profile_picture}</p>'
                            f'<a href=/logout>Logout</a>')
    return HTMLResponse('<a href=/login>Login</a>')


@app.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the url for our /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth/google')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = access_token.get('userinfo')
    print(user)
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')
