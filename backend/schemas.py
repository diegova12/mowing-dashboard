# backend/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class JobBase(BaseModel):
    client_id: int
    crew_id: Optional[int]
    service: str
    scheduled: date
    price: float
    latitude: float
    longitude: float

class JobCreate(JobBase):
    pass

class JobSchema(JobBase):
    id: int

    class Config:
        orm_mode = True
