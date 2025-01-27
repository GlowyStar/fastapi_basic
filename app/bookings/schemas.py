from pydantic import BaseModel
from datetime import date
from typing import Optional


class BookingBase(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    price: Optional[int] = None


class BookingResponse(BookingBase):
    id: int
    total_cost: Optional[int]
    total_days: Optional[int]

    class Config:
        from_attributes = True

