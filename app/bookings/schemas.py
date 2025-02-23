from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class BookingBase(BaseModel):
    room_id: int = Field(..., description="ID комнаты")
    user_id: int = Field(..., description="ID пользователя")
    date_from: date = Field(..., description="Дата начала бронирования")
    date_to: date = Field(..., description="Дата окончания бронирования")
    price: int = Field(..., gt=0, description="Цена бронирования, должна быть больше 0")


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    room_id: Optional[int] = Field(None, description="Обновленный ID комнаты")
    user_id: Optional[int] = Field(None, description="Обновленный ID пользователя")
    date_from: Optional[date] = Field(None, description="Обновленная дата начала бронирования")
    date_to: Optional[date] = Field(None, description="Обновленная дата окончания бронирования")
    price: Optional[int] = Field(None, gt=0, description="Обновленная цена бронирования, должна быть больше 0")


class BookingResponse(BookingBase):
    id: int = Field(..., description="ID бронирования")
    total_cost: Optional[int] = Field(None, description="Общая стоимость бронирования")
    total_days: Optional[int] = Field(None, description="Общее количество дней бронирования")

    class Config:
        from_attributes = True
