from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from src.beauty_services.models import BeautyService, BeautyServiceGroup, BeautyServiceWithGroup
from src.beauty_services.schemas import CreateBeautyService, GetBeautyService, CreateBeautyServiceGroup, \
    GetBeautyServiceGroup, GetBeautyServiceByGroup, GetBeautyServiceByGroupList
from src.beauty_services.helpers import get_service_group_by_service, get_service_by_id
from src.users.user.validations import is_user, is_admin, is_master, is_deleted


class BeautyServiceCrud:
    @staticmethod
    async def create_service(service_details, session, user):

        await is_admin(user.id)

        try:
            stmt = insert(BeautyService).values(name=service_details.name, added_by=user.id)
            await session.execute(stmt)
            await session.commit()

            query = select(BeautyService).limit(1).order_by(BeautyService.created_at.desc())
            created_service = await session.execute(query)
            result = created_service.scalar_one_or_none()

            stmt2 = insert(BeautyServiceWithGroup).values(service_id=result.id, group_id=service_details.group_id)
            await session.execute(stmt2)
            await session.commit()

            return GetBeautyService(id=result.id,
                                    name=result.name,
                                    group=await get_service_group_by_service(result.id, session),
                                    added_by=result.added_by,
                                    created_at=result.created_at)
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in create beauty service api service. Details:\n{e}")

    @staticmethod
    async def create_service_group(group_details, session, user):

        await is_admin(user.id)

        try:
            stmt = insert(BeautyServiceGroup).values(name=group_details.name, added_by=user.id)
            await session.execute(stmt)
            await session.commit()
            query = select(BeautyServiceGroup).limit(1).order_by(BeautyServiceGroup.created_at.desc())
            created_service = await session.execute(query)
            result = created_service.scalar_one_or_none()
            return GetBeautyServiceGroup(id=result.id,
                                         name=result.name,
                                         added_by=result.added_by,
                                         created_at=result.created_at)
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in create beauty service group api service. Details:\n{e}")

    @staticmethod
    async def get_all_beauty_services(skip, limit, session, user):

        await is_admin(user.id)

        try:
            query = select(BeautyService).limit(limit).offset(skip)
            services_list = await session.execute(query)
            result_list = services_list.scalars().all()
            return [GetBeautyService(id=service.id,
                                     name=service.name,
                                     group=await get_service_group_by_service(service.id, session),
                                     added_by=service.added_by,
                                     created_at=service.created_at) for service in result_list]

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in get all beauty services api service. Details:\n{e}")

    @staticmethod
    async def get_beauty_services_by_group(group_id, skip, limit, session, user):

        await is_admin(user.id)

        try:
            query = select(BeautyServiceWithGroup).limit(limit).offset(skip).\
                join(BeautyService, BeautyServiceWithGroup.service_id == BeautyService.id).\
                where(BeautyServiceWithGroup.group_id == group_id)
            services_list = await session.execute(query)
            result_list = services_list.scalars().all()

            return [GetBeautyServiceByGroupList(id=serv.service_id,
                                                service=await get_service_by_id(serv.service_id, session))
                    for serv in result_list]

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in get all beauty services api service. Details:\n{e}")