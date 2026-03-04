from typing import TypeVar, Generic, Any, Optional, Sequence
from sqlalchemy.sql import ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.infastructure.database import Base
from app.infastructure.database.db_exceptions import (
    DataBaseObjectNotFoundException,
    DataBaseObjectAlreadyExistsException,
)
from .db_domain_exceptions import (
    ObjectNotFoundException,
    ObjectAlreadyExistsException,
)
from .base_repository import BaseRepository

T = TypeVar(name="T", bound=Base)


class BaseService(Generic[T]):
    """Base Service"""

    def __init__(
        self,
        repository: BaseRepository[T],
        session: AsyncSession,
    ) -> None:
        self.repository: BaseRepository[T] = repository
        self.session: AsyncSession = session

    async def get(self, id: Any) -> Optional[T]:
        return await self.repository.get(id=id)

    async def get_one(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> T:
        try:
            return await self.repository.get_one(*where, **where_by)
        except DataBaseObjectNotFoundException:
            raise ObjectNotFoundException(model_name=self.repository.model.__name__)

    async def get_one_or_none(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Optional[T]:
        return await self.repository.get_one_or_none(*where, **where_by)

    async def get_all(
        self,
    ) -> Sequence[T]:
        return await self.repository.get_all()

    async def get_all_filtered(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> Sequence[T]:
        return await self.repository.get_all_filtered(*where, **where_by)

    async def exists(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> bool:
        return await self.repository.exists(*where, **where_by)

    async def count(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> int:
        return await self.repository.count(*where, **where_by)

    async def create(
        self,
        payload: dict[str, Any],
    ) -> T:
        try:
            obj = await self.repository.create(payload=payload)
            await self._safe_commit()
            return obj
        except DataBaseObjectAlreadyExistsException:
            raise ObjectAlreadyExistsException(
                model_name=self.repository.model.__name__
            )

    async def update(
        self,
        payload: dict[str, Any],
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> T:
        try:
            obj = await self.repository.update(payload=payload, *where, **where_by)
            await self._safe_commit()
            return obj
        except DataBaseObjectAlreadyExistsException:
            raise ObjectAlreadyExistsException(
                model_name=self.repository.model.__name__
            )
        except DataBaseObjectNotFoundException:
            raise ObjectNotFoundException(model_name=self.repository.model.__name__)

    async def update_by_id(
        self,
        id: Any,
        payload: dict[str, Any],
    ) -> T:
        try:
            obj = await self.repository.update(payload=payload, id=id)
            await self._safe_commit()
            return obj
        except DataBaseObjectAlreadyExistsException:
            raise ObjectAlreadyExistsException(
                model_name=self.repository.model.__name__
            )
        except DataBaseObjectNotFoundException:
            raise ObjectNotFoundException(model_name=self.repository.model.__name__)

    async def delete(
        self,
        *where: ColumnElement[bool],
        **where_by: Any,
    ) -> None:
        await self.repository.delete(*where, **where_by)
        await self._safe_commit()

    async def delete_by_id(
        self,
        id: Any,
    ) -> None:
        await self.repository.delete(id=id)
        await self._safe_commit()

    async def _safe_commit(self):
        try:
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise
