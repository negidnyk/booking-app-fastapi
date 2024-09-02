from pydantic import BaseModel
from typing import Optional


class UploadVideo(BaseModel):
    title: str
    description: str


class FileOut(BaseModel):
    id: int


class MediaOut(BaseModel):
    id: int
    file: str

    class Config:
        from_attributes = True
