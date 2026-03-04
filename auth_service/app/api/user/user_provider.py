from dishka import Provider, Scope, provide  # type: ignore[misc]
from sqlalchemy.ext.asyncio import AsyncSession
from .user_repository import UserRepository
from .user_service import UserService


class UserProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def user_repository(
        self,
        session: AsyncSession,
    ) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def user_service(
        self,
        user_repository: UserRepository,
        session: AsyncSession,
    ) -> UserService:
        return UserService(
            repository=user_repository,
            session=session,
        )
