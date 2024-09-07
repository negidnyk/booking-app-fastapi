from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from src.auth.models import User
from src.auth.schemas import UserGetsUser
# from src.users.user.helpers import get_avatar
# from src.files.helpers import validate_media, file_exist
from src.files.models import File
from src.files.helpers import validate_media, file_exist, checked_media
from src.files.services import get_avatar
from src.users.user.validations import is_user, is_deleted
from database import async_engine


class UserCrud:
    @staticmethod
    async def get_my_profile(session, user):
        is_user(user.role_id)
        is_deleted(user)

        try:
            query = select(User).where(User.id == user.id)
            user_profile = await session.execute(query)
            profile = user_profile.scalar_one_or_none()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong in get_me api service. Details:\n{e}")
        finally:
            return UserGetsUser(id=profile.id,
                                email=profile.email,
                                username=profile.username,
                                bio=profile.bio,
                                avatar=await get_avatar(user.id, session))

    @staticmethod
    async def change_profile(profile, session, user):

        is_user(user.role_id)
        is_deleted(user)

        if not profile.avatar_id and not profile.username and not profile.bio:
            try:
                query = select(User).where(User.id == user.id)
                my_profile = await session.execute(query)
                result_list = my_profile.scalars().one()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Something went wrong in change profile api service. "
                                                            f"Details:\n{e}")
            finally:
                return UserGetsUser(id=result_list.id,
                                    email=result_list.email,
                                    username=result_list.username,
                                    bio=result_list.bio,
                                    avatar=await get_avatar(user.id, session))
        else:
            payload = {}
            if profile.avatar_id:
                media_validation = await checked_media(profile.avatar_id, session)
                if not media_validation:
                    raise HTTPException(status_code=400, detail="Something wrong with avatar")
                else:
                    payload["avatar_id"] = profile.avatar_id

                if profile.username:
                    payload["username"] = profile.username

                if profile.bio:
                    payload["bio"] = profile.bio

                try:
                    stmt = update(User).where(User.id == user.id).values(**payload)
                    await session.execute(stmt)
                    await session.commit()

                    stmt2 = update(File).where(File.user_id == user.id).values(is_used=False)
                    await session.execute(stmt2)
                    await session.commit()

                    stmt3 = update(File).where(File.id == profile.avatar_id).values(is_used=True)
                    await session.execute(stmt3)
                    await session.commit()

                    query = select(User).where(User.id == user.id)
                    my_profile = await session.execute(query)
                    result_list = my_profile.scalars().one()

                    stmt4 = delete(File).filter(File.user_id == user.id, File.is_used == False)
                    await session.execute(stmt4)
                    await session.commit()

                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Something went wrong in change profile api service. "
                                                                f"Details:\n{e}")
                finally:
                    return UserGetsUser(id=result_list.id,
                                        email=result_list.email,
                                        username=result_list.username,
                                        bio=result_list.bio,
                                        avatar=await get_avatar(user.id, session))

            else:
                if profile.username:
                    payload["username"] = profile.username

                if profile.bio:
                    payload["bio"] = profile.bio

                try:
                    stmt = update(User).where(User.id == user.id).values(**payload)
                    await session.execute(stmt)
                    await session.commit()

                    query = select(User).where(User.id == user.id)
                    my_profile = await session.execute(query)
                    result_list = my_profile.scalars().one()

                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Something went wrong in change profile api service. "
                                                                f"Details:\n{e}")
                finally:
                    return UserGetsUser(id=result_list.id,
                                        email=result_list.email,
                                        username=result_list.username,
                                        bio=result_list.bio,
                                        avatar=await get_avatar(user.id, session))


    @staticmethod
    async def create_google_user_profile(email, name, session):
        payload = {}
        payload['email'] = email
        payload['hashed_password'] = ""
        payload['is_active'] = True
        payload['is_superuser'] = False
        payload['is_verified'] = True
        payload['username'] = name
        payload['role_id'] = 3
        payload['is_deleted'] = False
        print("HELLO GOOGLE")
        stmt = insert(User).values(email=email,
                                   hashed_password="",
                                   is_active=True,
                                   is_superuser=False,
                                   is_verified=True,
                                   username=name,
                                   role_id=3,
                                   is_deleted=False)
        print(stmt)
        await session.execute(stmt)
        await session.commit()
        print("HELLO GOOGLE2")
        # print(payload)

    # @staticmethod
    # async def complete_registration(profile, session, user):
    #
    #     is_user(user.role_id)
    #     is_deleted(user)
    #
    #     payload = {}
    #
    #     if profile.username is not None:
    #         payload["username"] = profile.username
    #
    #     if profile.bio is not None:
    #         payload["bio"] = profile.bio
    #
    #     try:
    #         stmt = update(User).where(User.id == user.id).values(**payload)
    #         await session.execute(stmt)
    #         await session.commit()
    #
    #         query = select(User).where(User.id == user.id)
    #         my_profile = await session.execute(query)
    #         result_list = my_profile.scalars().one()
    #
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Something went wrong in complete_registration api service. "
    #                                                     f"Details:\n{e}")
    #     finally:
    #         return UserGetsUser(id=result_list.id,
    #                             email=result_list.email,
    #                             username=result_list.username,
    #                             bio=result_list.bio,
    #                             avatar=await get_avatar(user.id, session))


    @staticmethod
    async def get_single_user(session, user_id, user):

        is_user(user.role_id)
        is_deleted(user)

        query = select(User).where(User.id == user_id)
        user_profile = await session.execute(query)
        profile = user_profile.scalar_one_or_none()

        if profile is None or profile.role_id == 1 or profile.role_id == 2:
            raise HTTPException(status_code=404, detail="User not found")

        return UserGetsUser(id=profile.id,
                            email=profile.email,
                            username=profile.username,
                            bio=profile.bio,
                            avatar=await get_avatar(user.id, session))

    @staticmethod
    async def remove_profile(session, user):

        is_user(user.role_id)
        is_deleted(user)
        payload = {"is_deleted": True}

        try:
            stmt = update(User).where(User.id == user.id).values(**payload)
            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong in remove_profile api service. "
                                                        f"Details:\n{e}")
        finally:
            return {f"User: {user.username} is successfully deleted!"}




