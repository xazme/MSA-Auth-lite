from dishka import Provider, Scope, provide  # type: ignore[misc]
from app.core.config import settings
from .jwt_helper import JWTHelper


class JWTProvider(Provider):
    @provide(scope=Scope.APP)
    def jwt_helper(self) -> JWTHelper:
        return JWTHelper(
            alogrithm=settings.algorithm,
            expire_days=settings.expire_days,
            expire_minutes=settings.expire_minutes,
            access_private_key=settings.access_private_key,
            access_public_key=settings.access_public_key,
            refresh_private_key=settings.refresh_private_key,
            refresh_public_key=settings.refresh_public_key,
        )
