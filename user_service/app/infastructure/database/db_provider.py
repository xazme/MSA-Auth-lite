from dishka import Provider, Scope, provide  # type: ignore[misc]
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from .db_helper import DataBaseHelper, create_db_helper


class DataBaseProvider(Provider):

    @provide(scope=Scope.APP)
    async def db_helper(self) -> DataBaseHelper:
        return create_db_helper()

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        db_helper: DataBaseHelper,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with db_helper.get_session() as session:
            yield session
