from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.bookings.repository import BookingRepository
from app.bookings.models import Bookings
from app.bookings.schemas import BookingCreate, BookingUpdate, BookingResponse


class BookingService:
    def __init__(
        self,
        repository: BookingRepository
    ):
        self.repository = repository

    async def get_all(
        self,
        session: AsyncSession
    ) -> List[BookingResponse]:
        bookings = await self.repository.get_all(session)
        return [BookingResponse.model_validate(booking) for booking in bookings]

    async def get_by_id(
        self,
        session: AsyncSession,
        booking_id: int
    ) -> Optional[BookingResponse]:
        booking = await self.repository.find_one_or_none(session, id=booking_id)
        return BookingResponse.model_validate(booking) if booking else None

    async def create(
        self,
        session: AsyncSession,
        booking_data: BookingCreate
    ) -> BookingResponse:
        booking = Bookings(**booking_data.dict())
        new_booking = await self.repository.create(session, booking)
        return BookingResponse.model_validate(new_booking)

    async def update(
        self,
        session: AsyncSession,
        booking_id: int,
        update_data: BookingUpdate
    ) -> Optional[BookingResponse]:
        values = update_data.dict(exclude_unset=True)
        updated_booking = await self.repository.update(session, booking_id, values)
        return BookingResponse.model_validate(updated_booking) if updated_booking else None

    async def delete(
        self,
        session: AsyncSession,
        booking_id: int
    ) -> bool:
        return await self.repository.delete(session, booking_id)

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

        bookings = await self.repository.get_all(session, filters=filters)
        return [BookingResponse(**booking.__dict__) for booking in bookings]

