from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from src.beauty_services.models import BeautyService
from src.beauty_services.schemas import CreateBeautyService, GetBeautyService


class BeautyServiceCrud:
    @staticmethod
    async def create_service(service_details, session, user):
        payload = {}
        payload["name"] = service_details.name
        payload["added_by"] = user.id
        payload["description"] = service_details.description

        try:
            stmt = insert(BeautyService).values(**payload)
            await session.execute(stmt)
            await session.commit()
            query = select(BeautyService).limit(1).order_by(BeautyService.created_at.desc())
            created_service = await session.execute(query)
            result = created_service.scalar_one_or_none()
            return GetBeautyService(id=result.id,
                                    name=result.name,
                                    description=result.description,
                                    added_by=result.added_by,
                                    created_at=result.created_at)
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in create beauty service api service. Details:\n{e}")
