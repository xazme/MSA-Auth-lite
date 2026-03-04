from sqlalchemy.ext.asyncio import AsyncSession
from app.infastructure.database import BaseRepository
from .user_model import User


class UserRepository(BaseRepository[User]):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(
            model=User,
            session=session,
        )
