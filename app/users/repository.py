from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.orm.repository import BaseRepository
from app.users.models import Users


class UserRepository(BaseRepository[Users]):
    def __init__(self):
        super().__init__(Users)

    async def get_user_by_email(
        self,
        session: AsyncSession,
        email: str
    ) -> Optional[Users]:
        filters = [Users.email == email]
        return await self.find_one_or_none(session, filters=filters)
