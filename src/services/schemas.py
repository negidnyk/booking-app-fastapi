from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
# from sqlalchemy.sql import func
from datetime import datetime, time, timedelta
from uuid import UUID


class ServiceTypes(str, Enum):
    manicure = "manicure"
    pedicure = "pedicure"
    haircut = "haircut"

