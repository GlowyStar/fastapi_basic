from typing import List, Optional, Type, TypeVar, Generic, Sequence
from sqlalchemy.sql.expression import ClauseElement, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")  # Тип модели


class BaseRepository(Generic[T]):
    def __init__(
        self,
        model: Type[T]
    ):
        self.model = model

    async def get_all(
        self,
        session: AsyncSession,
        filters: Optional[List[ClauseElement]] = None,
        **filter_by,
    ) -> Sequence[T]:
        query: Select = select(self.model)

        if filters:
            query = query.filter(*filters)

        if filter_by:
            query = query.filter_by(**filter_by)

        result = await session.execute(query)
        return result.scalars().all()

    async def find_one_or_none(
        self,
        session: AsyncSession,
        filters: Optional[List[ClauseElement]] = None,
        **filter_by,
    ) -> Optional[T]:
        query: Select = select(self.model)

        if filters:
            query = query.filter(*filters)

        if filter_by:
            query = query.filter_by(**filter_by)

        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        session: AsyncSession,
        item_id: int
    ) -> Optional[T]:
        query = select(self.model).where(self.model.id == item_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def update(
        self,
        session: AsyncSession,
        item_id: int,
        values: dict
    ) -> Optional[T]:
        query = select(self.model).where(self.model.id == item_id)
        result = await session.execute(query)
        instance = result.scalars().first()
        if not instance:
            return None
        for key, value in values.items():
            setattr(instance, key, value)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def delete(
        self,
        session: AsyncSession,
        item_id: int
    ) -> bool:
        query = select(self.model).where(self.model.id == item_id)
        result = await session.execute(query)
        instance = result.scalars().first()
        if not instance:
            return False
        await session.delete(instance)
        await session.commit()
        return True

    @staticmethod
    async def create(
        session: AsyncSession,
        obj: T
    ) -> T:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
