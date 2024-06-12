from fastapi import HTTPException
from sqlalchemy import select, update, delete
from src.auth.models import User
from src.auth.schemas import UserGetsUser
# from src.users.user.helpers import get_avatar
# from src.files.helpers import validate_media, file_exist
from src.files.models import File
from src.users.user.validations import is_user


async def get_my_profile(session, user):

    is_user(user.role_id)

    query = select(User).where(User.id == user.id)
    my_profile = await session.execute(query)
    result_list = my_profile.scalars().one()

    return UserGetsUser(id=result_list.id,
                        email=result_list.email,
                        username=result_list.username,
                        bio=result_list.bio
                        )


async def update_my_profile(profile, session, user):

    is_user(user.role_id)

    payload = {}

    if profile.username is not None:
        payload["username"] = profile.username

    if profile.bio is not None:
        payload["bio"] = profile.bio

    stmt = update(User).where(User.id == user.id).values(**payload)
    await session.execute(stmt)
    await session.commit()

    query = select(User).where(User.id == user.id)
    my_profile = await session.execute(query)
    result_list = my_profile.scalars().one()

    return UserGetsUser(id=result_list.id,
                        email=result_list.email,
                        username=result_list.username,
                        bio=result_list.bio
                        )
                        # avatar=await get_avatar(user.id, session))


async def complete_masters_profile(profile, session, user):

    is_user(user.role_id)

    payload = {}

    if profile.username is not None:
        payload["username"] = profile.username

    if profile.bio is not None:
        payload["bio"] = profile.bio

    stmt = update(User).where(User.id == user.id).values(**payload)
    await session.execute(stmt)
    await session.commit()

    query = select(User).where(User.id == user.id)
    my_profile = await session.execute(query)
    result_list = my_profile.scalars().one()

    return UserGetsUser(id=result_list.id,
                        email=result_list.email,
                        username=result_list.username,
                        bio=result_list.bio
                        )
                        # avatar=await get_avatar(user.id, session))


async def complete_users_profile(profile, session, user):

    return update_my_profile(profile, session, user)


async def get_user_profile(user_id, session, user):

    is_user(user.role_id)

    query = select(User).where(User.id == user_id)
    user_profile = await session.execute(query)
    profile = user_profile.scalar_one_or_none()

    if profile is None or profile.role_id == 1 or profile.role_id == 2:
        raise HTTPException(status_code=404, detail="User not found")

    else:
        return UserGetsUser(id=profile.id,
                            email=profile.email,
                            username=profile.username,
                            bio=profile.bio
                            )
                            # avatar=await get_avatar(user.id, session))


async def delete_my_profile(session, user):

    is_user(user.role_id)

    query = delete(User).where(User.id == user.id)
    deleted_profile = await session.execute(query)
    result = deleted_profile.scalars().one()

    return {f"Profile with id: {User.id} is successfully deleted"}
