from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.infastructure.database import BaseService, BaseRepository
from app.infastructure.database.db_exceptions import (
    DataBaseObjectAlreadyExistsException,
)
from app.infastructure.database.db_domain_exceptions import ObjectAlreadyExistsException
from .user_producer import UserKafkaProducer
from .user_model import User
from .user_dto import UpdateUserDTO
from .user_events import UserUpdateEvent


class UserService(BaseService[User]):
    def __init__(
        self,
        repository: BaseRepository[User],
        producer: UserKafkaProducer,
        session: AsyncSession,
    ) -> None:
        super().__init__(
            repository=repository,
            session=session,
        )
        self.user_producer = producer
        self.user_repository = repository

    async def update_user(
        self,
        id: UUID,
        payload: UpdateUserDTO,
    ) -> User:
        try:
            updated_user = await self.repository.update(
                id=id,
                payload=payload.model_dump(exclude_unset=True),
            )
        except DataBaseObjectAlreadyExistsException:
            raise ObjectAlreadyExistsException(
                details="Try again",
                model_name=User.__name__,
            )

        await self.user_producer.publish_update(
            user_id=updated_user.id,
            payload=UserUpdateEvent.model_validate(updated_user),
        )
        await self._safe_commit()
        return updated_user
