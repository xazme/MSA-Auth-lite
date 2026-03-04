from typing import Any
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.infastructure.database import BaseRepository
from .token_model import Token


class TokenRepository(BaseRepository[Token]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=Token, session=session)

    async def upsert(self, payload: dict[str, Any]):
        stmt = insert(table=self.model).values(**payload)
        stmt = stmt.on_conflict_do_update(
            index_elements=["user_id"],
            set_=dict(
                refresh_token=payload.get("refresh_token"),
            ),
        )
        await self.session.execute(statement=stmt)
