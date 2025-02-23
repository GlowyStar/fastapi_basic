from fastapi import HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.bookings.repository import BookingRepository
from app.bookings.models import Bookings
from app.bookings.schemas import BookingCreate, BookingUpdate, BookingResponse
from app.rooms.repository import RoomRepository
from app.users.repository import UserRepository

class BookingService:
    def __init__(
        self,
        booking_repository: BookingRepository,
        room_repository: RoomRepository,
        user_repository: UserRepository
    ):
        self.booking_repository = booking_repository
        self.room_repository = room_repository
        self.user_repository = user_repository

    async def get_all(
        self,
        session: AsyncSession
    ) -> List[BookingResponse]:
        bookings = await self.booking_repository.get_all(session)
        return [BookingResponse.model_validate(booking) for booking in bookings]

    async def get_by_id(
        self,
        session: AsyncSession,
        booking_id: int
    ) -> BookingResponse:
        booking = await self.booking_repository.find_one_or_none(session, id=booking_id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Бронирование с id {booking_id} не найдено.",
            )
        return BookingResponse.model_validate(booking)

    async def create(
        self,
        session: AsyncSession,
        booking_data: BookingCreate
    ) -> BookingResponse:
        # Проверка существования комнаты
        room = await self.room_repository.get_by_id(session, booking_data.room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Комната с id {booking_data.room_id} не существует.",
            )
        # Проверка существования пользователя
        user = await self.user_repository.get_by_id(session, booking_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Пользователь с id {booking_data.user_id} не существует.",
            )
        booking = Bookings(**booking_data.dict())
        new_booking = await self.booking_repository.create(session, booking)
        return BookingResponse.model_validate(new_booking)

    async def update(
        self,
        session: AsyncSession,
        booking_id: int,
        update_data: BookingUpdate
    ) -> BookingResponse:
        # Проверка существования бронирования
        existing_booking = await self.booking_repository.find_one_or_none(session, id=booking_id)
        if not existing_booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Бронирование с id {booking_id} не найдено.",
            )
        # Проверка существования комнаты, если обновляется room_id
        if update_data.room_id is not None:
            room = await self.room_repository.get_by_id(session, update_data.room_id)
            if not room:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Комната с id {update_data.room_id} не существует.",
                )
        # Проверка существования пользователя, если обновляется user_id
        if update_data.user_id is not None:
            user = await self.user_repository.get_by_id(session, update_data.user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Пользователь с id {update_data.user_id} не существует.",
                )
        values = update_data.dict(exclude_unset=True)
        updated_booking = await self.booking_repository.update(session, booking_id, values)
        if not updated_booking:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Не удалось обновить бронирование с id {booking_id}.",
            )
        return BookingResponse.model_validate(updated_booking)

    async def delete(
        self,
        session: AsyncSession,
        booking_id: int
    ) -> bool:
        # Проверка существования бронирования
        booking = await self.booking_repository.find_one_or_none(session, id=booking_id)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Бронирование с id {booking_id} не найдено.",
            )
        deleted = await self.booking_repository.delete(session, booking_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Не удалось удалить бронирование с id {booking_id}.",
            )
        return True

    async def get_filtered(
        self,
        session: AsyncSession,
        user_id: Optional[int] = None,
        room_id: Optional[int] = None,
    ) -> List[BookingResponse]:
        filters = []
        if user_id is not None:
            filters.append(Bookings.user_id == user_id)
        if room_id is not None:
            filters.append(Bookings.room_id == room_id)

        bookings = await self.booking_repository.get_all(session, filters=filters)
        return [BookingResponse.model_validate(booking) for booking in bookings]
