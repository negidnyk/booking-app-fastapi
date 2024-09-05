from fastapi import HTTPException
from sqlalchemy import select, update, insert, delete
from src.appointments.models import Appointment
from src.auth.models import User
