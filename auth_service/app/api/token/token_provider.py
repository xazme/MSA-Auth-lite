from dishka import Provider, Scope, provide  # type: ignore[misc]
from sqlalchemy.ext.asyncio import AsyncSession
from .token_repository import TokenRepository
from .token_service import TokenService


class TokenProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def token_repository(
        self,
        session: AsyncSession,
    ) -> TokenRepository:
        return TokenRepository(session)

    @provide(scope=Scope.REQUEST)
    def token_service(
        self,
        token_repository: TokenRepository,
        session: AsyncSession,
    ) -> TokenService:
        return TokenService(
            repository=token_repository,
            session=session,
        )
