from typing import Sequence, TypeVar, Generic, Any, Optional
from sqlalchemy import delete, insert, select, func, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from .db_exceptions import (
    DataBaseObjectNotFoundException,
    DataBaseObjectAlreadyExistsException,
)

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Base Repostirory"""

    def __init__(
        self,
        model: type[T],
        session: AsyncSession,
    ) -> None:
        self.model: type[T] = model
        self.session: AsyncSession = session

    async def get(
        self,
        id: Any,
    ) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == id)

        orm_obj = await self.session.execute(statement=stmt)
        return orm_obj.scalar_one_or_none()

    async def get_one(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> T:
        stmt = select(self.model)

        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)

        try:
            res = await self.session.execute(statement=stmt)
            orm_obj = res.scalar_one()
            return orm_obj
        except NoResultFound:
            raise DataBaseObjectNotFoundException()

    async def get_one_or_none(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Optional[T]:
        stmt = select(self.model)

        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)

        res = await self.session.execute(statement=stmt)
        return res.scalar_one_or_none()

    async def get_all(
        self,
    ) -> Sequence[T]:
        stmt = select(self.model)

        res = await self.session.execute(statement=stmt)
        return res.scalars().all()

    async def get_all_filtered(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Sequence[T]:
        stmt = select(self.model)

        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)

        res = await self.session.execute(statement=stmt)
        return res.scalars().all()

    async def exists(
        self,
        /,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> bool:
        stmt = select(func.count()).select_from(self.model)

        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)

        res = await self.session.execute(statement=stmt)
        return bool(res.scalar_one())

    async def count(
        self,
        /,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> int:
        stmt = select(func.count()).select_from(self.model)

        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)

        res = await self.session.execute(statement=stmt)
        return res.scalar_one()

    async def create(
        self,
        payload: dict[str, Any],
    ) -> T:
        stmt = insert(self.model).values(**payload).returning(self.model)

        try:
            res = await self.session.execute(statement=stmt)
            obj = res.scalar_one()
            return obj
        except IntegrityError:
            await self.session.rollback()
            raise DataBaseObjectAlreadyExistsException()

    async def update(
        self,
        /,
        payload: dict[str, Any],
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> T:
        stmt = update(self.model).values(**payload).returning(self.model)
        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)

        try:
            res = await self.session.execute(statement=stmt)
            obj = res.scalar_one()
            return obj
        except NoResultFound:
            raise DataBaseObjectNotFoundException(
                f"{self.model.__name__} not found for update",
            )
        except IntegrityError:
            await self.session.rollback()
            raise DataBaseObjectAlreadyExistsException()

    async def delete(
        self,
        /,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> None:
        stmt = delete(self.model)
        if not where and not where_by:
            raise ValueError("Delete without filter is not allowed")
        if where:
            stmt = stmt.filter(*where)
        if where_by:
            stmt = stmt.filter_by(**where_by)

        await self.session.execute(statement=stmt)
