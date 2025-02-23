from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.orm.repository import BaseRepository
from app.rooms.models import Rooms


class RoomRepository(BaseRepository[Rooms]):
    def __init__(self):
        super().__init__(Rooms)

    async def get_by_id(
        self,
        session: AsyncSession,
        room_id: int
    ) -> Optional[Rooms]:
        return await super().get_by_id(session, room_id)
