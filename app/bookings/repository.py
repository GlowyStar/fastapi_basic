from typing import List, Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import ClauseElement
from app.orm.repository import BaseRepository
from app.bookings.models import Bookings


class BookingRepository(BaseRepository):
    def __init__(self):
        super().__init__(Bookings)

    async def get_bookings_by_user(
        self,
        session: AsyncSession,
        user_id: int
    ) -> Sequence[Bookings]:
        filters = [Bookings.user_id == user_id]
        return await self.get_all(session, filters=filters)

    async def get_bookings_by_room(
        self,
        session: AsyncSession,
        room_id: int
    ) -> Sequence[Bookings]:
        filters = [Bookings.room_id == room_id]
        return await self.get_all(session, filters=filters)
