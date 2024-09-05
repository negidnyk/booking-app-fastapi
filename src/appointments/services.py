from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from src.appointments.models import Appointment
from src.appointments.schemas import GetCreatedAppointment


class AppointmentsCrud:
    @staticmethod
    async def create_appointment(appointment_details, session, user):
        payload = {}
        payload["master_id"] = appointment_details.master_id
        payload["user_id"] = user.id
        payload["description"] = appointment_details.description
        payload["service_id"] = appointment_details.service_id
        payload["price"] = appointment_details.price
        payload["booked_at"] = appointment_details.booked_at
        payload["booked_to"] = appointment_details.booked_to
        payload["is_approved_by_master"] = appointment_details.is_approved_by_master
        payload["is_visited_by_user"] = appointment_details.is_visited_by_user

        try:
            stmt = insert(Appointment).values(**payload)
            await session.execute(stmt)
            await session.commit()

            query = select(Appointment).limit(1).order_by(Appointment.created_at.desc())
            created_appointment = await session.execute(query)
            result = created_appointment.scalar_one_or_none()

            return GetCreatedAppointment(id=result.id,
                                         master_id=result.master_id,
                                         user_id=result.user_id,
                                         description=result.description,
                                         service_id=result.service_id,
                                         price=result.price,
                                         booked_at=result.booked_at,
                                         booked_to=result.booked_to,
                                         created_at=result.created_at,
                                         is_approved_by_master=result.is_approved_by_master,
                                         is_visited_by_user=result.is_visited_by_user)
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in create appointment api service. Details:\n{e}")
